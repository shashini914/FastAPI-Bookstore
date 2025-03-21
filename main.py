from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Bookstore API")

# Root route
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    Guides users to visit /docs for API documentation.
    """
    return {"message": "Welcome to the Bookstore API! Visit /docs for API documentation."}


# Dependency for DB session
def get_db():
    db = SessionLocal() # Open a new database session
    try:
        yield db # Provide session to the request
    finally:
        db.close() # Close session after request is processed

# Retrieve All Books (GET /books)
@app.get("/books", response_model=list[schemas.BookOut])
def read_books(db: Session = Depends(get_db)):
    """
    Fetch all books from the database.
    Uses dependency injection to get a database session.
    """
    return crud.get_books(db)

# Retrieve a specific book by ID 
@app.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Fetch a specific book by its ID.
    Raises a 404 error if the book is not found.
    """
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Create a new book
@app.post("/books", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book entry in the database.
    Uses Pydantic validation to ensure correct input.
    """
    return crud.create_book(db, book)

# Delete a book by ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database by ID.
    Raises a 404 error if the book does not exist.
    """
    deleted = crud.delete_book(db, book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
