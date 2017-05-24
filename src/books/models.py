from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=300)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    description = models.TextField()

    def __str__(self):
        return '<Author: {} {}, {}>'.format(self.first_name, self.last_name, self.country)


class Publisher(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    authors = models.ManyToManyField(Author)
    description = models.TextField()
    title = models.CharField(max_length=300)
    pages = models.IntegerField()
    publish_date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)  # TODO: make blanks
    language = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    # attachments
    # likes/dislikes

    def __str__(self):
        return '{} ({}), {}'.format(self.title, self.publish_date.year, self.genre.name)


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20)
    arrived = models.DateTimeField(auto_now=True)
