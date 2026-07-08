"""Turn a raw release note into a filled one-pager via Claude.

The model is forced to return the exact ``OnePager`` contract through a
tool-use call whose input schema is generated from the Pydantic model — so the
prompt, schema, and template can never drift apart.

If no ``ANTHROPIC_API_KEY`` is present (local dev, CI dry run) or ``--mock`` is
requested, a deterministic heuristic builds a reasonable one-pager from the
note text so the whole pipeline is runnable offline.
"""

from __future__ import annotations

import json
import os
import re
from typing import Optional

from .fetch import detect_status
from .models import Capability, OnePager, ReleaseNote, Step

_TOOL_NAME = "emit_one_pager"

_SYSTEM = """You are a Databricks platform analyst who writes crisp executive \
one-pagers about product release notes. For each release note you receive, \
produce a single one-pager that explains the update BOTH technically (what \
changed, how it works, prerequisites, limitations) AND from a business \
perspective (why it matters, who benefits, use cases).

Rules:
- Be specific and factual to the release note. Never invent version numbers, \
dates, or features that are not implied by the text.
- "what_it_does" is technical and concrete. "why_it_matters" is business \
impact for a data/platform leader.
- Keep capabilities to at most 4, each a short title + one sentence.
- Prerequisites, limitations, use_cases, steps: only include what the note \
supports; leave a list empty rather than padding it.
- "architecture" is an ordered list of 3-6 short stage/component labels showing \
where this fits in the data stack (e.g. "Unity Catalog", "Serverless SQL").
- "updated" must be a human date like "Jun 16, 2026".
- "status"/"status_label" reflect the maturity (GA, Public Preview, Beta, \
etc.). Use "changed"/"Update" if unclear.
- "key_takeaway" is one punchy sentence a busy executive can skim.
Call the emit_one_pager tool exactly once with the structured result."""


def _prompt_for(note: ReleaseNote) -> str:
    return (
        f"Release note title: {note.title}\n"
        f"Date: {note.date.isoformat()}\n"
        f"Cloud: {note.cloud}\n"
        f"Source URL: {note.url}\n\n"
        f"Release note content:\n{note.body[:8000]}\n"
    )


def enrich_note(
    note: ReleaseNote,
    cfg: dict,
    model: Optional[str] = None,
    mock: bool = False,
) -> OnePager:
    use_mock = mock or not os.environ.get("ANTHROPIC_API_KEY")
    if use_mock:
        op = _heuristic_onepager(note)
    else:
        op = _llm_onepager(note, cfg, model)
    # Fields the model must not set — always sourced from the record.
    op.note_id = note.id
    op.category = note.category
    op.source_url = note.url
    if not op.docs_url:
        op.docs_url = note.url
    return op


# --------------------------------------------------------------------------
# LLM path
# --------------------------------------------------------------------------
def _llm_onepager(note: ReleaseNote, cfg: dict, model: Optional[str]) -> OnePager:
    import anthropic

    client = anthropic.Anthropic()
    llm = cfg["llm"]
    chosen = model or llm["model"]
    tool = {
        "name": _TOOL_NAME,
        "description": "Emit the structured one-pager for this release note.",
        "input_schema": OnePager.json_schema_for_llm(),
    }
    resp = client.messages.create(
        model=chosen,
        max_tokens=llm.get("max_tokens", 2000),
        temperature=llm.get("temperature", 0.2),
        system=_SYSTEM,
        tools=[tool],
        tool_choice={"type": "tool", "name": _TOOL_NAME},
        messages=[{"role": "user", "content": _prompt_for(note)}],
    )
    for block in resp.content:
        if block.type == "tool_use" and block.name == _TOOL_NAME:
            return OnePager.model_validate(block.input)
    raise RuntimeError(f"model did not return a {_TOOL_NAME} tool call for {note.id}")


# --------------------------------------------------------------------------
# Offline heuristic path (no API key required)
# --------------------------------------------------------------------------
def _sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", re.sub(r"[#>*`_\-]{1,}", " ", text)).strip()
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def _bullets(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        m = re.match(r"\s*[-*+]\s+(.*)", line)
        if m and len(m.group(1).strip()) > 4:
            out.append(re.sub(r"[`*_]", "", m.group(1)).strip())
    return out


def _heuristic_onepager(note: ReleaseNote) -> OnePager:
    """Best-effort, deterministic one-pager built without an LLM.

    Not as good as the model, but structurally complete — used for offline
    development, CI dry runs, and as a graceful fallback.
    """
    status, label = detect_status(note.title + " " + note.body)
    sents = _sentences(note.body)
    bullets = _bullets(note.body)
    tagline = sents[0] if sents else note.title
    what = " ".join(sents[:2]) if sents else note.body[:280] or note.title
    why = (
        sents[2]
        if len(sents) > 2
        else "Reduces operational overhead and unlocks new capabilities for data teams on Databricks."
    )
    caps = [
        Capability(title=" ".join(b.split()[:4]) or "Capability", desc=b[:120])
        for b in (bullets[:4] or [tagline])
    ][:4]
    return OnePager(
        product=note.title[:80],
        tagline=tagline[:200],
        updated=note.date.strftime("%b %-d, %Y"),
        status_label=label,
        status=status,  # type: ignore[arg-type]
        docs_url=note.url,
        source_url=note.url,
        what_it_does=what,
        why_it_matters=why,
        capabilities=caps,
        prerequisites=[],
        use_cases=[],
        limitations=[],
        architecture=["Databricks Platform", note.category.title()],
        steps=[Step(title="Read the docs", desc="Review the linked release note.")],
        key_takeaway=tagline[:200],
    )
