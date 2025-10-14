from flask import Blueprint, request, jsonify
from . import db
from .models import Note
from .models import Book

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

#------------------------------------------------------------------

@bp.get("/books")
def list_books():
    title_filter = request.args.get("title") 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 5, type=int)
    query = Book.query
    if title_filter:
        query = query.filter(Book.title.ilike(f"%{title_filter}%"))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = [
        {
            "id": b.id,
            "title": b.title,
            "body": b.body,
            "created_at": b.created_at,
            "updated_at": b.updated_at
        }
        for b in pagination.items
    ]
    return jsonify({
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
        "notes": books
    })

@bp.post("/books")
def create_book():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"Ошибка": "Нужно добавить название"}), 400
    book = Book(title=data["title"], body=data.get("body", ""))
    db.session.add(book)
    db.session.commit()
    return jsonify({
        "id": book.id,
        "title": book.title,
        "body": book.body
    }), 201

@bp.get("/books/<int:book_id>")
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "body": book.body,
        "created_at": book.created_at,
        "updated_at": book.updated_at
    })

@bp.put("/books/<int:book_id>")
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.body = data.get("body", book.body)
    db.session.commit()
    return jsonify({
        "id": book.id,
        "title": book.title,
        "body": book.body
    })

@bp.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return "", 204



