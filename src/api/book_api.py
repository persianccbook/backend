from ninja import Router
from api.schema import  BookSchema
from api.utils import api_response
from books.models import Book
from typing import List




# ============================
# Books Endpoints
# ============================
router = Router(tags=["books"])


@router.get("/get_all_books", response=List[BookSchema])
# @paginate(LimitOffsetPagination)
def get_all_books(request,limit: int = 1, offset: int = 0):
    try:
        books = Book.objects.all()[offset*limit:offset*limit+limit  ]
        books_data = [BookSchema.from_orm(book) for book in books]  
        return books_data
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )
