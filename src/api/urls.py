from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja import Swagger
from django.urls import path

api = NinjaExtraAPI(title='BookStore',docs=Swagger(),csrf=True)
api.register_controllers(NinjaJWTDefaultController)

urlpatterns = [
    path("api/v1/", api.urls),
]