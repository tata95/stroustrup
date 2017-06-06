from django.core.exceptions import ValidationError
from isbnlib import notisbn


def validate_isbn(value):
    if notisbn(value):
        raise ValidationError('%(value)s is not ISBN-like', params={'value': value})
