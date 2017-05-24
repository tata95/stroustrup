from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Book


def books_list(request):
    template_name = 'books/list.html'
    books_list = Book.objects.filter(hidden=False)
    page = request.GET.get('page', 1)
    count = request.GET.get('count', 10)
    paginator = Paginator(books_list, count)
    page_neighbors_count = 3

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    index = books.number - 1
    max_index = len(paginator.page_range)
    start_index = index - page_neighbors_count + 1 if index >= page_neighbors_count + 1 else 0
    end_index = index + page_neighbors_count if index <= max_index - page_neighbors_count else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, template_name,
                  context={'books': books, 'page_range': page_range})


def book_details(request, isbn):
    template_name = 'books/details.html'
    book = get_object_or_404(Book, isbn=isbn)
    return render(request, template_name, context={'book': book})


def book_create(request):
    pass


def book_edit(request, isbn):
    pass


def book_toggle_view(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    book.hidden = not book.hidden
    book.save()
    messages.success(request, "Book '{}' has been {}".format(str(book), 'hidden' if book.hidden else 'shown'))
    return redirect('books:list')


def book_delete(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    book.delete()
    messages.success(request, "Book '{}' has been deleted".format(str(book)))
    return redirect('books:list')


def add_to_readlist(request, isbn):
    pass


class EditBook(LoginRequiredMixin, generic.TemplateView):
    template_name = 'books/edit.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if 'isbn' not in kwargs or not self.request.user.is_staff:
            return redirect('books:list')
        book = Book.objects.filter(isbn=kwargs['isbn']).first()
        if 'book_form' not in kwargs:
            kwargs['book_form'] = forms.BookForm(instance=book)
        return super(EditBook, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'isbn' not in kwargs or not self.request.user.is_staff:
            return redirect('books:list')
        book = Book.objects.filter(isbn=kwargs['isbn']).first()
        book_form = forms.BookForm(request.POST, instance=book)
        if not book_form.is_valid():
            messages.error(request, 'There was a problem with the form. '
                           'Please check the details.')
            book_form = forms.BookForm(instance=book)
            return super(EditBook, self).get(request,
                                             book_form=book_form)
        book = book_form.save()
        messages.success(request, 'Book details saved!')
        return redirect('books:details', isbn=book.isbn)


class CreateBook(LoginRequiredMixin, generic.TemplateView):
    template_name = 'books/create.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('books:list')
        if 'book_form' not in kwargs:
            kwargs['book_form'] = forms.BookForm()
        return super(CreateBook, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('books:list')
        book_form = forms.BookForm(request.POST)
        if not book_form.is_valid():
            messages.error(request, 'There was a problem with the form. '
                           'Please check the details.')
            book_form = forms.BookForm()
            return super(CreateBook, self).get(request,
                                               book_form=book_form)
        book = book_form.save()
        messages.success(request, 'Book details saved!')
        return redirect('books:details', isbn=book.isbn)
