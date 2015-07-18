from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import time
from django.contrib.auth.models import User
from datetime import datetime,date

#Event is a given entry for a day
class Event(models.Model):
	user = models.ForeignKey(User)
	startTime = models.TimeField(default=datetime.now().time())
	startDate = models.DateField(default=datetime.now().date())
	endTime = models.TimeField(default=datetime.now().time())
	endDate = models.DateField(default=datetime.now().date())
	location = models.CharField(max_length=100)
	invitedUsers = models.ManyToManyField(User,related_name="invitedUsers")
	def __unicode__(self):
		return self.location

	@staticmethod
	def get_events(user):
		return Event.objects.filter(user=user)
	
	def getEventName(self):
		return self.location.split(',')[0]


# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField(upload_to="profile-pics",blank=True)

class Follow(models.Model):
	follower = models.ForeignKey(User,related_name='followers')
	followee = models.ForeignKey(User,related_name='followees')

class Block(models.Model):
	blocker = models.ForeignKey(User,related_name="blockers")
	blockee = models.ForeignKey(User,related_name="blockees")

class Group(models.Model):
	owner = models.ForeignKey(User)	
	groupName = models.CharField(max_length=50)
	groupUsers = models.ManyToManyField(User, related_name="groupUsers")



