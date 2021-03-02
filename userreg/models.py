from django.db import models

# Create your models here.


class user_details(models.model):
	user_id=models.IntegerField(primary_key=True)
	user_name = models.CharField(max_length=20)
    	email_id = models.IntegerField(max_length=20)
    	birth_date = models.DateTimeField('date published')
    	gender_choices=[
        	('male',"Male"),
        	("female","Female"),
    	]
    	gender = models.CharField(
        	max_length=6, blank=True, null=True,
        	choices=gender_choices,
        	)
    
    	def __str__(self):
        	return self.name