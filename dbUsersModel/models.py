from django.db import models

# Create your models here.

class userInfo(models.Model):
	name = models.CharField(max_length=20)
	# birthday = models.DateField()

	user_pass = models.CharField(max_length=50, default=None)
	user_roleID = models.IntegerField(default=None)
	user_grade = models.CharField(max_length=40, null=True)
	user_class = models.CharField(max_length=40, null=True)
	user_gender = models.BooleanField(default=1)
	submission_date = models.DateField(auto_now=True)



# class Contact(models.Model):
#     name   = models.CharField(max_length=200)
#     age    = models.IntegerField(default=0)
#     email  = models.EmailField()
#     def __unicode__(self):
#         return self.name

# class Tag(models.Model):
# 	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
# 	name    = models.CharField(max_length=50)
# 	def __unicode__(self):
# 		return self.name