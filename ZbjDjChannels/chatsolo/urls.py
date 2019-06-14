from django.conf.urls import url

from chatsolo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>[^/]+)/$', views.soloroom, name='soloroom'),
]