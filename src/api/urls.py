from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja import Swagger
from django.urls import path
from .user_api import router as users_router


api = NinjaExtraAPI(title='BookStore',docs=Swagger(),csrf=True)

# jwt controler
api.register_controllers(NinjaJWTDefaultController)


# routers
api.add_router("/users/",users_router)

urlpatterns = [
    path("api/v1/", api.urls),
]