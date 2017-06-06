from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.BooksListView.as_view(), name='list'),
    url(r'^list$', views.BooksListView.as_view(), name='list'),
    url(r'^toggle/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.book_toggle_view, name='toggle'),
    url(r'^edit/(?P<pk>[0-9,a-z,A-Z]+)/$', views.EditBook.as_view(), name='edit'),
    url(r'^delete/(?P<pk>[0-9,a-z,A-Z]+)/$', views.DeleteBook.as_view(), name='delete'),
    url(r'^create$', views.CreateBook.as_view(success_url='list'), name='create'),
    url(r'^view/(?P<pk>[0-9,a-z,A-Z]+)/$', views.ViewBook.as_view(), name='details'),
    url(r'^upvote/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.vote_book, {'value': 1}, name='upvote'),
    url(r'^downvote/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.vote_book, {'value': -1}, name='downvote'),
    url(r'^block_comment/(?P<pk>[0-9,a-z,A-Z]+)/$', views.CommentBlock.as_view(), name='comment_block'),
    url(r'^unblock_comment/(?P<pk>[0-9,a-z,A-Z]+)/$', views.comment_unblock, name='comment_unblock'),
    url(r'^isbn_fetch$', views.isbn_info, name='isbn_fetch'),
    url(r'^tag/add/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.AddTag.as_view(), name='add_tag'),

    url(r'^file/add/(?P<isbn>[0-9]+)/$', views.AddBookFile.as_view(), name='add_file'),
    url(r'^file/edit/(?P<pk>[0-9]+)/$', views.EditBookFile.as_view(), name='edit_file'),
    url(r'^file/delete/(?P<pk>[0-9]+)/$', views.DeleteBookFile.as_view(), name='delete_file'),
]
