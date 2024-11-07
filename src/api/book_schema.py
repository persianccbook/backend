from ninja import Field, ModelSchema, Schema
from api.schema import ApiResponseSchema, DataSchema
from books.models import Book, Chapter, Page


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


class SingleBookDataSchema(DataSchema):
    payload: BookSchema


class SingleBookSchema(ApiResponseSchema):
    data: SingleBookDataSchema


class TopBookSchema(Schema):
    books: list[BookSchema]


class TopBooksDataSchema(DataSchema):
    payload: TopBookSchema


class TopBooksSchema(ApiResponseSchema):
    data: TopBooksDataSchema


class PaginatedBooks(Schema):
    books: list[BookSchema]
    next_page: int
    prev_page: int


class PaginatedBooksDataSchema(DataSchema):
    payload: PaginatedBooks


class PaginatedBooksSchema(ApiResponseSchema):
    data: PaginatedBooksDataSchema


class ChapterSchema(ModelSchema):
    class Meta:
        model = Chapter
        fields = ["book", "title", "chapter_number", "created", "updated"]


class PageSchema(ModelSchema):
    class Meta:
        model = Page
        fields = ["chapter", "content", "title", "page_number", "created", "updated"]
