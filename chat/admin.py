from django.contrib import admin

# Register your models here.
from chat.models import Chat,Message

class ChatAdmin(admin.ModelAdmin):
	# list_display = ['name']
	search_fields = ['participants','messages','name']
	readonly_fields = ['is_group']

	class Meta:
		model = Chat

admin.site.register(Chat,ChatAdmin)

class MessageAdmin(admin.ModelAdmin):
	search_fields = ['author','content']
	readonly_fields = ['timestamp']

	class Meta:
		model = Message

admin.site.register(Message,MessageAdmin)
