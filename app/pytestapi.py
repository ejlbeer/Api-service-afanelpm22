import json

def test_create_note(client):
    response = client.post("/api/notes", json={
        "title": "Test note",
        "body": "Hello world"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

def test_list_notes(client):
    response = client.get("/api/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
