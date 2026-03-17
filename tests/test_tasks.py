from datetime import date, timedelta
TODAY = str(date.today())

def test_create_task(client, auth_headers):
    res = client.post("/tasks", headers=auth_headers,
        json={"topic_id": 1, "task_date": TODAY, "planned_hours": 2.0})
    assert res.status_code == 201
    data = res.json()
    assert data["topic_id"] == 1
    assert data["task_log"] is None

def test_list_tasks_for_date(client, auth_headers):
    res = client.get(f"/tasks?task_date={TODAY}", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_log_task_completed(client, auth_headers):
    tasks = client.get(f"/tasks?task_date={TODAY}", headers=auth_headers).json()
    task_id = tasks[0]["id"]
    res = client.patch(f"/tasks/{task_id}/log", headers=auth_headers,
        json={"status": "COMPLETED", "actual_hours": 1.8})
    assert res.status_code == 200
    assert res.json()["status"] == "COMPLETED"

def test_task_log_appears_in_list(client, auth_headers):
    tasks = client.get(f"/tasks?task_date={TODAY}", headers=auth_headers).json()
    logged = [t for t in tasks if t["task_log"] is not None]
    assert len(logged) >= 1

def test_log_task_invalid_status(client, auth_headers):
    tasks = client.get(f"/tasks?task_date={TODAY}", headers=auth_headers).json()
    task_id = tasks[0]["id"]
    res = client.patch(f"/tasks/{task_id}/log", headers=auth_headers,
        json={"status": "INVALID"})
    assert res.status_code == 422

def test_wrong_exam_topic(client, auth_headers):
    res = client.post("/tasks", headers=auth_headers,
        json={"topic_id": 9999, "task_date": TODAY, "planned_hours": 1.0})
    assert res.status_code == 404
