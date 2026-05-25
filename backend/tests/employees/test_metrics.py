VALID_PAYLOAD = {
    "full_name": "Alice Smith",
    "job_title": "Software Engineer",
    "department": "Engineering",
    "country": "India",
    "salary": 80000,
    "email": "alice.smith@company.com",
}


# ── GET /api/employees/metrics ────────────────────────────────────────────────

def test_metrics_returns_200(client):
    res = client.get("/api/employees/metrics")
    assert res.status_code == 200


def test_metrics_returns_zeros_when_no_employees(client):
    res = client.get("/api/employees/metrics")
    body = res.json()["data"]
    assert body["total"] == 0
    assert body["average_salary"] == 0
    assert body["min_salary"] is None
    assert body["max_salary"] is None
    assert body["by_department"] == []
    assert body["by_country"] == []


def test_metrics_overall_stats(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "salary": 120000})

    body = client.get("/api/employees/metrics").json()["data"]
    assert body["total"] == 2
    assert body["average_salary"] == 100000
    assert body["min_salary"] == 80000
    assert body["max_salary"] == 120000


def test_metrics_by_department(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "department": "Design", "salary": 60000})

    body = client.get("/api/employees/metrics").json()["data"]
    by_dept = {d["department"]: d for d in body["by_department"]}
    assert by_dept["Engineering"]["count"] == 1
    assert by_dept["Engineering"]["average_salary"] == 80000
    assert by_dept["Design"]["count"] == 1
    assert by_dept["Design"]["average_salary"] == 60000


def test_metrics_by_country(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "country": "Germany", "salary": 90000})

    body = client.get("/api/employees/metrics").json()["data"]
    by_country = {c["country"]: c for c in body["by_country"]}
    assert by_country["India"]["count"] == 1
    assert by_country["India"]["average_salary"] == 80000
    assert by_country["Germany"]["count"] == 1
    assert by_country["Germany"]["average_salary"] == 90000


def test_metrics_by_department_multiple_employees(client):
    for i in range(3):
        client.post("/api/employees", json={**VALID_PAYLOAD, "email": f"eng{i}@company.com", "salary": 60000 + i * 30000})
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "design@company.com", "department": "Design", "salary": 50000})

    body = client.get("/api/employees/metrics").json()["data"]
    by_dept = {d["department"]: d for d in body["by_department"]}
    assert by_dept["Engineering"]["count"] == 3
    assert by_dept["Engineering"]["average_salary"] == 90000
    assert by_dept["Design"]["count"] == 1


def test_metrics_by_country_includes_min_and_max_salary(client):
    client.post("/api/employees", json=VALID_PAYLOAD)                                                        # India, 80_000
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "salary": 120000})      # India, 120_000
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "charlie@company.com", "country": "Germany", "salary": 90000})

    body = client.get("/api/employees/metrics").json()["data"]
    by_country = {c["country"]: c for c in body["by_country"]}

    assert by_country["India"]["min_salary"] == 80000
    assert by_country["India"]["max_salary"] == 120000
    assert by_country["Germany"]["min_salary"] == 90000
    assert by_country["Germany"]["max_salary"] == 90000


def test_metrics_by_country_single_employee_min_equals_max(client):
    client.post("/api/employees", json=VALID_PAYLOAD)  # India, 80_000 — only employee

    body = client.get("/api/employees/metrics").json()["data"]
    by_country = {c["country"]: c for c in body["by_country"]}

    assert by_country["India"]["min_salary"] == 80000
    assert by_country["India"]["max_salary"] == 80000


def test_metrics_by_country_min_max_picks_correct_extremes(client):
    # Five India employees — min and max must be the actual outliers, not first/last inserted
    salaries = [95000, 60000, 110000, 75000, 130000]
    for i, sal in enumerate(salaries):
        client.post("/api/employees", json={**VALID_PAYLOAD, "email": f"e{i}@company.com", "salary": sal})

    body = client.get("/api/employees/metrics").json()["data"]
    by_country = {c["country"]: c for c in body["by_country"]}

    assert by_country["India"]["min_salary"] == 60000
    assert by_country["India"]["max_salary"] == 130000


def test_metrics_by_country_min_max_are_independent_per_country(client):
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "a@c.com", "country": "India", "salary": 50000})
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "b@c.com", "country": "India", "salary": 90000})
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "c@c.com", "country": "Germany", "salary": 70000})
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "d@c.com", "country": "Germany", "salary": 100000})

    body = client.get("/api/employees/metrics").json()["data"]
    by_country = {c["country"]: c for c in body["by_country"]}

    # India range must not bleed into Germany and vice-versa
    assert by_country["India"]["min_salary"] == 50000
    assert by_country["India"]["max_salary"] == 90000
    assert by_country["Germany"]["min_salary"] == 70000
    assert by_country["Germany"]["max_salary"] == 100000
