from django.contrib import admin
from announcement.models import Announcement, ContactUs


# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['email','is_read']
    readonly_fields = ('email','message',)
    ordering = ['is_read',]
    list_filter = ['is_read',]


admin.site.register(ContactUs,ContactUsAdmin)

admin.site.register(Announcement, AnnouncementAdmin)
