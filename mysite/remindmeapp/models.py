from django.db import models

# Create your models here.
class Reminder(models.Model):
	pid = models.CharField(max_length=60)
	txt = models.CharField(max_length=60)
	indx = models.CharField(max_length=60)
	#date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.txt