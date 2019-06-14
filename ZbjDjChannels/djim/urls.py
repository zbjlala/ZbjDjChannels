from django.conf.urls import url

from djim import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>[^/]+)/$', views.djim, name='djim'),
]