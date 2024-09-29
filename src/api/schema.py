from ninja import Field, ModelSchema,Schema
from pydantic import BaseModel,EmailStr
from typing import Optional
from books.models import Book
from users.models import User

class ErrorSchema(Schema):
    details: Optional[str]

class DataSchema(Schema):
    message: str
    payload: Optional[dict] = None
    error: Optional[ErrorSchema] = None

class ApiResponseSchema(Schema):
    status: str
    data: DataSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','is_superuser','is_verified']

class SignInSchema(BaseModel):
    email: EmailStr
    password: str

class EmailVerificationSchema(Schema):
    user_id: str
    token: str

class ChangePasswordSchema(Schema):
    current_password: str
    new_password: str
    confirm_new_password: str

class PasswordResetRequestSchema(Schema):
    email: EmailStr

class PasswordResetConfirmSchema(Schema):
    token: str
    user_id: str
    new_password: str
    confirm_new_password: str

class BookSchema(ModelSchema):
    class Meta:
        model = Book
        fields = ['id','title','description','genre','authors','cover_image','published']

    rating: str = Field(alias='average_rating',default=None)
    
   
    