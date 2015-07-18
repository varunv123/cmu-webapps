from django import forms

from django.contrib.auth.models import User
from datetime import datetime
#from django_google_maps import fields as map_fields
from models import *
forms.TimeInput.input_type = "time"
forms.DateInput.input_type="date"
forms.DateTimeInput.input_type="datetime" 


class RegistrationForm(forms.Form):
	username = forms.CharField(max_length = 20,
				widget = forms.TextInput(attrs={'placeholder':"Username"}))
	email = forms.CharField(max_length = 40,
			widget = forms.EmailInput(attrs={'placeholder':"Email"}))
	password1 = forms.CharField(max_length = 200,
								label = "Password",
	widget = forms.PasswordInput(attrs={'placeholder':"Enter Password"}))
	password2 = forms.CharField(max_length = 200,
								label = "Confirm Password",
	widget = forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__exact=email):
			raise forms.ValidationError("Email is already taken.")
		return email

class LocationWidget(forms.TextInput):
	class Media:
		js = ('geo.js')

class GroupForm(forms.Form):
	groupName = forms.CharField(max_length=35, label='Name:',
					widget = forms.TextInput(attrs={'placeholder':"Group Name"}))
	def clean(self):
		cleaned_data = super(GroupForm,self).clean()
		return cleaned_data

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ('user','invitedUsers')
		widgets = {
			'location': LocationWidget(attrs={'id':"autocomplete"})
		}

class SearchForm(forms.Form):
	searchfield = forms.CharField(max_length = 42,
			widget = forms.TextInput(attrs={'placeholder':"Search"}))
	def clean(self):
		cleaned_data = super(SearchForm,self).clean()
		return cleaned_data


class ChangeEmailForm(forms.Form):
	email1 = forms.CharField(max_length = 40,
			widget = forms.EmailInput(attrs={'placeholder':"New Email"}))
	email2 = forms.CharField(max_length = 40,
			widget = forms.EmailInput(attrs={'placeholder':"New Email"}))
	def clean(self):
		cleaned_data = super(ChangeEmailForm,self).clean()
		email1 = cleaned_data.get('email1')
		email2 = cleaned_data.get('email2')
		if email1 and email2 and email1 != email2:
			raise forms.ValidationError("Emails do not match")
		return cleaned_data

class ChangePasswordForm(forms.Form):
	oldpassword = forms.CharField(max_length = 200,
								label = "OldPassword",
	widget = forms.PasswordInput(attrs={'placeholder':"Old Password"}))
	password1 = forms.CharField(max_length = 200,
								label = "Password",
	widget = forms.PasswordInput(attrs={'placeholder':"New Password"}))
	password2 = forms.CharField(max_length = 200,
								label = "Password",
	widget = forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

class PictureForm(forms.Form):
	picture = forms.FileField(widget=forms.FileInput(),required=False)
	def clean(self):
		cleaned_data = super(PictureForm,self).clean()
		return cleaned_data

class PasswordResetForm(forms.Form):
	email = forms.CharField(max_length = 40,
			widget = forms.EmailInput(attrs={'placeholder':"Email"}))
	def clean(self):
		cleaned_data = super(PasswordResetForm,self).clean()
		return cleaned_data

class ResetChangePasswordForm(forms.Form):
	password1 = forms.CharField(max_length = 200,
								label = "Password",
	widget = forms.PasswordInput(attrs={'placeholder':"New Password"}))
	password2 = forms.CharField(max_length = 200,
								label = "Password",
	widget = forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
	def clean(self):
		cleaned_data = super(ResetChangePasswordForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data


