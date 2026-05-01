from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('channel/<int:channel_id>/', views.channel_room, name='channel_room'),
    path('dm/start/<int:user_id>/', views.start_dm, name='start_dm'),
    path('join/<int:channel_id>/', views.join_channel, name='join_channel'),
    path('channel/<int:channel_id>/send/', views.send_attachment, name='send_attachment'),
]