class Book:
    def __init__(self, book_id, title, author, year=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        """Convertit l'objet Book en dictionnaire (pour JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    def __repr__(self):
        return f"<Book {self.id} - {self.title} ({self.author})>"
