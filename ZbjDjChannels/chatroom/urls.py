from django.conf.urls import url

from chatroom import views

urlpatterns = [
    url('', views.index, name='index'),
   # url('<str: room_name>/', views.room, name='room'),
]