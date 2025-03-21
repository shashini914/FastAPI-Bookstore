from sqlalchemy import Column, Integer, String
from database import Base

# Define the Book model, which maps to the "books" table in the database
class Book(Base):
    __tablename__ = "books"  # Set the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each book (Primary Key)
    title = Column(String, index=True)  # Book title (Indexed for faster searches)
    author = Column(String)  # Author's name
    year = Column(Integer)  # Year of publication
