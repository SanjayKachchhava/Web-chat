from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib import settings
import json

from account.models import Account
from friend.models import FriendList
from chat.models import Chat
# from django.contrib.auth import get_user_model

def room(request,*args,**kwargs):

	if not request.user.is_authenticated:
		return HttpResponse("For chat with friend you must be authenticated");
	
	sender_id = request.user.id

	chat_id = kwargs.get('chat_id')
	try:
		chat = Chat.objects.get(pk=chat_id)
	except Chat.DoesNotExist:
		return HttpResponse("Something went wrong !! This chat does not exist !!")

	group_name = chat.name

	is_group = chat.is_group
	print(is_group)
	print(chat.id)

	receiver = None

	if not is_group:
		if chat.numberOfParticipant() == 2:
			receiver = chat.participants.all().exclude(username=request.user.username)[0]
			if sender_id == receiver.id:
				return HttpResponse("Something went wrong")
		else:
			return HttpResponse("Something went wrong")


	friends = FriendList.objects.get(user=request.user).friends.all()
	# if not request.user in FriendList.objects.get(user=receiver).friends.all():
	# 	return HttpResponse("You must be friends to chat with "+receiver.username)

	room_name = str(chat_id)
	
	# if sender_id > receiver_id:
	# 	room_name = str(receiver_id)+"_"+str(sender_id)	#   pattern : minvalue_maxvalue

	# print(sender_id)
	# print(receiver_id)
	# print(room_name)

	# all_chat = Chat.objects.all()
	chat_list = []	# [(chat1,receiver_username),(chat2,receiver_username),.....]

	for chat in Chat.objects.all():
		for user in chat.participants.all():
			if user == request.user:
				if chat.numberOfParticipant() == 2 and (not chat.is_group):
					chat_list.append((chat,chat.participants.all().exclude(username=user.username)[0]))
				else:
					chat_list.append((chat,False))


	# return HttpResponse("helllo world "+str(sender_id) +" "+ str(receiver_id))
	return render(request,'chat/chat.html',{
		'room_name':room_name,
		'receiver':receiver,
		'chat_list' : chat_list,
		'chat_id' : chat_id,
		'group_name' : group_name,
		'friends' : friends,
		})

def private_chat(request,receiver_id):
	user = request.user

	try:
		receiver = Account.objects.get(pk=receiver_id)
	except Account.DoesNotExist:
		return HttpResponse("Something went wrong !! Account does not exist ")

	receiver_friend_list = FriendList.objects.get(user=receiver)

	if not user in receiver_friend_list.friends.all():
		return HttpResponse("Something went wrong !! You must be friend with "+receiver.user.username)

	chat_id = None

	print(receiver)

	for chat in Chat.objects.all():
		if not chat.is_group:
			# print(chat.numberOfParticipant())
			if chat.numberOfParticipant() == 2:
				if (receiver in chat.participants.all()) and (request.user in chat.participants.all()):
						chat_id = chat.id

	if chat_id == None:
		chat = Chat.objects.create()
		chat.addParticipant(user)
		chat.addParticipant(receiver)
		chat.is_group = True
		chat_id = chat.id

	print(receiver.username+ " : "+str(chat_id))

	return redirect("chat:room",chat_id=chat_id)


def create_group(request):
	payload = {}
	user = request.user

	if request.method == "POST" and user.is_authenticated:
		try:
			print(request.POST.getlist('usernames[]'))
			username_list = request.POST.getlist('usernames[]')
			group_name = request.POST.get('group_name')
			# print("username list :"+username_list)
		
			chat = Chat.objects.create()
			chat.addParticipant(user)
			chat.add_admin(user)
			chat.name = group_name
			chat.is_group = True
			chat_id = chat.id
			chat.save()

			user_friend_list = FriendList.objects.get(user=user)

			for username in username_list:
				try:
					participant = Account.objects.get(username=username)
					if not participant in user_friend_list.friends.all():
						continue
				except Account.DoesNotExitst:
					continue

				if chat_id:
					chat.addParticipant(participant)

			payload['chat_id'] = chat_id
			payload['result'] = "success";

			print(chat.is_group)
			print(chat.id)

		except Exception as e:
			payload['result'] = "error"
			payload['exception'] = str(e)


	return HttpResponse(json.dumps(payload),content_type="application/json")

def group_view(request,*args,**kwargs):
	context = {}

	chat_id = kwargs.get('chat_id')
	
	

	if not request.user.is_authenticated:
		return redirect("login")
	try:
		chat = Chat.objects.get(pk=chat_id)
	except Chat.DoesNotExist:
		return HttpResponse("Something went wrong !! chat does not exist")

	if not chat.is_group:
		return HttpResponse("Something went wrong")

	context['chat'] = chat
	context['admins'] = chat.admin.all()

	participants = chat.participants.all()

	context['participants'] = participants

	return render(request,'chat/group.html',context)


