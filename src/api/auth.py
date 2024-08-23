from ninja_jwt.authentication import JWTAuth
from .utils import api_response
from ninja.errors import HttpError

class CustomJWTAuth(JWTAuth):
    def authenticate(self, request):
        try:
            user = super().authenticate(request)
            if not user:
                raise HttpError(401, "Unauthorized access!")
            return user
        except HttpError as e:
            raise HttpError(401, "Unauthorized access!")  # Re-raise with custom message
    
    
# return api_response(
#     success=False,
#     message="You should be athorized to access this.",
#     error="Unathorized",
#     status_code=401
# )