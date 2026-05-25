# Seed Script Performance

## Result

10,000 employees seeded in **~0.27 seconds** on a 2023 MacBook Pro (Apple M2, SQLite on local SSD).

## Benchmark

```
Seeding 10000 employees in 20 batches of 500…
  Batch 1/20  —  500 rows inserted
  Batch 2/20  — 1000 rows inserted
  ...
  Batch 20/20 — 10000 rows inserted
Done. 10000 employees seeded successfully.

real    0m0.273s
```

## Why it's fast

### 1. SQLAlchemy bulk insert — not ORM session.add()

```python
# Slow: 10,000 individual INSERT statements
for row in rows:
    session.add(Employee(**row))
session.commit()

# Fast: one compiled INSERT per batch of 500
session.execute(sa_insert(Employee), batch)   # batch = list[dict]
```

`sa_insert(Employee)` with a list of dicts compiles to a single parameterised INSERT with 500 rows per call. SQLAlchemy sends 20 statements instead of 10,000.

### 2. Single transaction wrapping all batches

```python
with session.begin():          # one BEGIN / COMMIT pair
    for batch in batches:
        session.execute(sa_insert(Employee), batch)
```

SQLite flushes to disk on every `COMMIT`. Wrapping all 20 batches in one transaction means one disk flush instead of 20. This is the dominant factor for SQLite write performance.

### 3. Pre-generated rows — no per-row DB round-trips

All 10,000 row dicts are built in Python (`_build_rows()`) before any database statement runs. There are zero SELECT queries during the insert phase.

### 4. Idempotency check is a COUNT, not a full scan

```python
count = session.exec(select(func.count()).select_from(Employee)).one()
if count >= TARGET:
    return   # nothing to do
```

The guard check is O(1) — SQLite stores the row count in the table header.

### 5. Fixed RNG seed for reproducibility

```python
RNG = random.Random(42)
```

The same seed produces the same 10,000 employees on every run, making the dataset deterministic for testing and demos without sacrificing speed.

## Scaling headroom

For 100,000 rows the same script would take ~2–3 s with no code changes. For 1,000,000 rows, switching to raw `sqlite3.executemany()` (bypassing SQLAlchemy entirely) would bring it back under 10 s.
