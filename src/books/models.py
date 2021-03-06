import os
import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .validators import validate_isbn

User = get_user_model()
UP = 1
DOWN = -1


def book_picture_path(instance, filename):
    return 'books/isbn_{0}/paperback.png'.format(instance.isbn)


def book_files_path(instance, filename):
    return 'books/isbn_{0}/{1}'.format(instance.book.isbn, filename)


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=300)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    description = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.full_name, self.country)

    @property
    def full_name(self):
        names = (self.first_name, self.middle_name, self.last_name)
        return ' '.join(list(filter(None.__ne__, names)))


class Publisher(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=100)

    def __str__(self):
        return '{} ({})'.format(self.name, self.country)


class Tag(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True, primary_key=True,
                            # validators=[validate_isbn])
                            validators=[])
    authors = models.ManyToManyField(Author, related_name='books')
    description = models.TextField()
    title = models.CharField(max_length=300)
    pages = models.IntegerField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    publisher = models.ForeignKey(Publisher, blank=True, null=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=100, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='books')
    hidden = models.BooleanField(default=False)
    picture = models.ImageField('Book picture',
                                upload_to=book_picture_path,
                                null=True,
                                blank=True)
    copies_num = models.IntegerField(default=0)

    def __str__(self):
        return '{0} by {1} [ISBN: {2}]'.format(self.title, self.authors_names, self.isbn)

    def get_absolute_url(self):
        return reverse('books:details', args=[self.isbn])

    def get_upvotes_count(self):
        return Vote.objects.filter(book=self, action=UP).count()

    def get_downvotes_count(self):
        return Vote.objects.filter(book=self, action=DOWN).count()

    def get_rating(self):
        return self.get_upvotes_count() - self.get_downvotes_count()

    def take_book(self, user):
        if self.copies_num <= 0:
            return
        record = ReadersListRecord(book=self, user=user)
        record.save()
        self.copies_num -= 1
        self.save()
        return record

    def return_book(self, user):
        record = ReadersListRecord.objects.filter(book=self, user=user,
                                                  date_returned=None).first()
        record.date_returned = datetime.datetime.now()
        record.save()
        self.copies_num += 1
        self.save()
        return True

    def is_taken_by(self, user):
        record = ReadersListRecord.objects.filter(book=self, user=user, date_returned=None)
        return True if record else False

    def get_current_readers_records(self):
        return ReadersListRecord.objects.filter(book=self, date_returned=None).all()

    @property
    def authors_names(self):
        names = [x.full_name for x in self.authors.all()]
        return ', '.join(names)


class BookFile(models.Model):
    book = models.ForeignKey(Book, related_name='files',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=book_files_path)

    def __str__(self):
        return 'File "{}" for {}'.format(self.name, self.book)

    def filename(self):
        return os.path.basename(self.file.name)


class Vote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.SmallIntegerField(default=UP)


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BookComment(models.Model):
    book = models.ForeignKey(Book, related_name='comments')
    body = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments')
    blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{}: {}'.format(self.user.email, self.body)


class ReadersListRecord(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True, blank=False)
    date_returned = models.DateTimeField(null=True, blank=True)
