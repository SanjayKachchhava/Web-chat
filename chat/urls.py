from django.urls import path,include

from . import views

app_name = 'chat'

urlpatterns = [
	path('private/chat/<int:receiver_id>/',views.private_chat,name='private_chat'),
	path('group/',views.create_group,name='create_group'),
	path('group_view/<int:chat_id>/',views.group_view,name='group_view'),
    path('<int:chat_id>/',views.room,name='room'),
]
