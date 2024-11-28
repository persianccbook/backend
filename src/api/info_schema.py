from ninja import ModelSchema
from pydantic import BaseModel, EmailStr
from announcement.models import Announcement
from api.schema import ApiResponseSchema, DataSchema


class AnnouncementSchema(ModelSchema):
    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "content",
        ]


class SingleAnnouncementDataSchema(DataSchema):
    payload: AnnouncementSchema


class SingleAnnouncementSchema(ApiResponseSchema):
    data: SingleAnnouncementDataSchema


class ContactUsMessage(BaseModel):
    email: EmailStr
    message: str

class ContactUsDataSchema(DataSchema):
    payload:ContactUsMessage

class ContactUsSchema(ApiResponseSchema):
    data:ContactUsDataSchema