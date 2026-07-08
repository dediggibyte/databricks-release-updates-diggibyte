"""Smoke tests that exercise the offline path end-to-end (no network/API)."""

from datetime import date

from dbx_onepager.enrich import enrich_note
from dbx_onepager.fetch import detect_status
from dbx_onepager.models import OnePager, ReleaseNote


def _note(**kw) -> ReleaseNote:
    base = dict(
        id="2026-06-16-x",
        title="Feature X is now generally available",
        date=date(2026, 6, 16),
        url="https://example.com",
        body="Feature X is now generally available. It does a useful thing.",
    )
    base.update(kw)
    return ReleaseNote(**base)


def test_status_detection_handles_wrapped_phrases():
    assert detect_status("now in Public\nPreview")[0] == "public-preview"
    assert detect_status("is generally available")[0] == "ga"
    assert detect_status("nothing notable here")[0] == "changed"


def test_make_id_is_stable_and_dated():
    a = ReleaseNote.make_id(date(2026, 6, 16), "Feature X!")
    b = ReleaseNote.make_id(date(2026, 6, 16), "Feature X!")
    assert a == b
    assert a.startswith("2026-06-16-")


def test_heuristic_enrichment_produces_valid_onepager():
    cfg = {"llm": {}, "source": {}}
    op = enrich_note(_note(), cfg, mock=True)
    assert isinstance(op, OnePager)
    assert op.product
    assert op.what_it_does
    assert op.key_takeaway
    assert op.status == "ga"
    assert op.note_id == "2026-06-16-x"          # linkage set from the record
    assert op.source_url == "https://example.com"


def test_llm_schema_drops_linkage_fields():
    schema = OnePager.json_schema_for_llm()
    assert "note_id" not in schema["properties"]
    assert "category" not in schema["properties"]
    assert "product" in schema["required"]
