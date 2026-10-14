import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import tracker  # noqa: E402

TODAY = date(2026, 10, 14)


def test_add_assigns_incrementing_ids():
    rows = []
    a = tracker.add_row(rows, company="A", role="x", today=TODAY)
    b = tracker.add_row(rows, company="B", role="y", today=TODAY)
    assert (a["id"], b["id"]) == ("1", "2")
    assert a["date"] == "2026-10-14"


def test_applied_sets_default_followup_of_seven_days():
    rows = []
    tracker.add_row(rows, company="A", role="x", today=TODAY)
    row = tracker.update_row(rows, 1, status="applied", today=TODAY)
    assert row["followup_date"] == "2026-10-21"


def test_explicit_followup_overrides_default():
    rows = []
    tracker.add_row(rows, company="A", role="x", today=TODAY)
    row = tracker.update_row(rows, 1, status="applied", followup_in=3, today=TODAY)
    assert row["followup_date"] == "2026-10-17"


def test_update_unknown_id_raises():
    try:
        tracker.update_row([], 9)
    except KeyError:
        return
    raise AssertionError("expected KeyError")


def test_due_only_lists_applied_and_overdue():
    rows = []
    for company in "ABCD":
        tracker.add_row(rows, company=company, role="r", today=TODAY)
    tracker.update_row(rows, 1, status="applied", followup_in=0, today=TODAY)  # due today
    tracker.update_row(rows, 2, status="applied", followup_in=5, today=TODAY)  # future
    tracker.update_row(rows, 3, status="rejected", followup_in=0, today=TODAY)  # closed
    due = tracker.due_rows(rows, today=TODAY)
    assert [r["company"] for r in due] == ["A"]


def test_csv_round_trip_and_cli(tmp_path, capsys):
    file = tmp_path / "t.csv"
    assert (
        tracker.main(["--file", str(file), "add", "--company", "Acme", "--role", "Dev, Backend"])
        == 0
    )
    assert tracker.main(["--file", str(file), "update", "1", "--status", "applied"]) == 0
    assert tracker.main(["--file", str(file), "list", "--status", "applied"]) == 0
    out = capsys.readouterr().out
    assert "Acme / Dev, Backend" in out
    assert tracker.load(file)[0]["role"] == "Dev, Backend"


def test_cli_update_missing_id_returns_error(tmp_path, capsys):
    assert (
        tracker.main(["--file", str(tmp_path / "t.csv"), "update", "5", "--status", "offer"]) == 1
    )
    assert "no application" in capsys.readouterr().err
