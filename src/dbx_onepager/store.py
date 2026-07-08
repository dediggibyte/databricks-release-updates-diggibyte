"""Durable JSON store for release notes and generated one-pagers.

Design goals:
* Dedup by ``ReleaseNote.id`` so weekly runs only process genuinely new notes.
* Keep the full history on disk so *any* past note can be (re)generated later.
* Plain JSON files (git-friendly, diffable, no database to operate).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .config import Paths
from .models import OnePager, ReleaseNote


class Store:
    def __init__(self, paths: Paths):
        self.paths = paths
        self.paths.ensure()

    # -- release notes ----------------------------------------------------
    def _note_path(self, note_id: str) -> Path:
        return self.paths.releases / f"{note_id}.json"

    def has_note(self, note_id: str) -> bool:
        return self._note_path(note_id).exists()

    def save_note(self, note: ReleaseNote) -> None:
        self._note_path(note.id).write_text(
            note.model_dump_json(indent=2), encoding="utf-8"
        )

    def add_notes(self, notes: Iterable[ReleaseNote]) -> list[ReleaseNote]:
        """Persist notes that are not already stored. Returns the new ones."""
        new: list[ReleaseNote] = []
        for note in notes:
            if not self.has_note(note.id):
                self.save_note(note)
                new.append(note)
        return new

    def get_note(self, note_id: str) -> Optional[ReleaseNote]:
        path = self._note_path(note_id)
        if not path.exists():
            return None
        return ReleaseNote.model_validate_json(path.read_text(encoding="utf-8"))

    def all_notes(self) -> list[ReleaseNote]:
        notes = [
            ReleaseNote.model_validate_json(p.read_text(encoding="utf-8"))
            for p in self.paths.releases.glob("*.json")
        ]
        return sorted(notes, key=lambda n: (n.date, n.title), reverse=True)

    # -- one-pagers -------------------------------------------------------
    def _onepager_path(self, note_id: str) -> Path:
        return self.paths.onepagers / f"{note_id}.json"

    def has_onepager(self, note_id: str) -> bool:
        return self._onepager_path(note_id).exists()

    def save_onepager(self, op: OnePager) -> None:
        self._onepager_path(op.note_id).write_text(
            op.model_dump_json(indent=2), encoding="utf-8"
        )

    def get_onepager(self, note_id: str) -> Optional[OnePager]:
        path = self._onepager_path(note_id)
        if not path.exists():
            return None
        return OnePager.model_validate_json(path.read_text(encoding="utf-8"))

    def all_onepagers(self) -> list[OnePager]:
        return [
            OnePager.model_validate_json(p.read_text(encoding="utf-8"))
            for p in self.paths.onepagers.glob("*.json")
        ]

    def notes_needing_enrichment(self) -> list[ReleaseNote]:
        return [n for n in self.all_notes() if not self.has_onepager(n.id)]
