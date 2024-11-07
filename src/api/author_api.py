from ninja import Router
from api.author_schema import AuthorSchema, SingleAuthorSchema, PaginatedAuthorsSchema
from api.book_schema import BookSchema, PaginatedBooksSchema
from api.utils import api_response
from books.models import Book
from users.models import User

# ============================
# author Endpoints
# ============================
router = Router(tags=["author"])


@router.get("/get_all_authors", response=PaginatedAuthorsSchema)
def get_all_authors(request, limit: int = 1, offset: int = 0):
    try:
        authors = User.objects.filter(authored_books__isnull=False).distinct()
        if limit * offset >= len(authors):
            return api_response(
                success=False,
                message="This page is empty",
                error="empty page",
                status_code=404,
            )
        if len(authors) == limit * offset + limit:
            next = -1
        elif len(authors) < limit * offset + limit and len(authors) >= limit * offset:
            next = -1
            limit = len(authors) % limit
        else:
            next = offset + 1
        if offset == 0:
            prev = -1
        else:
            prev = offset - 1

        authors = authors[offset * limit : offset * limit + limit]
        authors_data = [AuthorSchema.from_orm(author) for author in authors]
        # return authors_data
        return api_response(
            success=True,
            message="all authors fetched successfully",
            payload={"authors": authors_data, "next_page": next, "perv_page": prev},
        )

    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )


@router.get("/get_author", response=SingleAuthorSchema)
def get_author(request, author_id: int):
    try:
        author = User.objects.filter(authored_books__isnull=False).distinct().get(id=author_id)
        author_data = AuthorSchema.from_orm(author)
        return api_response(
            success=True,
            message="Author fetched successfully.",
            payload=author_data.dict(),
            status_code=200,
        )
    except User.DoesNotExist:
        return api_response(
            success=False,
            message="Author not found.",
            error="No Author with this author id exists.",
            status_code=404,
        )

@router.get("/get_author_books", response=PaginatedBooksSchema)
def get_author_books(request, author_id: int, limit: int = 1, offset: int = 0):
    try:
        author = User.objects.filter(authored_books__isnull=False).distinct().get(id=author_id)
        try:
            books = Book.objects.filter(authors__id=author.id)          
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
    except User.DoesNotExist:
        return api_response(
            success=False,
            message="Author not found.",
            error="No Author with this author id exists.",
            status_code=404,
        )