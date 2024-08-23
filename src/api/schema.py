from ninja import ModelSchema,Schema
from typing import Any, Optional
from users.models import User

class ErrorSchema(Schema):
    details: Optional[str]

class DataSchema(Schema):
    message: str
    payload: Optional[Any] = None
    error: Optional[ErrorSchema] = None

class ApiResponseSchema(Schema):
    status: str
    data: DataSchema


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','is_superuser','is_verified']