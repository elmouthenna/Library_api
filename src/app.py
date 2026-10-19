from flask import Flask, request, jsonify

from database import init_db
from services import (
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
)

app = Flask(__name__)

# Crée la table "books" au démarrage si elle n'existe pas encore.
init_db()


@app.get("/")
def home():
    return {"message": "Library API working"}


# ----------------------------------------------
# GET /books : la liste de tous les livres
# ----------------------------------------------
@app.get("/books")
def list_books():
    return jsonify(get_all_books()), 200


# ----------------------------------------------
# GET /books/<id> : un livre précis
# ----------------------------------------------
@app.get("/books/<int:book_id>")
def read_book(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        return {"error": f"Book {book_id} not found."}, 404

    return jsonify(book), 200


# ----------------------------------------------
# POST /books : ajouter un livre
# ----------------------------------------------
@app.post("/books")
def create_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return {"error": "Fields 'title' and 'author' are required."}, 400

    book = add_book(title, author, data.get("year"))
    return jsonify(book), 201   # 201 = créé


# ----------------------------------------------
# PUT /books/<id> : modifier un livre
# ----------------------------------------------
@app.put("/books/<int:book_id>")
def edit_book(book_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return {"error": "Fields 'title' and 'author' are required."}, 400

    book = update_book(book_id, title, author, data.get("year"))
    if book is None:
        return {"error": f"Book {book_id} not found."}, 404

    return jsonify(book), 200


# ----------------------------------------------
# DELETE /books/<id> : supprimer un livre
# ----------------------------------------------
@app.delete("/books/<int:book_id>")
def remove_book(book_id):
    result = delete_book(book_id)
    if result is None:
        return {"error": f"Book {book_id} not found."}, 404

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
    
