from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import forms
from .models import Book, Vote, BookFile, UP, DOWN

import os


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


class ViewBook(generic.DetailView):
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

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        for obj in book.files.all():
            try:
                obj.file.delete()
            except:
                pass
        return super(DeleteBookFile, self).delete(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_staff)
def book_toggle_view(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    book.hidden = not book.hidden
    book.save()
    messages.success(request, "Book '{}' has been {}".format(str(book), 'hidden' if book.hidden else 'shown'))
    return redirect('books:list')


@login_required
def vote_book(request, isbn, value=UP):
    book = get_object_or_404(Book, isbn=isbn)
    if value not in [DOWN, UP]:
        return HttpResponse('Your vote is invalid')
    vote = Vote.objects.filter(book=book, user=request.user).first()
    if vote:
        if vote.action == value:
            vote.delete()
            return HttpResponse('Your vote has been deleted')
    else:
        vote = Vote(book=book, user=request.user)
    vote.action = value
    vote.save()
    return HttpResponse('Your {}vote has been scored'.format('up' if value == UP else 'down'))


class DeleteBookFile(StaffOnlyView, generic.edit.DeleteView):
    model = BookFile
    template_name = 'files/files_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('books:details', kwargs={'pk': self.book_pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.book_pk = obj.book.pk
        try:
            obj.file.delete()
        except:
            pass
        return super(DeleteBookFile, self).delete(request, *args, **kwargs)


class EditBookFile(StaffOnlyView, generic.edit.UpdateView):
    template_name = 'files/edit.html'
    model = BookFile
    form_class = forms.BookFileForm


class AddBookFile(StaffOnlyView, generic.CreateView):
    template_name = 'files/edit.html'
    model = BookFile
    form_class = forms.BookFileForm
