from django.db import models
from django.conf import settings
from django.utils import timezone

class FriendList(models.Model):
	user		= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user")	# if user is deleted then corresponds to this user Friedlist all record will be deleted
	friends 	= models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="friends")

	def __str__(self):
		return self.user.username



	def add_friend(self,account):
		if not account in self.friends.all():
			self.friends.add(account)

	def remove_friend(self,account):
		if account in self.friends.all():
			self.friends.remove(account)

	# above to functions are core function

	def unfriend(self,other):
		#remove friend from remover friend list
		self.remove_friend(other)

		#remove friend from "other" friend list
		friends_list = FriendList.objects.get(user=other)
		friends_list.remove_friend(self.user)

	def is_mutual_friend(self,friend):
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	sender		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
	receiver	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")
	is_active	= models.BooleanField(blank=True,null=False,default=True)
	timestamp	= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.sender.username

	def accept(self):
		receiver_friend_list = FriendList.objects.get(user=self.receiver)

		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		self.is_active = False
		self.save()

	def cancel(self):
		self.is_active = False
		self.save()


