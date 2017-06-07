from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
import random
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce

from books.models import Book, ReadersListRecord


class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)

    read_books = models.ManyToManyField(Book, blank=True, related_name='readers')

    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField('Short Bio', max_length=200, blank=True, null=True)
    email_verified = models.BooleanField('Email verified', default=False)

    def get_absolute_url(self):
        return reverse('profiles:show', args=[self.slug])

    def get_taken_books(self):
        result = self.user.readerslistrecord_set.filter(date_returned=None)
        return result

    def get_recommended_books(self):
        read_books_ids = self.read_books.values_list('pk', flat=True)
        unread_books = Book.objects.filter(hidden=False) \
                           .annotate(rating=Coalesce(Sum('vote__action'), 0)) \
                           .exclude(pk__in=read_books_ids)

        top_rated_all = unread_books.order_by('-rating')

        top_genres = self.read_books.values('genre') \
                         .annotate(c=Count('genre')).order_by('-c')[:5]
        top_genres_list = [obj['genre'] for obj in top_genres]
        top_rated_by_genre = unread_books.filter(genre__in=top_genres_list) \
                                         .order_by('-rating')
        # TODO: Add queryset with top books by tags of read books
        result = list((top_rated_all | top_rated_by_genre).distinct()[:25])
        random.shuffle(result)
        return result

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):

    def __str__(self):
        return "{}'s profile". format(self.user)
