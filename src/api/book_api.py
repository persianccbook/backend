from ninja import Router
from api.schema import ApiResponseSchema, BookSchema, ChapterSchema, GenreSchema, PageSchema, PaginatedBooksSchema
from api.utils import api_response
from books.models import Book
from typing import List

# ============================
# Books Endpoints
# ============================                  
router = Router(tags=["books"])

# TODO: make all returns use api_response

@router.get("/get_all_books", response=PaginatedBooksSchema)
def get_all_books(request, limit: int = 1, offset: int = 0):
    try:
        books = Book.objects.all()
        if limit*offset>=len(books):
            return api_response(success=False,message="This page is empty",error='empty page',status_code=404) 
        if len(books)==limit*offset+limit:
            next = -1
        elif len(books)<limit*offset+limit and len(books)>=limit*offset:
            next = -1
            limit = len(books)%limit
        else:
            next = offset+1 
        if offset==0:
            prev=-1
        else:
            prev = offset-1
        
        books=books[offset * limit : offset * limit + limit]
        books_data = [BookSchema.from_orm(book) for book in books]
        # return books_data
        return api_response(success=True,message="all books fetched successfully",payload={'books':books_data,'next_page':next,'perv_page':prev})   

    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


@router.get("/get_book", response=BookSchema)
def get_book(request, book_id: int):
    try:
            book = Book.objects.get(id=book_id)
            book_data = BookSchema.from_orm(book)
            return api_response(
                success=True,
                message="Book fetched successfully.",
                payload=book_data.dict(),
                status_code=200
            )
    except Book.DoesNotExist:
        return api_response(
            success=False,
            message="Book not found.",
            error="No book with this book id exists.",
            status_code=404
        )
                    

@router.get("/top_books", response=List[BookSchema])
def top_books(request):
    try:
        # TODO: use rating to pick top 3 books after rating implementation completed
        books = Book.objects.all()
        if len(books) > 3 :
            books= books[0:3]
        books_data = [BookSchema.from_orm(book) for book in books]
        return books_data
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )            

#  TODO: implement endpoints below

@router.get("/get_book_chapters", response=List[ChapterSchema])
def get_book_chapters(request, book_id: int):
    pass


@router.get("/get_chapter_", response=List[PageSchema])
def get_chapter_pages(request, book_id: int, chapter_number: int):
    pass


@router.get("/get_genres", response=List[GenreSchema])
def get_genres(request):
    pass

@router.get("/get_genre_books", response=List[BookSchema])
def get_genre_books(request):
    pass