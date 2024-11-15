from django.contrib import admin
from announcement.models import Announcement


# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


admin.site.register(Announcement, AnnouncementAdmin)
