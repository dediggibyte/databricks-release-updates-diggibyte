"""Command-line entrypoint.

Examples:
    # Weekly incremental (the scheduled job): fetch new notes, enrich, rebuild.
    python -m dbx_onepager weekly

    # Backfill historical notes for a month range, then rebuild.
    python -m dbx_onepager backfill --from 2025-01 --to 2025-12

    # Offline demo/test over fixtures (no network, no API key needed).
    python -m dbx_onepager fixtures --mock

    # Re-enrich anything pending / rebuild the static site only.
    python -m dbx_onepager enrich
    python -m dbx_onepager build

Global flags:
    --mock    Skip the LLM; build one-pagers with the offline heuristic.
    --model   Override the model id (e.g. claude-opus-4-8) for this run.
    --config  Path to a config.yaml (defaults to repo root).
"""

from __future__ import annotations

import argparse
import sys
from datetime import date

from . import pipeline


def _parse_month(value: str) -> date:
    """Parse 'YYYY-MM' (or 'YYYY-MM-DD') into a date on the 1st of the month."""
    parts = value.split("-")
    if len(parts) < 2:
        raise argparse.ArgumentTypeError(f"expected YYYY-MM, got {value!r}")
    year, month = int(parts[0]), int(parts[1])
    return date(year, month, 1)


def build_parser() -> argparse.ArgumentParser:
    # Common flags usable either before OR after the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=None, help="Path to config.yaml")
    common.add_argument("--model", default=None, help="Override LLM model id")
    common.add_argument("--mock", action="store_true", help="Use offline heuristic, no LLM")

    p = argparse.ArgumentParser(prog="dbx_onepager", description=__doc__, parents=[common])
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("weekly", parents=[common],
                   help="Fetch new notes via RSS, enrich, rebuild site")

    bf = sub.add_parser("backfill", parents=[common],
                        help="Backfill historical notes by month range")
    bf.add_argument("--from", dest="start", required=True, type=_parse_month,
                    help="Start month YYYY-MM")
    bf.add_argument("--to", dest="end", required=True, type=_parse_month,
                    help="End month YYYY-MM (inclusive)")

    sub.add_parser("fixtures", parents=[common], help="Run offline over fixtures/ (dev + CI)")
    sub.add_parser("enrich", parents=[common], help="Enrich all pending notes, rebuild site")
    sub.add_parser("build", parents=[common], help="Rebuild the static site from existing data")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cmd = args.command
    if cmd == "weekly":
        pipeline.run_weekly(args.config, args.model, args.mock)
    elif cmd == "backfill":
        pipeline.run_backfill(args.config, args.start, args.end, args.model, args.mock)
    elif cmd == "fixtures":
        pipeline.run_fixtures(args.config, args.model, args.mock)
    elif cmd == "enrich":
        pipeline.run_enrich(args.config, args.model, args.mock)
    elif cmd == "build":
        pipeline.run_build(args.config)
    else:  # pragma: no cover - argparse enforces
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
