from django.contrib import admin
from .models import Book, BookCopy, Genre, Author, Tag, Publisher


admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Publisher)
