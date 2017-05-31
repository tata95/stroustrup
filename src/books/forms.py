from django import forms
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from .models import Book, BookFile


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('isbn'),
            Field('title'),
            Field('pages'),
            Field('publish_date'),
            Field('publisher'),
            Field('language'),
            Field('authors'),
            Field('genre'),
            Field('tags'),
            Field('picture'),
            Field('description'),
            Submit('save', 'Save', css_class="btn-success"),
        )

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'pages', 'publish_date', 'tags',
                  'publisher', 'language', 'authors', 'genre', 'picture']


class BookFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('file'),
            Submit('save', 'Save', css_class="btn-success"),
        )

    class Meta:
        model = BookFile
        fields = ['name', 'description', 'file']
