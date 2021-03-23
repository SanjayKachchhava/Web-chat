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
	name        		= models.CharField(max_length=30,blank=True)
	admin				= models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="group_admin") 

	def addMessage(self,message):
		self.messages.add(message)

	def addParticipant(self,user):
		if self.is_group or (not self.is_group and self.numberOfParticipant() < 2):
			self.participants.add(user)

	def removeParticipant(self,user):
		if user in self.participants.all():
			self.participants.remove(user)

	def deleteMessage(self,message):
		if message in self.messages.all():
			self.messages.remove(message)

	def getChatProfPicUrl(self,username):
		user = settings.AUTH_USER_MODEL.objects.get(username=username)
		if not self.is_group:
			if self.numberOfParticipant() == 2:
				receiver = self.participants.all().exclude(user=user)[0]
				return receiver.profile_image.url
		else:
			return "media/profile/def_prof_pic.png"

	def change_name(self,name):
		self.name = name
		self.save()

	def is_participant(self,user):
		if user in self.participants.all():
			return True
		return False


	def add_admin(self,user):
		if not user in self.admin.all():
			self.admin.add(user)


	def removeParticipant(self,user):
		self.participants.remove(user)

	def numberOfParticipant(self):
		return self.participants.all().count()

	def last_10_messages(self):
		return self.messages.all().order_by('-timestamp')[:10]

	def __str__(self):
		return str(self.pk)



# def get_profile_image_filepath(self,filename):
# 	return f'group_profile_images/{self.pk}/{"profile_image.png"}'

# def get_default_profile_image():
# 	return "group_profile_images/def_prof_pic.png"

# class Group(models.Model):
# 	chat 			= models.OneToOneField(Chat,on_delete=models.CASCADE,related_name='chat')
# 	name        	= models.CharField(max_length=30,unique=False,blank=False)
# 	profile_image 	= models.ImageField(max_length=255,upload_to=get_profile_image_filepath,null=True,blank=True,default=get_default_profile_image)
# 	admin			= models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="admin")

	# def add_admin(self,user):
	# 	if not user in self.admin.all():
	# 		self.admin.add(user)

# 	def __str__(self):
# 		return self.name

