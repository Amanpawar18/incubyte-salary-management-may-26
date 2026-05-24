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


def test_create_employee_returns_422_when_job_title_blank(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "job_title": "   "})
    assert res.status_code == 422


def test_create_employee_returns_422_when_department_blank(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "department": ""})
    assert res.status_code == 422


def test_create_employee_returns_422_when_country_blank(client):
    res = client.post("/api/employees", json={**VALID_PAYLOAD, "country": "   "})
    assert res.status_code == 422


def test_create_employee_returns_201_with_all_fields(client):
    res = client.post("/api/employees", json=VALID_PAYLOAD)
    assert res.status_code == 201
    body = res.json()["data"]
    assert body["job_title"] == VALID_PAYLOAD["job_title"]
    assert body["department"] == VALID_PAYLOAD["department"]
    assert body["country"] == VALID_PAYLOAD["country"]
    assert body["email"] == VALID_PAYLOAD["email"]
    assert "created_at" in body
    assert "updated_at" in body


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


# ── GET /api/employees/{id} ───────────────────────────────────────────────────

def test_get_employee_by_id_returns_200(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.get(f"/api/employees/{created['id']}")
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["id"] == created["id"]
    assert body["full_name"] == "Alice Smith"


def test_get_employee_by_id_returns_404_when_not_found(client):
    res = client.get("/api/employees/9999")
    assert res.status_code == 404


# ── PUT /api/employees/{id} ───────────────────────────────────────────────────

def test_update_employee_returns_200(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "salary": 95000})
    assert res.status_code == 200
    assert res.json()["data"]["salary"] == 95000


def test_update_employee_returns_404_when_not_found(client):
    res = client.put("/api/employees/9999", json=VALID_PAYLOAD)
    assert res.status_code == 404


def test_update_employee_returns_422_when_salary_invalid(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "salary": -500})
    assert res.status_code == 422


def test_update_employee_returns_409_when_email_taken(client):
    client.post("/api/employees", json=VALID_PAYLOAD)
    other = client.post("/api/employees", json={**VALID_PAYLOAD, "email": "bob@company.com", "full_name": "Bob"}).json()["data"]
    res = client.put(f"/api/employees/{other['id']}", json={**VALID_PAYLOAD, "email": VALID_PAYLOAD["email"]})
    assert res.status_code == 409


def test_update_employee_allows_keeping_own_email(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "salary": 90000})
    assert res.status_code == 200


def test_update_employee_returns_422_when_full_name_blank(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "full_name": "   "})
    assert res.status_code == 422


def test_update_employee_returns_422_when_salary_zero(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "salary": 0})
    assert res.status_code == 422


def test_update_employee_returns_422_when_email_invalid(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.put(f"/api/employees/{created['id']}", json={**VALID_PAYLOAD, "email": "bad-email"})
    assert res.status_code == 422


# ── DELETE /api/employees/{id} ───────────────────────────────────────────────

def test_delete_employee_returns_204(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    res = client.delete(f"/api/employees/{created['id']}")
    assert res.status_code == 204


def test_delete_employee_removes_employee_from_list(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    client.delete(f"/api/employees/{created['id']}")
    res = client.get("/api/employees")
    assert res.json()["data"]["total"] == 0


def test_delete_employee_returns_404_when_not_found(client):
    res = client.delete("/api/employees/9999")
    assert res.status_code == 404


def test_delete_employee_makes_id_unreachable(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    client.delete(f"/api/employees/{created['id']}")
    res = client.get(f"/api/employees/{created['id']}")
    assert res.status_code == 404


def test_update_employee_returns_200_with_all_updated_fields(client):
    created = client.post("/api/employees", json=VALID_PAYLOAD).json()["data"]
    updated_payload = {
        "full_name": "Alice Updated",
        "job_title": "Senior Engineer",
        "department": "Platform",
        "country": "Germany",
        "salary": 120000,
        "email": "alice.updated@company.com",
    }
    res = client.put(f"/api/employees/{created['id']}", json=updated_payload)
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["full_name"] == "Alice Updated"
    assert body["job_title"] == "Senior Engineer"
    assert body["department"] == "Platform"
    assert body["country"] == "Germany"
    assert body["salary"] == 120000
    assert body["email"] == "alice.updated@company.com"
