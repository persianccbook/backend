from ninja import Router
from api.book_schema import (
    BookChaptersSchema,
    BookPagesSchema,
    BookSchema,
    ChapterSchema,
    PageSchema,
    PaginatedBooksSchema,
    SingleBookSchema,
    TopBooksSchema,
)
from api.schema import GenreSchema
from api.utils import api_response
from books.models import Book
from typing import List
from django.views.decorators.cache import cache_page

# ============================
# Books Endpoints
# ============================
router = Router(tags=["books"])

# TODO: make all returns use api_response


@router.get("/get_all_books", response=PaginatedBooksSchema)
@cache_page(60 * 60)
def get_all_books(request, limit: int = 1, offset: int = 0):
    try:
        books = Book.released.all()
        if limit * offset >= len(books):
            return api_response(
                success=False,
                message="This page is empty",
                error="empty page",
                status_code=404,
            )
        if len(books) == limit * offset + limit:
            next = -1
        elif len(books) < limit * offset + limit and len(books) >= limit * offset:
            next = -1
            limit = len(books) % limit
        else:
            next = offset + 1
        if offset == 0:
            prev = -1
        else:
            prev = offset - 1

        books = books[offset * limit : offset * limit + limit]
        books_data = [BookSchema.from_orm(book) for book in books]
        # return books_data
        return api_response(
            success=True,
            message="all books fetched successfully",
            payload={"books": books_data, "next_page": next, "perv_page": prev},
        )

    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


@router.get("/get_book", response=SingleBookSchema)
@cache_page(60 * 60)
def get_book(request, book_id: int):
    try:
        book = Book.released.get(id=book_id)
        book_data = BookSchema.from_orm(book)
        return api_response(
            success=True,
            message="Book fetched successfully.",
            payload=book_data.dict(),
            status_code=200,
        )
    except Book.DoesNotExist:
        return api_response(
            success=False,
            message="Book not found.",
            error="No book with this book id exists.",
            status_code=404,
        )


@router.get("/top_books", response=TopBooksSchema)
@cache_page(60 * 60)
def top_books(request):
    try:
        # TODO: use rating to pick top 3 books after rating implementation completed
        books = Book.released.all().order_by("-rating", "published")
        if len(books) > 3:
            books = books[0:3]
        books_data = [BookSchema.from_orm(book) for book in books]
        return api_response(
            success=True,
            message="top books fetched successfully",
            payload={"books": books_data},
        )
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


#  TODO: implement endpoints below


@router.get("/get_book_chapters", response=BookChaptersSchema)
@cache_page(60 * 60)
def get_book_chapters(request, book_id: int):
    try:
        book = Book.released.get(id=book_id)
        chapters = book.chapters.all()
        chapters_data = [ChapterSchema.from_orm(chapter) for chapter in chapters]

        return api_response(
            success=True,
            message="book chapters fetched successfully",
            payload={"chapters": chapters_data},
        )
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


@router.get("/get_chapter_pages", response=BookPagesSchema)
@cache_page(60*60)
def get_chapter_pages(request, book_id: int, chapter_number: int):
    try:
        book = Book.released.get(id=book_id)
        pages = book.chapters.get(chapter_number=chapter_number).pages.all()
        pages_data = [PageSchema.from_orm(page) for page in pages]

        return api_response(
            success=True,
            message="chapter pages fetched successfully",
            payload={"pages": pages_data},
        )
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


@router.get("/get_genres", response=List[GenreSchema])
def get_genres(request):
    pass


@router.get("/get_genre_books", response=List[BookSchema])
def get_genre_books(request):
    pass
