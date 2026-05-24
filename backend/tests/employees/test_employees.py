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
