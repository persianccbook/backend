from ninja import Field, ModelSchema, Schema
from pydantic import BaseModel, EmailStr
from typing import Optional
from books.models import Book, Chapter, Genre, Page
from users.models import User


class ErrorSchema(Schema):
    details: Optional[str]


class DataSchema(Schema):
    message: str
    payload: Optional[dict] = None
    error: Optional[ErrorSchema] = None

class ApiResponseSchema(Schema):
    status: str
    data: DataSchema



class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "is_verified",
        ]


class SignInSchema(BaseModel):
    email: EmailStr
    password: str


class EmailVerificationSchema(Schema):
    user_id: str
    token: str


class ChangePasswordSchema(Schema):
    current_password: str
    new_password: str
    confirm_new_password: str


class PasswordResetRequestSchema(Schema):
    email: EmailStr


class PasswordResetConfirmSchema(Schema):
    token: str
    user_id: str
    new_password: str
    confirm_new_password: str


class BookSchema(ModelSchema):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "genre",
            "authors",
            "cover_image",
            "published",
        ]

    rating: str = Field(alias="average_rating", default=None)


class PaginatedBooks(Schema):
    books: list[BookSchema]
    next_page: int
    prev_page: int

class PaginatedBooksDataSchema (DataSchema):
    payload:PaginatedBooks

class PaginatedBooksSchema (ApiResponseSchema):
    data:PaginatedBooksDataSchema

class ChapterSchema(ModelSchema):
    class Meta:
        model = Chapter
        fields = ["book", "title", "chapter_number", "created", "updated"]


class PageSchema(ModelSchema):
    class Meta:
        model = Page
        fields = ["chapter", "content", "title", "page_number", "created", "updated"]


class GenreSchema(ModelSchema):
    class Meta:
        model = Genre
        fields = ["id", "title", "description"]
