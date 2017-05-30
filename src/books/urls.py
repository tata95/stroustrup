from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.books_list, name='list'),
    url(r'^list$', views.books_list, name='list'),
    url(r'^toggle/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.book_toggle_view, name='toggle'),
    url(r'^edit/(?P<pk>[0-9,a-z,A-Z]+)/$', views.EditBook.as_view(), name='edit'),
    url(r'^delete/(?P<pk>[0-9,a-z,A-Z]+)/$', views.DeleteBook.as_view(), name='delete'),
    url(r'^create$', views.CreateBook.as_view(success_url='list'), name='create'),
    url(r'^view/(?P<pk>[0-9,a-z,A-Z]+)/$', views.ViewBook.as_view(), name='details'),
]
