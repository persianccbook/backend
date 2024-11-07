from ninja.responses import Response
from .schema import ApiResponseSchema, DataSchema, ErrorSchema

def api_response(success: bool, message: str, payload=None, error=None, status_code=200):
    """
    Utility function to standardize API responses.
    """
    error_message = error.__str__() if error else None
    response_structure = ApiResponseSchema(
        status='success' if success else 'error',
        data=DataSchema(
            message=message,
            payload=payload if success else None,
            error=ErrorSchema(details=error_message) if not success else None
        )
    )
    return Response(response_structure.dict(), status=status_code)