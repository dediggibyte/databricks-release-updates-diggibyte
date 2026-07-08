# Databricks Update One-Pager

Automatically turn **Databricks release notes** into executive **one-pagers** —
each explaining an update *technically* (what changed, prerequisites,
limitations) and from a *business perspective* (why it matters, use cases).

Runs **weekly (every Tuesday)** to catch new releases, and can **backfill any
past release notes** on demand. Output is a browsable, filterable static
gallery published to GitHub Pages.

The one-pager design is a faithful port of the "Databricks Update One-Pager"
Datalab design (dark *console* variant by default, light *paper* variant as an
alternate/print view).

![One-pager + gallery](docs/preview.png)

---

## How it works

```
fetch  →  store  →  enrich (Claude)  →  render  →  gallery
```

| Stage | Module | What it does |
|-------|--------|--------------|
| **fetch**  | `fetch.py`   | Pulls release notes. Weekly = the release-notes **RSS feed**; backfill = walks **monthly archive** pages. Uses headless **Chromium/Playwright** (Databricks docs block plain bots), with a urllib fallback and offline fixtures. |
| **store**  | `store.py`   | Durable JSON per note, **deduped by id**. Keeps full history so any past note is always re-generatable. |
| **enrich** | `enrich.py`  | Sends each note to **Claude**, which returns the structured one-pager contract via a forced tool call. Falls back to an offline heuristic when no API key is set. |
| **render** | `render.py`  | Fills the Jinja2 template with the Datalab design tokens → one self-contained HTML page per note. |
| **gallery**| `render.py`  | Builds `index.html`: a searchable, filterable card grid of every update. |

The one-pager **content contract** lives in `models.py` (`OnePager`). That single
Pydantic model drives the Claude tool schema *and* the template, so they can
never drift apart.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m playwright install chromium          # only needed for live fetch

# Offline demo over sample notes in fixtures/ (no network, no API key):
python -m dbx_onepager fixtures --mock
open site/index.html
```

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...

# Weekly incremental — the scheduled job. Fetch new notes, enrich, rebuild.
python -m dbx_onepager weekly

# Backfill past release notes for a month range (on-demand).
python -m dbx_onepager backfill --from 2025-01 --to 2025-12

# Re-enrich anything pending / rebuild the static site only.
python -m dbx_onepager enrich
python -m dbx_onepager build
```

Global flags (usable before or after the subcommand):

| Flag | Meaning |
|------|---------|
| `--mock`  | Skip the LLM; build one-pagers with the offline heuristic. |
| `--model` | Override the model id for the run (e.g. `claude-opus-4-8`). |
| `--config`| Path to an alternate `config.yaml`. |

## Configuration

Everything retargetable lives in [`config.yaml`](config.yaml): the source
(cloud, RSS/archive URLs), the LLM model, and rendering options (default
variant, whether to emit the alternate theme, site title). No code changes
needed to switch cloud or model.

## Scheduling & publishing (GitHub Actions + Pages)

[`.github/workflows/weekly.yml`](.github/workflows/weekly.yml):

* **`schedule`** — cron `0 7 * * 2` runs `weekly` every Tuesday 07:00 UTC.
* **`workflow_dispatch`** — manual runs with a `mode` (`weekly`/`backfill`),
  `from_month`/`to_month`, and optional `model` — this is the **on-demand past
  release-note** path.
* Generated `data/` and `site/` are committed back, and `site/` is deployed to
  **GitHub Pages**.

**Setup:** add `ANTHROPIC_API_KEY` as a repository secret, and enable Pages
(Settings → Pages → Source: GitHub Actions).

## Layout

```
config.yaml                 source / model / render settings
assets/ds/tokens/*.css      Datalab design tokens (ported from the design)
templates/                  onepager.html.j2, gallery.html.j2
src/dbx_onepager/           fetch · store · enrich · render · pipeline · cli
fixtures/                   sample release notes for offline runs/tests
data/releases/              raw normalized notes (source of truth, git-tracked)
data/onepagers/             enriched one-pager JSON
site/                       rendered HTML (GitHub Pages root)
.github/workflows/weekly.yml
```

## Extending

* **Other release-note streams** (Runtime, SQL, Azure/GCP): point `config.yaml`
  at a different feed/archive, or run multiple configs.
* **Design tweaks**: edit `templates/onepager.html.j2`; tokens live in
  `assets/ds/tokens/`.
* **Model quality vs cost**: default `claude-sonnet-5` for the batch; pass
  `--model claude-opus-4-8` for high-value notes.
