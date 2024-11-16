from ninja import Router
from api.info_schema import AnnouncementSchema, SingleAnnouncementSchema
from announcement.models import Announcement
from api.utils import api_response

# ============================
# Info Endpoints
# ============================
router = Router(tags=["info"])


@router.get("/get_announcement", response=SingleAnnouncementSchema)
def get_announcement(request):
    try:
        announcement = Announcement.objects.last()
        announcement_data = AnnouncementSchema.from_orm(announcement)

        return api_response(
            success=True,
            message="last announcement fetched successfully",
            payload=announcement_data.dict(),
        )
    except Exception as e:
        return api_response(
            success=False, message="Error occurd", error=e, status_code=503
        )
