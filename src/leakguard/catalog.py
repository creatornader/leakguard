"""Catalog loading: read YAML, optionally merge a user override."""

from importlib import resources
from pathlib import Path

import yaml


def load_starter_catalog() -> list:
    """Load the catalog shipped with leakguard."""
    text = resources.files("leakguard.data").joinpath("starter-catalog.yaml").read_text()
    return _parse(text)


def load_catalog(path: Path) -> list:
    """Load a catalog from a user-supplied file."""
    return _parse(path.read_text())


def load_with_overrides(user_path: Path | None) -> list:
    """Load starter catalog and merge a user catalog on top (user wins by `id`)."""
    classes = load_starter_catalog()
    if user_path is None or not user_path.exists():
        return classes
    user_classes = load_catalog(user_path)
    return _merge(classes, user_classes)


def _parse(text: str) -> list:
    data = yaml.safe_load(text) or {}
    classes = data.get("classes", [])
    if not isinstance(classes, list):
        raise ValueError("catalog `classes` must be a list")
    for cls in classes:
        if "id" not in cls or "name" not in cls:
            raise ValueError(f"catalog class missing required field: {cls!r}")
        cls.setdefault("patterns", [])
        cls.setdefault("case_sensitive", False)
    return classes


def _merge(base: list, override: list) -> list:
    by_id = {c["id"]: c for c in base}
    for c in override:
        existing = by_id.get(c["id"])
        if existing is None:
            by_id[c["id"]] = c
            continue
        # Merge: override patterns extend by default; replace if user sets `replace: true`
        if c.get("replace"):
            by_id[c["id"]] = c
        else:
            merged_patterns = list(dict.fromkeys(existing["patterns"] + c.get("patterns", [])))
            by_id[c["id"]] = {**existing, **{k: v for k, v in c.items() if k != "patterns"}, "patterns": merged_patterns}
    return list(by_id.values())
