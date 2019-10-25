from __future__ import unicode_literals
from django.db import models
import re
import datetime
import random
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def user_validator(self, postData):
		errors = {}
		#all 
		if len(postData['fname']) < 1 and len(postData['lname']) < 1  and len(postData['username']) < 1 and len(postData['password']) < 1:
			errors['form'] = 'Please fill out form'
			return errors
		else: 
			#name
			if len(postData['fname']) < 1:
				errors['fname'] = 'Please enter a first name'
			if len(postData['fname']) < 3:
				errors['fname'] = 'First name must be at least 2 characters'
			if len(postData['lname']) < 1:
				errors['lname'] = 'Please enter a last name'
			if len(postData['lname']) < 3:
				errors['lname'] = 'Last name must be at least 2 characters'		

			#dojo key
			if len(postData['dojokey']) < 1:
				errors['dojokey'] = 'Pleae enter a dojo Key'
			if postData['dojokey'] != 'dojo1' and postData['dojokey'] != 'dojo2' and postData['dojokey'] != 'dojo3' and postData['dojokey'] != 'NickIsTheGreatest':
				errors['dojokey'] = 'Invalid dojo key'

			#username
			if len(postData['username']) < 1:
				errors['username'] = 'Please enter an username'
			if len(postData['username']) < 4:
				errors['username'] = 'Username must be at least 3 characters'
			if len(User.objects.filter(username = postData['username'])) > 0:
				errors['username'] = 'username already taken'

			#password
			if len(postData['password']) < 1:
				errors['password'] = 'Please enter a password'	 
			if len(postData['password']) < 8:
				errors['password'] = 'Password must be at least 8 characters long'
			if postData['password'] != postData['password_confirm']:
				errors['password'] = 'Your passwords do not match'
			return errors

	def login_validator(self, postData):
		errors = {}
		if len(postData['username']) < 1 and len(postData['password']) < 1:
			errors['form'] = 'Please fill out form'
			return errors
		else: 
			if len(User.objects.filter(username = postData['username'])) == 0:
				errors['username'] = 'Invalid username'
			else:
				current_user = User.objects.get(username = postData['username'])
				if bcrypt.checkpw(postData['password'].encode(), current_user.password.encode()) != True:
					errors['password'] = 'Incorrect password'
			return errors

class PostManager(models.Manager):
	def post_validator(self, postData):
		errors = {}
		if len(postData['content']) < 1:
			errors['content'] = 'No empty posts'
		return errors

class CommentManager(models.Manager):
	def comment_validator(self, postData):
		errors = {}
		if len(postData['content']) < 1:
			errors['content'] = 'No empty comments'
		return errors

class EventManager(models.Manager):
	def event_validator(self, postData):
		errors = {}
		if len(postData['content']) < 1:
			errors['content'] = 'Please enter a description'
		current_time = str(datetime.datetime.now())
		startdate = postData['startdate']
		if current_time > startdate:
			errors['startdate'] = 'Invalid start date'
		return errors

class User(models.Model):
	fname = models.CharField(max_length = 255)
	lname = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	dojokey = models.CharField(max_length = 255)
	balance = models.IntegerField(default=300)
	following = models.ManyToManyField('self', related_name = 'followers')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	is_admin = models.BooleanField(default = False)
	objects = UserManager()

class Farm(models.Model):
	size = models.IntegerField()
	user = models.OneToOneField(User, related_name="farm", on_delete = models.CASCADE, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
		

class Badge(models.Model):
	name = models.CharField(max_length = 255)
	desc = models.CharField(max_length = 255)
	user = models.ManyToManyField(User, related_name = 'badges')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Crop(models.Model):
	name = models.CharField(max_length = 255)
	desc = models.CharField(max_length = 255)
	bPrice = models.IntegerField()
	sPrice = models.IntegerField()
	gRate = models.IntegerField()
	output = models.IntegerField()
	user = models.ForeignKey(User, related_name = 'crops', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'crops', on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)


class Post(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User, related_name = 'posts', on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = PostManager()
		
class Comment(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
	post = models.ForeignKey(Post, related_name = 'posts', on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = CommentManager()

class Event(models.Model):
	name = models.CharField(max_length=255, null = True)
	content = models.TextField(null = True)
	uploader = models.ForeignKey(User, related_name = 'my_plans', on_delete = models.CASCADE, null = True)
	attender = models.ManyToManyField(User, related_name = 'plans', null = True)
	startdate = models.DateField(null = True)
	starttime = models.TimeField(null = True)
	enddate = models.DateField(null = True)
	endtime = models.TimeField(null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = EventManager()

###########################@###########################@###########################@###########################@

class Seed(models.Model):
	name = models.CharField(max_length = 255)
	desc = models.CharField(max_length = 255)
	bPrice = models.IntegerField()
	gRate = models.IntegerField()
	isReady = models.IntegerField(default = 0)
	output = models.IntegerField()
	isPlanted = models.BooleanField(default = False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	class Meta:
		abstract = True

class Crop(models.Model):
	name = models.CharField(max_length = 255)
	desc = models.CharField(max_length = 255)
	sPrice = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	class Meta:
		abstract = True

class CornSeed(Seed):
	name = 'Corn Seed'
	desc = 'A seed for corn'
	bPrice = 1
	gRate = 100
	output = random.randint(1, 3)
	user = models.ForeignKey(User, related_name = 'cornSeed', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'cornSeed', on_delete = models.CASCADE)

class Corn(Crop):
	name = 'Corn'
	desc = 'An ear of Corn'
	sPrice = 2
	user = models.ForeignKey(User, related_name = 'corn', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'corn', on_delete = models.CASCADE)

class WheatSeed(Seed):
	name = 'Wheat Seed'
	desc = 'A seed for wheat'
	bPrice = 1
	gRate = 50
	output = random.randint(1, 3)
	user = models.ForeignKey(User, related_name = 'wheatSeed', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'wheatSeed', on_delete = models.CASCADE)

class Wheat(Crop):
	name = 'Wheat'
	desc = 'An ear of Wheat'
	sPrice = 4
	user = models.ForeignKey(User, related_name = 'wheat', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'wheat', on_delete = models.CASCADE)

class CarrotSeed(Seed):
	name = 'Carrot Seed'
	desc = 'A seed for carrots'
	bPrice = 2
	gRate = 50
	output = random.randint(1, 3)
	user = models.ForeignKey(User, related_name = 'carrotSeed', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'carrotSeed', on_delete = models.CASCADE)

class Carrot(Crop):
	name = 'Carrot'
	desc = 'A Carrot'
	sPrice = 5
	user = models.ForeignKey(User, related_name = 'carrot', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'carrot', on_delete = models.CASCADE)

class LeekSeed(Seed):
	name = 'Leek Seed'
	desc = 'A seed for leeks'
	bPrice = 3
	gRate = 20
	output = random.randint(1, 3)
	user = models.ForeignKey(User, related_name = 'leekSeed', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'leekSeed', on_delete = models.CASCADE)

class Leek(Crop):
	name = 'Leek'
	desc = 'A Leek'
	sPrice = 9
	user = models.ForeignKey(User, related_name = 'leek', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'leek', on_delete = models.CASCADE)

class BlackTomatoSeed(Seed):
	name = 'Black Tomato Seed'
	desc = 'A seed for black tomatos'
	bPrice = 10
	gRate = 10
	output = random.randint(1, 3)
	user = models.ForeignKey(User, related_name = 'blackTomatoSeed', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'blackTomatoSeed', on_delete = models.CASCADE)

class BlackTomato(Crop):
	name = 'Black Tomato'
	desc = 'A Black Tomato'
	sPrice = 30
	user = models.ForeignKey(User, related_name = 'blackTomato', on_delete = models.CASCADE)
	farm = models.ForeignKey(Farm, related_name = 'blackTomato', on_delete = models.CASCADE)