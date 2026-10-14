#!/usr/bin/env python3
"""Tiny CSV tracker for job applications. Standard library only.

python scripts/tracker.py add --company Acme --role "Backend dev" --link https://...
python scripts/tracker.py list [--status applied]
python scripts/tracker.py update 3 --status applied --followup-in 7
python scripts/tracker.py due
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

FIELDS = [
    "id",
    "date",
    "company",
    "role",
    "link",
    "status",
    "fit",
    "followup_date",
    "notes",
]
STATUSES = ("saved", "applied", "interviewing", "offer", "rejected", "withdrawn")
DEFAULT_FILE = Path("tracker.csv")


def load(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def add_row(rows, *, company, role, link="", status="saved", fit="", notes="", today=None):
    today = today or date.today()
    row = {
        "id": str(max((int(r["id"]) for r in rows), default=0) + 1),
        "date": today.isoformat(),
        "company": company,
        "role": role,
        "link": link,
        "status": status,
        "fit": str(fit),
        "followup_date": "",
        "notes": notes,
    }
    rows.append(row)
    return row


def update_row(rows, row_id, *, status=None, followup_in=None, notes=None, today=None):
    today = today or date.today()
    for row in rows:
        if row["id"] == str(row_id):
            if status:
                row["status"] = status
                if status == "applied" and followup_in is None and not row["followup_date"]:
                    followup_in = 7
            if followup_in is not None:
                row["followup_date"] = (today + timedelta(days=followup_in)).isoformat()
            if notes is not None:
                row["notes"] = notes
            return row
    raise KeyError(f"no application with id {row_id}")


def due_rows(rows, today=None):
    today = (today or date.today()).isoformat()
    return [
        r
        for r in rows
        if r["status"] in ("applied", "interviewing")
        and r["followup_date"]
        and r["followup_date"] <= today
    ]


def format_rows(rows) -> str:
    if not rows:
        return "(none)"
    return "\n".join(
        f"{r['id']:>3}  {r['status']:<12} fit={r['fit'] or '-':<3} {r['company']} / {r['role']}"
        + (f"  follow up {r['followup_date']}" if r["followup_date"] else "")
        for r in rows
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add")
    add.add_argument("--company", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--link", default="")
    add.add_argument("--status", choices=STATUSES, default="saved")
    add.add_argument("--fit", default="")
    add.add_argument("--notes", default="")

    lst = sub.add_parser("list")
    lst.add_argument("--status", choices=STATUSES)

    upd = sub.add_parser("update")
    upd.add_argument("id", type=int)
    upd.add_argument("--status", choices=STATUSES)
    upd.add_argument("--followup-in", type=int, metavar="DAYS")
    upd.add_argument("--notes")

    sub.add_parser("due")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = load(args.file)

    if args.command == "add":
        row = add_row(
            rows,
            company=args.company,
            role=args.role,
            link=args.link,
            status=args.status,
            fit=args.fit,
            notes=args.notes,
        )
        save(args.file, rows)
        print(f"added #{row['id']}: {row['company']} / {row['role']}")
    elif args.command == "list":
        selected = [r for r in rows if not args.status or r["status"] == args.status]
        print(format_rows(selected))
    elif args.command == "update":
        try:
            row = update_row(
                rows,
                args.id,
                status=args.status,
                followup_in=args.followup_in,
                notes=args.notes,
            )
        except KeyError as error:
            print(error, file=sys.stderr)
            return 1
        save(args.file, rows)
        print(f"updated #{row['id']}: {row['status']}")
    elif args.command == "due":
        print(format_rows(due_rows(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
