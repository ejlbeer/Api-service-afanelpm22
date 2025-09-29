from flask import Blueprint, request, jsonify
from . import db
from .models import Note

bp = Blueprint("api", __name__)

@bp.get("/notes")
def list_notes():
    notes = Note.query.all()
    return jsonify([
        {"id": n.id, "title": n.title, "body": n.body,
         "created_at": n.created_at, "updated_at": n.updated_at}
        for n in notes
    ])

@bp.get("/notes/<int:note_id>")
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify({
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "created_at": note.created_at,
        "updated_at": note.updated_at
    })

@bp.post("/notes")
def create_note():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    note = Note(title=data["title"], body=data.get("body", ""))
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id, "title": note.title, "body": note.body}), 201

@bp.put("/notes/<int:note_id>")
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    note.title = data.get("title", note.title)
    note.body = data.get("body", note.body)
    db.session.commit()
    return jsonify({"id": note.id, "title": note.title, "body": note.body})

@bp.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return "", 204