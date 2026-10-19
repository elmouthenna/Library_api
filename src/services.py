from database import get_connection
from models import Book

# ----------------------------------------------
# CREATE  : ajouter un livre
# ----------------------------------------------
def add_book(title, author, year=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (title, author, year)
    )

    conn.commit()
    new_id = cur.lastrowid   # id auto-incrémenté créé par SQLite
    conn.close()

    return Book(new_id, title, author, year).to_dict()


# ----------------------------------------------
# READ  : lire tous les livres
# ----------------------------------------------
def get_all_books():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, author, year FROM books")
    rows = cur.fetchall()
    conn.close()

    books = []
    for row in rows:
        book = Book(row[0], row[1], row[2], row[3])
        books.append(book.to_dict())

    return books

#lire un livre par son id
# ----------------------------------------------
def get_book_by_id(book_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, author, year FROM books WHERE id = ?",
        (book_id,)
    )
    row = cur.fetchone()   # None si aucune ligne ne correspond
    conn.close()

    if row is None:
        return None

    return Book(row[0], row[1], row[2], row[3]).to_dict()

# ----------------------------------------------
# UPDATE : modifier un livre
# ----------------------------------------------
def update_book(book_id, title, author, year=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
        (title, author, year, book_id)
    )

   conn.commit()
    touched = cur.rowcount   # nombre de lignes réellement modifiées
    conn.close()

    if touched == 0:
        return None          # aucun livre avec cet id

    return {"message": f"Book {book_id} updated."}


# ----------------------------------------------
# DELETE : supprimer un livre
# ----------------------------------------------
def delete_book(book_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))

     conn.commit()
    touched = cur.rowcount   # 0 si aucun livre n'avait cet id
    conn.close()

    if touched == 0:
        return None

    return {"message": f"Book {book_id} deleted."}
