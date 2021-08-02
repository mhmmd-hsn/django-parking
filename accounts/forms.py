from django.forms import ModelForm
from .models import Slot, Customer, Capacity
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SlotForm(ModelForm):
	class Meta:
		model = Slot
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


class Change_Capacity(ModelForm):
	class Meta:
		model = Capacity
		fields = '__all__'