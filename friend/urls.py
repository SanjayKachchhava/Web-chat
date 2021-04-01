from django.urls import path

from friend.views import(
	send_friend_request,
	friend_requests_view,
	accept_friend_request,
	remove_friend,
	decline_friend_request,
	cancel_friend_request,
	friend_list_view,
)

app_name = "friend"

urlpatterns = [
	path('list/<user_id>/',friend_list_view,name="list"),
	path('remove_friend/',remove_friend,name="remove_friend"),
	path('friend_request/',send_friend_request,name="friend_request"),
	path('friend_request/<user_id>/',friend_requests_view,name="friend_requests_view"),
	path('accept_friend_request/<friend_request_id>/',accept_friend_request,name="accept_friend_request"),
	path('decline_friend_request/<friend_request_id>/',decline_friend_request,name="decline_friend_request"),
	path('cancel_friend_request/',cancel_friend_request,name="cancel_friend_request"),
]