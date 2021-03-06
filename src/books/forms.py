from django import forms
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from .models import Book, BookFile, BookComment, Tag
from pagedown.widgets import PagedownWidget, AdminPagedownWidget


class BookForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('isbn'),
            Button('fetch', 'Fetch info'),
            Field('title'),
            Field('pages'),
            Field('publish_date'),
            Field('publisher'),
            Field('language'),
            Field('authors'),
            Field('genre'),
            Field('tags'),
            Field('description'),
            Field('picture'),
            Submit('save', 'Save', css_class="btn-success"),
        )

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'pages', 'publish_date', 'tags', 'description',
                  'publisher', 'language', 'authors', 'genre', 'picture']


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    genre = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Field('title'),
            Field('tags'),
            Field('genre'),
            Submit('', 'Search', css_class="btn-success"),
        )


class BookAdminForm(BookForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'pages', 'publish_date', 'tags', 'description',
                  'publisher', 'language', 'authors', 'genre', 'picture', 'hidden', 'copies_num']


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


class BookCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = "form-group"
        self.helper.form_show_labels = False
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Field('body', rows="4", css_class='form-control'),
            Submit('send', 'Send', css_class="btn-success"),
        )

    class Meta:
        model = BookComment
        fields = ['body']


class CommentBlockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentBlockForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-group"
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Field('blocked_reason', rows="4", css_class='form-control'),
            Submit('save', 'Save', css_class="btn-success"),
        )

    class Meta:
        model = BookComment
        fields = ['blocked_reason']


class TagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Submit('save', 'Save', css_class="btn-success"),
        )

    class Meta:
        model = Tag
        fields = ['name']
