from pydantic import BaseModel

# Base model for input
class BookBase(BaseModel):
    title: str
    author: str
    year: int

# Model for creating a book
class BookCreate(BookBase):
    pass

# Model for response with ID
class BookOut(BookBase):
    id: int

    class Config:
        orm_mode = True
