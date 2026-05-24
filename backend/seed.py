"""
Seed 10,000 employees generated from first_names.txt x last_names.txt.
Inserts in batches within a single transaction — atomic: all succeed or all roll back.
Safe to run multiple times — skips if already seeded.
"""

import random
from pathlib import Path
from sqlalchemy import insert as sa_insert, func
from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import Employee

TARGET = 10_000
BATCH_SIZE = 500
RNG = random.Random(42)  # fixed seed → reproducible data

DEPARTMENTS: list[tuple[str, list[str], tuple[int, int]]] = [
    ("Engineering",  ["Software Engineer", "Senior Software Engineer", "Staff Engineer", "Engineering Manager"], (70_000, 160_000)),
    ("Design",       ["UI Designer", "UX Designer", "Senior Product Designer", "Design Lead"],                  (65_000, 130_000)),
    ("Product",      ["Associate Product Manager", "Product Manager", "Senior Product Manager"],                 (75_000, 155_000)),
    ("Marketing",    ["Growth Marketer", "Content Strategist", "Marketing Manager", "Brand Designer"],          (55_000, 115_000)),
    ("HR",           ["HR Coordinator", "HR Business Partner", "Talent Acquisition Specialist", "HR Manager"],  (50_000, 100_000)),
    ("Finance",      ["Financial Analyst", "Senior Accountant", "Finance Manager", "Controller"],               (65_000, 135_000)),
    ("Sales",        ["Sales Development Rep", "Account Executive", "Senior Account Executive", "Sales Manager"],(55_000, 145_000)),
    ("Operations",   ["Operations Analyst", "Operations Manager", "Business Analyst", "COO"],                   (60_000, 140_000)),
]

COUNTRIES = [
    "India", "United States", "Germany", "United Kingdom", "Brazil",
    "Canada", "France", "Japan", "Australia", "Netherlands",
    "Spain", "Poland", "Mexico", "South Korea", "Sweden",
    "Nigeria", "South Africa", "Argentina", "Portugal", "Denmark",
]


def _load_names() -> tuple[list[str], list[str]]:
    base = Path(__file__).parent
    first = (base / "first_names.txt").read_text().split()
    last = (base / "last_names.txt").read_text().split()
    return first, last


def _build_rows(first_names: list[str], last_names: list[str]) -> list[dict]:
    rows: list[dict] = []
    dept_cycle = 0

    for first in first_names:
        for last in last_names:
            dept, titles, (sal_min, sal_max) = DEPARTMENTS[dept_cycle % len(DEPARTMENTS)]
            dept_cycle += 1

            rows.append({
                "full_name": f"{first} {last}",
                "email": f"{first.lower()}.{last.lower()}@company.com",
                "job_title": RNG.choice(titles),
                "department": dept,
                "country": RNG.choice(COUNTRIES),
                "salary": float(RNG.randint(sal_min, sal_max)),
            })

    return rows


def seed() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        count: int = session.exec(select(func.count()).select_from(Employee)).one()
        if count >= TARGET:
            print(f"Already seeded ({count} employees) — nothing to do.")
            return

        if count > 0:
            print(f"Found {count} existing employees — clearing before re-seed.")
            session.exec(Employee.__table__.delete())  # type: ignore[attr-defined]
            session.commit()

    first_names, last_names = _load_names()
    rows = _build_rows(first_names, last_names)
    total_batches = (len(rows) + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Seeding {len(rows)} employees in {total_batches} batches of {BATCH_SIZE}…")

    try:
        with Session(engine) as session:
            with session.begin():  # single transaction — rolls back all batches on any failure
                for batch_num, offset in enumerate(range(0, len(rows), BATCH_SIZE), start=1):
                    batch = rows[offset : offset + BATCH_SIZE]
                    session.execute(sa_insert(Employee), batch)
                    print(f"  Batch {batch_num}/{total_batches} — {offset + len(batch)} rows inserted")
    except Exception as exc:
        print(f"Seed failed — transaction rolled back. Reason: {exc}")
        raise

    print(f"Done. {len(rows)} employees seeded successfully.")


if __name__ == "__main__":
    seed()
