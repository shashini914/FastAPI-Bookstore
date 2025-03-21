from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate

def get_books(db: Session):
    """
    Retrieve all books from the database.

    :param db: Database session
    :return: List of all books
    """
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    """
    Retrieve a single book by its ID.

    :param db: Database session
    :param book_id: ID of the book to retrieve
    :return: Book object if found, otherwise None
    """
    return db.query(Book).filter(Book.id == book_id).first()

def create_book(db: Session, book: BookCreate):
    """
    Add a new book to the database.

    :param db: Database session
    :param book: Book data validated using Pydantic schema
    :return: Newly created book object
    """
    db_book = Book(**book.dict()) # Convert Pydantic model to dictionary and unpack it
    db.add(db_book) # Add book to session
    db.commit() # Commit changes to database
    db.refresh(db_book) # Refresh the object to get updated data
    return db_book

def delete_book(db: Session, book_id: int):
    """
    Delete a book from the database by its ID.

    :param db: Database session
    :param book_id: ID of the book to delete
    :return: Deleted book object if found, otherwise None
    """
    book = get_book(db, book_id)
    if book:
        db.delete(book) # Mark book for deletion
        db.commit() # Commit changes
    return book
