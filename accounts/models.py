from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile2.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Capacity(models.Model):
	capacity = models.IntegerField(null=True)

	def __(self):
		return self.capacity


class Slot(models.Model):
	events = (
			('Enter', 'Enter'),
			('Exit', 'Exit'),
			)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	event_type = models.CharField(max_length=200, null=True, choices= events)
	date_happened = models.DateTimeField(auto_now_add=True, null=True)
	slot_num = models.IntegerField(null=True)

	def __str__(self):
		return self.event_type

