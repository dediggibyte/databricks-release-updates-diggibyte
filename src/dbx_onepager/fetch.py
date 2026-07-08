"""Fetch and normalize Databricks release notes.

Databricks docs sit behind bot protection that 403s plain HTTP clients, so the
primary transport is a real headless Chromium via Playwright. A urllib
fallback (browser User-Agent) is used if Playwright is unavailable, and a
fixture loader lets the whole pipeline run offline for development and CI dry
runs.

Two ingestion modes:
* ``fetch_rss``            — weekly incremental: the release-notes RSS feed.
* ``fetch_archive_range`` — historical backfill: walk monthly archive pages.
"""

from __future__ import annotations

import calendar
import json
import re
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from dateutil import parser as dateparser

from .models import ReleaseNote

_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
_DATE_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{1,2},\s+\d{4}\b"
)
# Maturity phrases Databricks uses, mapped to our status vocabulary.
_STATUS_HINTS = [
    ("public preview", "public-preview", "Public Preview"),
    ("gated preview", "gated-preview", "Gated Preview"),
    ("beta", "beta", "Beta"),
    ("generally available", "ga", "GA"),
    ("now available", "ga", "GA"),
    ("end of support", "eol", "EOL"),
    ("end-of-life", "eol", "EOL"),
]


# --------------------------------------------------------------------------
# Transport
# --------------------------------------------------------------------------
def fetch_url(url: str, timeout: int = 45) -> str:
    """Return page HTML. Prefer Playwright (bypasses bot walls); fall back to
    urllib with a browser UA. Raises the last error if both fail."""
    try:
        return _fetch_playwright(url, timeout)
    except Exception as pw_err:  # noqa: BLE001 - fall back deliberately
        try:
            return _fetch_urllib(url, timeout)
        except Exception as ul_err:  # noqa: BLE001
            raise RuntimeError(
                f"fetch failed for {url}: playwright={pw_err!r} urllib={ul_err!r}"
            ) from ul_err


def _fetch_playwright(url: str, timeout: int) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=_UA)
            page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            # Docs pages hydrate; give the main content a moment.
            page.wait_for_timeout(800)
            return page.content()
        finally:
            browser.close()


def _fetch_urllib(url: str, timeout: int) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")


# --------------------------------------------------------------------------
# Parsing helpers
# --------------------------------------------------------------------------
def detect_status(text: str) -> tuple[str, str]:
    """Return (status, label). Defaults to a neutral 'changed'/'Update'.

    Whitespace is collapsed first so line-wrapped phrases (common in scraped
    docs and RSS bodies), e.g. "Public\\nPreview", still match.
    """
    low = re.sub(r"\s+", " ", text).lower()
    for needle, status, label in _STATUS_HINTS:
        if needle in low:
            return status, label
    return "changed", "Update"


def _extract_date(text: str, fallback: date) -> date:
    m = _DATE_RE.search(text)
    if m:
        try:
            return dateparser.parse(m.group(0)).date()
        except (ValueError, OverflowError):
            pass
    return fallback


def _html_to_markdown(html: str) -> str:
    from markdownify import markdownify as md

    text = md(html, heading_style="ATX", strip=["img"])
    # Collapse excessive blank lines.
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# --------------------------------------------------------------------------
# RSS ingestion (weekly incremental)
# --------------------------------------------------------------------------
def fetch_rss(cfg: dict) -> list[ReleaseNote]:
    import feedparser

    src = cfg["source"]
    raw = fetch_url(src["rss_url"])
    feed = feedparser.parse(raw)
    notes: list[ReleaseNote] = []
    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        if not title:
            continue
        link = entry.get("link") or src["index_url"]
        published = entry.get("published") or entry.get("updated") or ""
        try:
            note_date = dateparser.parse(published).date() if published else date.today()
        except (ValueError, OverflowError):
            note_date = date.today()
        summary_html = ""
        if entry.get("content"):
            summary_html = entry["content"][0].get("value", "")
        summary_html = summary_html or entry.get("summary", "")
        body = _html_to_markdown(summary_html) if summary_html else title
        notes.append(
            ReleaseNote(
                id=ReleaseNote.make_id(note_date, title),
                title=title,
                date=note_date,
                url=link,
                cloud=src.get("cloud", "aws"),
                category=cfg["source"].get("category", "platform"),
                body=body,
                source="rss",
                fetched_at=datetime.now(timezone.utc),
            )
        )
    return notes


# --------------------------------------------------------------------------
# Archive ingestion (historical backfill)
# --------------------------------------------------------------------------
def parse_archive_html(html: str, year: int, month: int, cfg: dict) -> list[ReleaseNote]:
    """Split a monthly archive page into individual release notes.

    Heuristic: each release note is an ``h2``/``h3`` heading followed by prose
    up to the next heading of the same-or-higher level. Works against the
    generic Databricks docs article structure.
    """
    from bs4 import BeautifulSoup

    src = cfg["source"]
    month_start = date(year, month, 1)
    soup = BeautifulSoup(html, "lxml")
    article = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", attrs={"role": "main"})
        or soup.body
        or soup
    )
    headings = article.find_all(["h2", "h3"])
    notes: list[ReleaseNote] = []
    for h in headings:
        title = h.get_text(" ", strip=True)
        if not title or len(title) < 4:
            continue
        # Collect sibling content until the next h2/h3.
        frag: list[str] = []
        for sib in h.find_all_next():
            if sib in headings:
                break
            if sib.name in ("h2", "h3"):
                break
            if sib.name in ("p", "ul", "ol", "pre", "table", "blockquote"):
                frag.append(str(sib))
        body_html = "".join(frag)
        body = _html_to_markdown(body_html) if body_html else title
        note_date = _extract_date(title + " " + body, month_start)
        # Prefer an anchor link if the heading has an id.
        anchor = h.get("id")
        url = f"{src['archive_pattern'].format(year=year, month=calendar.month_name[month].lower())}"
        if anchor:
            url = f"{url}#{anchor}"
        notes.append(
            ReleaseNote(
                id=ReleaseNote.make_id(note_date, title),
                title=title,
                date=note_date,
                url=url,
                cloud=src.get("cloud", "aws"),
                category="platform",
                body=body,
                source="archive",
                fetched_at=datetime.now(timezone.utc),
            )
        )
    return notes


def fetch_archive_month(cfg: dict, year: int, month: int) -> list[ReleaseNote]:
    src = cfg["source"]
    url = src["archive_pattern"].format(
        year=year, month=calendar.month_name[month].lower()
    )
    html = fetch_url(url)
    return parse_archive_html(html, year, month, cfg)


def _month_iter(start: date, end: date) -> Iterable[tuple[int, int]]:
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        yield y, m
        m += 1
        if m > 12:
            m = 1
            y += 1


def fetch_archive_range(cfg: dict, start: date, end: date) -> list[ReleaseNote]:
    """Walk monthly archive pages in [start, end]. Missing months are skipped."""
    notes: list[ReleaseNote] = []
    for year, month in _month_iter(start, end):
        try:
            notes.extend(fetch_archive_month(cfg, year, month))
        except Exception as err:  # noqa: BLE001 - one bad month shouldn't abort
            print(f"  ! skipped {year}-{month:02d}: {err}")
    return notes


# --------------------------------------------------------------------------
# Fixtures (offline)
# --------------------------------------------------------------------------
def load_fixtures(fixtures_dir: Path) -> list[ReleaseNote]:
    """Load sample release notes from ``fixtures/`` for offline runs/tests.

    Supports ``*.json`` (full ReleaseNote) and ``*.md`` (front-matter-lite:
    first line ``# Title``, optional ``> date: YYYY-MM-DD``, rest is body).
    """
    notes: list[ReleaseNote] = []
    for jf in sorted(fixtures_dir.glob("*.json")):
        notes.append(ReleaseNote.model_validate_json(jf.read_text(encoding="utf-8")))
    for mf in sorted(fixtures_dir.glob("*.md")):
        notes.append(_note_from_markdown(mf))
    return notes


def _note_from_markdown(path: Path) -> ReleaseNote:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = "Untitled"
    note_date = date.today()
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body_start = i + 1
        elif line.lower().startswith("> date:"):
            try:
                note_date = dateparser.parse(line.split(":", 1)[1].strip()).date()
            except (ValueError, OverflowError):
                pass
            body_start = i + 1
        elif line.strip() and not line.startswith(("#", ">")):
            break
    body = "\n".join(lines[body_start:]).strip()
    return ReleaseNote(
        id=ReleaseNote.make_id(note_date, title),
        title=title,
        date=note_date,
        url=f"https://docs.databricks.com/aws/en/release-notes/product/#{path.stem}",
        body=body,
        source="fixture",
        fetched_at=datetime.now(timezone.utc),
    )
