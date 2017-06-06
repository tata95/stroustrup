from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^me$', views.ShowProfile.as_view(), name='show_self'),
    url(r'^me/edit$', views.EditProfile.as_view(), name='edit_self'),
    url(r'^(?P<slug>[\w\-]+)$', views.ShowProfile.as_view(),
        name='show'),

    url(r'^readlist/(?P<isbn>[0-9,a-z,A-Z]+)/$', views.readlist_add_remove, name='readlist_toggle'),
]
