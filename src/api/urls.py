from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja import Swagger
from django.urls import path
from .user_api import router as users_router
from .auth_api import router as auth_router
from ninja.errors import ValidationError,AuthenticationError,HttpError
from .utils import api_response

api = NinjaExtraAPI(title='PersianCCBooks',docs=Swagger(),csrf=True)

# jwt controler
api.register_controllers(NinjaJWTDefaultController)

# exception handler
@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return api_response(
            success=False,
            message="Your input is not valid.",
            error="Invalid Input.",
            status_code=403
        )
@api.exception_handler(AuthenticationError)
def authemtication_errors(request, exc):
    return api_response(
            success=False,
            message="You are not authenticated, login to continue.",
            error="Not Authenticated.",
            status_code=401
        )
# routers
api.add_router("/users/",users_router)
api.add_router("/auth/",auth_router)

urlpatterns = [
    path("api/v1/", api.urls),
]