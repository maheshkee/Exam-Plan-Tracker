def test_list_exams(client, seeded_db):
    res = client.get("/exams")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_get_exam_detail(client, seeded_db):
    res = client.get("/exams/1")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "GATE CS"
    assert len(data["subjects"]) >= 1

def test_get_exam_not_found(client):
    res = client.get("/exams/9999")
    assert res.status_code == 404

def test_enroll_success(client, auth_headers, seeded_db):
    res = client.post("/exams/enroll", headers=auth_headers,
        json={"exam_id": 1, "exam_date": "2027-01-01", "study_hours_per_day": 4.0})
    assert res.status_code == 201
    data = res.json()
    assert data["exam_id"] == 1
    assert data["days_remaining"] > 0
    assert data["total_syllabus_hours"] > 0

def test_enroll_duplicate(client, auth_headers):
    res = client.post("/exams/enroll", headers=auth_headers,
        json={"exam_id": 1, "exam_date": "2027-01-01", "study_hours_per_day": 3.0})
    assert res.status_code == 400

def test_my_enrollment(client, auth_headers):
    res = client.get("/exams/my-enrollment", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["exam_id"] == 1

def test_enroll_past_date(client, seeded_db):
    client.post("/auth/register", json={"email": "user2@test.com", "password": "password123"})
    res2 = client.post("/auth/login", json={"email": "user2@test.com", "password": "password123"})
    h2 = {"Authorization": f"Bearer {res2.json()['access_token']}"}
    res = client.post("/exams/enroll", headers=h2,
        json={"exam_id": 1, "exam_date": "2020-01-01", "study_hours_per_day": 4.0})
    assert res.status_code == 422
