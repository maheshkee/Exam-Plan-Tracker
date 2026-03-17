from datetime import date
TODAY = str(date.today())

def test_dashboard(client, auth_headers):
    res = client.get("/progress/dashboard", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "exam_name" in data
    assert data["pace_status"] in ("AHEAD", "ON_TRACK", "BEHIND")

def test_end_of_day(client, auth_headers):
    res = client.post(f"/progress/end-of-day?target_date={TODAY}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["day_status"] in ("COMPLETED", "PARTIAL", "MISSED")

def test_history_after_snapshot(client, auth_headers):
    res = client.get("/progress/history", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_dashboard_unauthenticated(client):
    res = client.get("/progress/dashboard")
    assert res.status_code == 401
