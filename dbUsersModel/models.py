from django.db import models

# Create your models here.

class userInfo(models.Model):
	name = models.CharField(max_length=20)
	birthday = models.DateField()