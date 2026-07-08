"""Databricks Update One-Pager generator.

A weekly pipeline that reads Databricks release notes, understands each one
technically and from a business perspective via Claude, and renders a
one-pager (matching the Datalab design) per release note.

Stages: fetch -> store -> enrich -> render -> gallery.
"""

__version__ = "0.1.0"
