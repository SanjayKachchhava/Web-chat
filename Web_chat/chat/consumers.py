from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message,Chat
from account.models import Account
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):


	async def fetch_messages(self,data):

		try:
			chat = await sync_to_async(Chat.objects.get,thread_sensitive=True)(pk=data['chat_id'])
		except Chat.DoesNotExist:
			pass

		messages = await sync_to_async(chat.last_10_messages,thread_sensitive=True)()
		# print(messages)
		content = {
			'command' : 'fetch_messages',
			'messages' : await sync_to_async(self.messages_to_json,thread_sensitive=True)(messages)
		}

		await self.send_messages(content)


	async def new_message(self,data):

		author = data['author']

		try:
			author_user = await sync_to_async(Account.objects.get, thread_sensitive=True)(username=author)	 
		except Account.DoesNotExist:
			pass

		try:
			chat = await sync_to_async(Chat.objects.get,thread_sensitive=True)(pk=data['chat_id'])
		except Chat.DoesNotExist:
			pass

		if not await sync_to_async(chat.is_participant,thread_sensitive=True)(author_user):
			pass

		
		message = await sync_to_async(Message.objects.create,thread_sensitive=True)(
			author = author_user,
			content = data['message']
			)

		await sync_to_async(chat.addMessage,thread_sensitive=True)(message)

		content = {
			'command' : 'new_message',
			'message': self.message_to_json(message),
		}


		await self.send_to_group(content)
		

	commands = {
		'fetch_messages' : fetch_messages,
		'new_message' : new_message
	}

	def messages_to_json(self,messages):
		message_list = []
		for message in messages:
			message_list.append(self.message_to_json(message))

		return message_list

	def message_to_json(self,message):
		return {
			'author' : message.author.username,
			'content' : message.content,
			'profile_url' : message.author.profile_image.url,
			'timestamp' : str(message.timestamp),
		}


	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		username = (self.scope['user']).username
		# print(self.room_name)
		# print(self.room_group_name)

		# add user to specific group:
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()			# must be accept or reject

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'connect_message',
				'message' : 'has been join the chat',
				'author' : username,
			}
		)
		
		

	async def connect_message(self,event):
		message = event['message']
		username= event['author']

		await self.send(text_data=json.dumps({
				'command' : "connect_message",
				'message' : message,
				'author' : username,
			}))


	async def disconnect(self,close_code):
		
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		
	#receive messages from websocket
	async def receive(self,text_data):
		data = json.loads(text_data)

		await self.commands[data['command']](self,data)

		# message = data['message']
		# username = data['username']

	#send message to room group
	async def send_to_group(self,message):
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type' : 'room_message',
				'message' : message,
			}
		)
	
	# messages received from room group
	async def room_message(self,event):
		message = event['message']
		# print('room_message : '+message)
		await self.send(text_data=json.dumps(message))

	async def send_messages(self,message):
		await self.send(text_data=json.dumps(message))


