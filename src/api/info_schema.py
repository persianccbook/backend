from ninja import ModelSchema
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
