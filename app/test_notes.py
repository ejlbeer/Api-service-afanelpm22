import pytest
from app import create_app, db
from app.models import Note

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            note1 = Note(title="Note 1", body="Body 1")
            note2 = Note(title="Note 2", body="Body 2")
            db.session.add_all([note1, note2])
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

def test_list_notes(client):
    response = client.get("/api/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_create_note(client):
    response = client.post("/api/notes", json={
        "title": "New Note",
        "body": "Hello world"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "New Note"


def test_update_note(client):
    response = client.put("/api/notes/1", json={
        "title": "Updated Title",
        "body": "Updated Body"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"


def test_delete_note(client):
    response = client.delete("/api/notes/1")
    assert response.status_code == 204
    check = client.get("/api/notes/1")
    assert check.status_code == 404