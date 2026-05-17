"""Smoke tests for the scanner + starter catalog."""

from pathlib import Path

from leakguard.catalog import load_starter_catalog
from leakguard.scanner import scan_paths


FIXTURES = Path(__file__).parent / "fixtures"


def test_starter_catalog_loads_with_expected_classes():
    classes = load_starter_catalog()
    ids = {c["id"] for c in classes}
    expected = {
        "cross-project-codenames",
        "operator-paths",
        "private-wrapper-services",
        "phase-numbering",
        "handoff-doc-names",
        "agent-memory-ids",
        "time-of-day-narration",
        "user-pushback",
        "agent-actor-references",
        "session-restart-narration",
        "session-state-framing",
        "strategic-process-framing",
    }
    assert expected.issubset(ids)


def test_clean_file_has_no_findings():
    classes = load_starter_catalog()
    findings = scan_paths([FIXTURES / "clean.md"], classes)
    assert findings == [], f"clean fixture leaked: {findings}"


def test_leaky_file_flags_multiple_classes():
    classes = load_starter_catalog()
    findings = scan_paths([FIXTURES / "leaky.md"], classes)
    ids = {f.class_id for f in findings}
    assert "phase-numbering" in ids
    assert "session-state-framing" in ids
    assert "agent-memory-ids" in ids
    assert "time-of-day-narration" in ids
    assert "user-pushback" in ids
    assert "handoff-doc-names" in ids


def test_scan_returns_line_numbers():
    classes = load_starter_catalog()
    findings = scan_paths([FIXTURES / "leaky.md"], classes)
    assert all(f.line_no > 0 for f in findings)
    assert all(isinstance(f.line, str) for f in findings)
