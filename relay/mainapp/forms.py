from django import forms
import re
from django.core import validators

class registerform(forms.Form):
	teamname = forms.CharField(max_length=50)
	password1 = forms.CharField(widget=forms.PasswordInput(),max_length=20)
	password2 = forms.CharField(widget=forms.PasswordInput(),max_length=20)
	id = forms.CharField(max_length=20,validators=[\
		validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P'),message='BITS ID of teammate 1 is empty or invalid',code='invalid!')])



