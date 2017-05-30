from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse_lazy
from . import forms
from .models import Book


class StaffOnlyView(object):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(StaffOnlyView, self).dispatch(request, *args, **kwargs)


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


class ViewBook(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'books/details.html'


class EditBook(StaffOnlyView, generic.edit.UpdateView):
    template_name = 'books/edit.html'
    model = Book
    form_class = forms.BookForm


class CreateBook(StaffOnlyView, generic.CreateView):
    template_name = 'books/create.html'
    model = Book
    form_class = forms.BookForm


class DeleteBook(StaffOnlyView, generic.edit.DeleteView):
    model = Book
    success_url = reverse_lazy('books:list')


@user_passes_test(lambda u: u.is_staff)
def book_toggle_view(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    book.hidden = not book.hidden
    book.save()
    messages.success(request, "Book '{}' has been {}".format(str(book), 'hidden' if book.hidden else 'shown'))
    return redirect('books:list')
