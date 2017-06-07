from django.contrib import admin
from .models import Book, ReadersListRecord, Genre, Author, Tag, Publisher, BookFile
from .forms import BookAdminForm


# admin.site.register(Book)
admin.site.register(ReadersListRecord)
admin.site.register(BookFile)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Publisher)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
