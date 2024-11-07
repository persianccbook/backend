from ninja import ModelSchema, Schema
from api.schema import ApiResponseSchema, DataSchema
from users.models import User


class AuthorSchema(ModelSchema):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
        ]


class SingleAuthorDataSchema(DataSchema):
    payload: AuthorSchema


class SingleAuthorSchema(ApiResponseSchema):
    data: SingleAuthorDataSchema


class PaginatedAuthors(Schema):
    authors: list[AuthorSchema]
    next_page: int
    prev_page: int


class PaginatedAuthorsDataSchema(DataSchema):
    payload: PaginatedAuthors


class PaginatedAuthorsSchema(ApiResponseSchema):
    data: PaginatedAuthorsDataSchema
