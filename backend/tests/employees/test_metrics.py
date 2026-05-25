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


# ── GET /api/employees/metrics/job-title ──────────────────────────────────────

def test_job_title_metrics_returns_200(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    res = client.get("/api/employees/metrics/job-title?job_title=Software Engineer&country=India")
    assert res.status_code == 200


def test_job_title_metrics_returns_count_and_average(client):
    client.post("/api/employees", json=VALID_PAYLOAD)                                                    # 80_000
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "salary": 100000}) # 100_000

    body = client.get("/api/employees/metrics/job-title?job_title=Software Engineer&country=India").json()["data"]
    assert body["job_title"] == "Software Engineer"
    assert body["country"] == "India"
    assert body["count"] == 2
    assert body["average_salary"] == 90000


def test_job_title_metrics_returns_404_when_no_match(client):
    res = client.get("/api/employees/metrics/job-title?job_title=CEO&country=Mars")
    assert res.status_code == 404


def test_job_title_metrics_is_case_insensitive(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    res = client.get("/api/employees/metrics/job-title?job_title=software engineer&country=india")
    assert res.status_code == 200
    assert res.json()["data"]["count"] == 1


def test_job_title_metrics_excludes_other_countries(client):
    client.post("/api/employees", json=VALID_PAYLOAD)                                                             # India
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "country": "Germany"})      # Germany — same job title

    body = client.get("/api/employees/metrics/job-title?job_title=Software Engineer&country=India").json()["data"]
    assert body["count"] == 1  # only the India employee


def test_job_title_metrics_excludes_other_job_titles(client):
    client.post("/api/employees", json=VALID_PAYLOAD)                                                             # Software Engineer
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "job_title": "Designer"})   # different title

    body = client.get("/api/employees/metrics/job-title?job_title=Software Engineer&country=India").json()["data"]
    assert body["count"] == 1  # only the Software Engineer


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
