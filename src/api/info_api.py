from ninja import Router
from api.info_schema import AnnouncementSchema, ContactUsMessage, ContactUsSchema, SingleAnnouncementSchema
from announcement.models import Announcement, ContactUs
from api.schema import ApiResponseSchema
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

@router.post("/contact-us", response=ContactUsSchema)
def contact_us(request, payload: ContactUsMessage):
    try:
        contact = ContactUs.objects.create(
            email=payload.email,
            message=payload.message
        )
        return api_response(
            success=True,
            message="Message received successfully",
            payload={'email':contact.email,'message':contact.message},
            status_code=200
        )
    except Exception as e:
        return api_response(
            success=False,
            message=str(e),
            payload=None,
            status_code=503
        )