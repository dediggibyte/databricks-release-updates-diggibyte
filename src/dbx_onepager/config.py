"""Configuration loading and path resolution."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    """Repo root = two levels up from this file (src/dbx_onepager/)."""
    return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def load_config(path: str | None = None) -> dict[str, Any]:
    cfg_path = Path(path) if path else repo_root() / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class Paths:
    """Resolved absolute paths for the pipeline's directories."""

    def __init__(self, cfg: dict[str, Any]):
        root = repo_root()
        p = cfg["paths"]
        self.root = root
        self.releases = root / p["releases"]
        self.onepagers = root / p["onepagers"]
        self.docs = root / p.get("docs", "data/docs")
        self.site = root / p["site"]
        self.site_onepagers = self.site / "onepagers"
        self.fixtures = root / p["fixtures"]
        self.assets = root / "assets"
        self.templates = root / "templates"

    def ensure(self) -> None:
        for d in (self.releases, self.onepagers, self.docs, self.site, self.site_onepagers):
            d.mkdir(parents=True, exist_ok=True)
