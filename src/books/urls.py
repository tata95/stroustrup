from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list$', views.books_list, name='list'),
    url(r'^toggle/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.book_toggle_view, name='toggle'),
    url(r'^edit/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.EditBook.as_view(), name='edit'),
    url(r'^delete/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.book_delete, name='delete'),
    url(r'^create$', views.CreateBook.as_view(), name='create'),
    url(r'^view/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.book_details, name='details'),
]
