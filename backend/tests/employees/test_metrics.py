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
