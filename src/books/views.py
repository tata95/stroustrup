from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from . import forms
from .models import Book, Vote, BookFile, Tag, Genre, UP, DOWN, BookComment, ReadersListRecord
import isbnlib

isbnlib.config.add_apikey('isbndb', settings.ISBNDB_API_KEY)


class StaffOnlyView(object):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(StaffOnlyView, self).dispatch(request, *args, **kwargs)


class BooksListView(generic.ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        count = request.GET.get('count')
        if count:
            self.paginate_by = count
        return super(BooksListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        page_neighbors_count = 3
        index = context['page_obj'].number - 1
        max_index = len(context['paginator'].page_range)
        start_index = index - page_neighbors_count + 1 if index >= page_neighbors_count + 1 else 0
        end_index = index + page_neighbors_count if index <= max_index - page_neighbors_count else max_index
        page_range = context['paginator'].page_range[start_index:end_index]
        context.update({'page_range': page_range})
        return context


class BooksSearchView(BooksListView, generic.edit.FormView):
    template_name = 'books/search.html'
    form_class = forms.BookSearchForm

    def get_context_data(self, **kwargs):
        context = {'form': self.get_form(self.form_class)}
        return super(BooksSearchView, self).get_context_data(**context)

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        tags = [x for x in self.request.GET.get('tags', '').split(',') if x]
        genre = self.request.GET.get('genre', '')
        object_list = self.model.objects.filter(hidden=False)
        if title:
            object_list = object_list.filter(title__icontains=title) | \
                object_list.filter(isbn__icontains=title)
        if genre:
            object_list = object_list.filter(
                genre__in=Genre.objects.filter(name__icontains=genre))
        if tags:
            object_list = object_list.filter(
                tags__in=Tag.objects.filter(name__in=tags))
        return object_list


class ViewBook(generic.DetailView, generic.edit.FormView):
    model = Book
    form_class = forms.BookCommentForm
    template_name = 'books/details.html'

    def get_context_data(self, **kwargs):
        context = {'form': self.get_form(self.form_class)}
        return super(ViewBook, self).get_context_data(**context)

    def form_valid(self, form):
        book = self.get_object()
        msg = form.cleaned_data['body']
        user = self.request.user
        comment_obj = BookComment(user=user, book=book, body=msg)
        comment_obj.save()
        return redirect('books:details', pk=book.pk)


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
            except Exception:
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
        except Exception:
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


class CommentBlock(StaffOnlyView, generic.edit.UpdateView):
    model = BookComment
    form_class = forms.CommentBlockForm
    template_name = 'books/block_comment.html'

    def get_context_data(self, **kwargs):
        context = {'form': self.get_form(self.form_class)}
        return super(CommentBlock, self).get_context_data(**context)

    def form_valid(self, form):
        comment = self.get_object()
        book = comment.book
        comment.blocked = True
        comment.blocked_reason = form.cleaned_data['blocked_reason']
        comment.save()
        messages.success(self.request, "Comment has been blocked")
        return redirect('books:details', pk=book.pk)


@user_passes_test(lambda u: u.is_staff)
def comment_unblock(request, pk):
    comment = get_object_or_404(BookComment, pk=pk)
    comment.blocked = False
    comment.blocked_reason = None
    comment.save()
    messages.success(request, "Comment has been unblocked")
    return redirect('books:details', pk=comment.book.pk)


def isbn_info(request):
    isbn = request.GET.get('isbn', '')
    data = {}
    if isbnlib.notisbn(isbn):
        return JsonResponse(data, status=400)
    description = isbnlib.desc(isbn)
    if description:
        data.update({'description': description})
    try:
        metadata = isbnlib.meta(isbn, 'isbndb')
    except Exception:
        metadata = {}
    data.update({'meta': metadata})
    return JsonResponse(data)


class AddTag(LoginRequiredMixin, generic.FormView):
    template_name = 'tags/add.html'
    model = Tag
    form_class = forms.TagForm

    def get_context_data(self, **kwargs):
        context = {'form': self.get_form(self.form_class),
                   'book': self.book}
        return super(AddTag, self).get_context_data(**context)

    def dispatch(self, request, *args, **kwargs):
        print(kwargs.get('isbn'))
        self.book = get_object_or_404(Book, isbn=kwargs.get('isbn'))
        return super(AddTag, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        tag = Tag.objects.get_or_create(name=name)[0]
        self.book.tags.add(tag)
        return super(AddTag, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'pk': self.book.pk})


@login_required
def purchase_request(request, isbn):
    template_name = 'books/emails/purchase.html'
    subject = 'Purchase request'
    from_email = request.user.email
    to_email = [settings.ADMIN_EMAIL]
    book = get_object_or_404(Book, isbn=isbn)
    context = {'request': request, 'book': book}
    message = get_template(template_name).render(context)
    msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    return redirect('books:details', pk=book.pk)


@login_required
def take_return_book(request, isbn):
    user = request.user
    book = get_object_or_404(Book, isbn=isbn)
    records = ReadersListRecord.objects.filter(book=book, user=user, date_returned=None)
    if records:
        if book.return_book(user):
            messages.success(request, "Book '{}' has been returned".format(str(book)))
        else:
            messages.error(request, "Book '{}' has not been returned".format(str(book)))
    else:
        if book.take_book(user):
            messages.success(request, "Book '{}' has been taken".format(str(book)))
        else:
            messages.error(request, "Book '{}' has not been taken".format(str(book)))
    return redirect('books:details', pk=book.pk)
