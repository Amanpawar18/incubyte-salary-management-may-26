VALID_PAYLOAD = {
    "full_name": "Alice Smith",
    "job_title": "Software Engineer",
    "department": "Engineering",
    "country": "India",
    "salary": 80000,
    "email": "alice.smith@company.com",
}


def test_create_employee_returns_201(client):
    res = client.post("/api/employees", json=VALID_PAYLOAD)
    assert res.status_code == 201
    body = res.json()["data"]
    assert body["id"] is not None
    assert body["full_name"] == "Alice Smith"
    assert body["salary"] == 80000


def test_create_employee_returns_422_when_full_name_empty(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "full_name": ""})
    assert res.status_code == 422


def test_create_employee_returns_422_when_full_name_whitespace(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "full_name": "   "})
    assert res.status_code == 422


def test_create_employee_returns_422_when_salary_negative(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "salary": -100})
    assert res.status_code == 422


def test_create_employee_returns_422_when_salary_zero(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "salary": 0})
    assert res.status_code == 422


def test_create_employee_returns_422_when_email_invalid(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "email": "not-an-email"})
    assert res.status_code == 422


def test_create_employee_returns_422_when_required_field_missing(client):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "job_title"}
    res = client.post("/api/employees", json=payload)
    assert res.status_code == 422


def test_create_employee_returns_409_when_email_duplicate(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    res = client.post("/api/employees", json=VALID_PAYLOAD)
    assert res.status_code == 409


# ── GET /api/employees ────────────────────────────────────────────────────────

def test_list_employees_returns_empty_page(client):
    res = client.get("/api/employees")
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["items"] == []
    assert body["total"] == 0
    assert body["page"] == 1
    assert body["page_size"] == 20


def test_list_employees_returns_created_employees(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "full_name": "Bob Jones"})

    res = client.get("/api/employees")
    assert res.status_code == 200
    assert res.json()["data"]["total"] == 2


def test_list_employees_pagination(client):
    for i in range(5):
        client.post("/api/employees", json={**VALID_PAYLOAD, "email": f"user{i}@company.com"})

    res = client.get("/api/employees?page=1&page_size=3")
    body = res.json()["data"]
    assert len(body["items"]) == 3
    assert body["total"] == 5


def test_list_employees_search_by_name(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "full_name": "Bob Jones", "email": "bob@company.com"})

    res = client.get("/api/employees?name=Alice")
    assert res.json()["data"]["total"] == 1
    assert res.json()["data"]["items"][0]["full_name"] == "Alice Smith"


def test_list_employees_filter_by_country(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    client.post("/api/employees", json={**VALID_PAYLOAD, "country": "Germany", "email": "bob@company.com"})

    res = client.get("/api/employees?country=India")
    assert res.json()["data"]["total"] == 1
