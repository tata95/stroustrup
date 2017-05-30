from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


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
    isbn = models.CharField(max_length=20, unique=True, primary_key=True)
    authors = models.ManyToManyField(Author)
    description = models.TextField()
    title = models.CharField(max_length=300)
    pages = models.IntegerField()
    publish_date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)  # TODO: make blanks
    language = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    hidden = models.BooleanField(default=False)
    # attachments
    # likes/dislikes

    def __str__(self):
        return '{0} ({1}) by {2} [ISBN: {3}]'.format(self.title, self.publish_date.year,
                                                     self.authors_names, self.isbn)

    def get_absolute_url(self):
        return reverse('books:details', args=[self.isbn])

    @property
    def authors_names(self):
        names = [x.full_name for x in self.authors.all()]
        return ', '.join(names)


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20)
    arrived = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} copy, ID: {}, condition: {}'.format(self.book.title, self.pk, self.condition)


class BookComment(models.Model):
    book = models.ForeignKey(Book)
    body = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comment')
    blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.body)


class ReadersListRecord(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True, blank=False)
    date_returned = models.DateTimeField(blank=True)
