"""Render one-pagers and the gallery to static HTML under ``site/``.

Output layout (GitHub Pages root = ``site/``):
    site/index.html                     gallery
    site/onepagers/<id>.html            console (dark) one-pager
    site/onepagers/<id>.paper.html      optional paper (light) alternate
    site/assets/ds/tokens/*.css         copied design tokens
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import Paths
from .models import OnePager

# Status -> accent color token used by badges (matches the design palette).
STATUS_COLOR = {
    "ga": "--ok-400",
    "public-preview": "--info-400",
    "gated-preview": "--info-400",
    "beta": "--warn-400",
    "changed": "--flow-400",
    "eol": "--error-400",
}


def _env(paths: Paths) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(paths.templates)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def status_color(status: str) -> str:
    return STATUS_COLOR.get(status, "--flow-400")


def copy_assets(paths: Paths) -> None:
    dst = paths.site / "assets"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(paths.assets, dst)


def render_onepager(op: OnePager, cfg: dict, paths: Paths, env: Environment) -> Path:
    """Render one one-pager (default variant + optional alternate). Returns the
    canonical HTML path."""
    tmpl = env.get_template("onepager.html.j2")
    variant = cfg["render"].get("variant", "console")
    out = paths.site_onepagers / f"{op.note_id}.html"
    out.write_text(
        tmpl.render(
            op=op,
            theme=variant,
            status_color=status_color(op.status),
            asset_prefix="../assets",
            gallery_href="../index.html",
        ),
        encoding="utf-8",
    )
    if cfg["render"].get("emit_alternate", False):
        alt = "paper" if variant == "console" else "console"
        (paths.site_onepagers / f"{op.note_id}.{alt}.html").write_text(
            tmpl.render(
                op=op,
                theme=alt,
                status_color=status_color(op.status),
                asset_prefix="../assets",
                gallery_href="../index.html",
            ),
            encoding="utf-8",
        )
    return out


def render_gallery(onepagers: list[OnePager], cfg: dict, paths: Paths, env: Environment) -> Path:
    tmpl = env.get_template("gallery.html.j2")
    items = []
    for op in onepagers:
        items.append(
            {
                "product": op.product,
                "tagline": op.tagline,
                "updated": op.updated,
                "date_iso": _sort_key(op),
                "status": op.status,
                "status_label": op.status_label,
                "status_color": status_color(op.status),
                "category": op.category,
                "href": f"onepagers/{op.note_id}.html",
            }
        )
    items.sort(key=lambda i: i["date_iso"], reverse=True)
    out = paths.site / "index.html"
    out.write_text(
        tmpl.render(
            site_title=cfg["render"].get("site_title", "Databricks Update One-Pagers"),
            generated_at=datetime.now(timezone.utc).strftime("%b %d, %Y %H:%M UTC"),
            items=items,
        ),
        encoding="utf-8",
    )
    return out


def _sort_key(op: OnePager) -> str:
    """Derive an ISO-ish sort key from note_id (which starts with the date)."""
    head = op.note_id.split("-")[:3]
    if len(head) == 3 and head[0].isdigit():
        return "-".join(head)
    return op.updated


def build_site(onepagers: list[OnePager], cfg: dict, paths: Paths) -> None:
    """Full site rebuild: assets + every one-pager + gallery."""
    paths.ensure()
    env = _env(paths)
    copy_assets(paths)
    for op in onepagers:
        render_onepager(op, cfg, paths, env)
    render_gallery(onepagers, cfg, paths, env)
