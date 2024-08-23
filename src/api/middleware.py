from django.utils.deprecation import MiddlewareMixin
from .utils import api_response
from ninja.errors import HttpError
from django.http import JsonResponse


class FormatExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpError) and exception.status_code == 401:
            return JsonResponse({
                "success": False,
                "message": "Unauthorized access"
            }, status=401)
        else:
            return api_response(
                    success=False,
                    message=exception.message,
                    error=str(exception),
                    status_code=exception.status_code
                )