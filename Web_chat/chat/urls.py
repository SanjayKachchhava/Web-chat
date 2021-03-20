from django.urls import path,include

from . import views

app_name = 'chat'

urlpatterns = [
	path('private/chat/<int:receiver_id>/',views.private_chat,name='private_chat'),
    path('<int:chat_id>/',views.room,name='room'),
]
