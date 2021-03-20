from django.db import models
from django.conf import settings


class Message(models.Model):
	author		= models.ForeignKey(settings.AUTH_USER_MODEL,related_name="author",on_delete=models.CASCADE)
	content		= models.TextField()
	timestamp	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username


class Chat(models.Model):
	participants		= models.ManyToManyField(settings.AUTH_USER_MODEL)
	messages			= models.ManyToManyField(Message,blank=True)
	is_group			= models.BooleanField(default=False)

	def addMessage(self,message):
		self.messages.add(message)

	def addParticipant(self,user):
		if self.is_group or (not self.is_group and self.numberOfParticipant() < 2):
			self.participants.add(user)

	def getChatProfPicUrl(self,username):
		user = settings.AUTH_USER_MODEL.objects.get(username=username)
		if not self.is_group:
			if self.numberOfParticipant() == 2:
				receiver = self.participants.all().exclude(user=user)[0]
				return receiver.profile_image.url
		else:
			return "media/profile/def_prof_pic.png"

	def is_participant(self,user):
		if user in self.participants.all():
			return True
		return False


	def removeParticipant(self,user):
		self.participants.remove(user)

	def numberOfParticipant(self):
		return self.participants.all().count()

	def last_10_messages(self):
		return self.messages.all().order_by('-timestamp')[:10]

	def __str__(self):
		return str(self.pk)