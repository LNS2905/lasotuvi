from fastapi.testclient import TestClient

from lasotuvi.api.main import app


client = TestClient(app)


def test_create_and_fetch_chart():
    payload = {
        "day": 24,
        "month": 10,
        "year": 1991,
        "hour_branch": 7,
        "gender": 1,
        "name": "Test",
        "solar_calendar": True,
        "timezone": 7,
    }
    create_response = client.post("/charts", json=payload)
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["id"] is not None
    chart_id = created["id"]

    get_response = client.get(f"/charts/{chart_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == chart_id
    assert fetched["request"]["name"] == "Test"
