from django.contrib import admin
from .models import Book, Chapter, Page, Genre


# Register your models here.


class PageInline(admin.TabularInline):
    model = Page
    # fields = ('page_number', 'content')
    extra = 1
    show_change_link = True


class ChapterInline(admin.TabularInline):
    model = Chapter
    inlines = [PageInline]
    fields = ("chapter_number", "title")
    extra = 1
    show_change_link = True


class BookAdmin(admin.ModelAdmin):
    fields = (
        # 'id',
        "title",
        "authors",
        "genre",
        "description",
        "cover_image",
        "status",
    )
    inlines = [ChapterInline]


class PageAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    fields = ("title", "description")


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter)
admin.site.register(Page, PageAdmin)
