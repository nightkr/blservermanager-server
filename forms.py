from django.core import validators
from django import forms
from blmanager import models
import re

class AdminKeyValidator(validators.RegexValidator):
	def __call__(self, value):
		super(AdminKeyValidator, self).__call__(value)
		if value not in models.servers_and_webclients:
			raise validators.ValidationError(self.message, code=self.code)

class AdminKeyField(forms.CharField):
	def __init__(self, *args, **kwargs):
		kwargs['error_messages'] = kwargs.get('error_messages') or {}
		kwargs['error_messages']['invalid'] = "Please enter a valid key."
		super(AdminKeyField, self).__init__(*args, **kwargs)
		self.regex = re.compile("(\{){0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}(\}){0,1}")
		self.validators.append(AdminKeyValidator(regex=self.regex))

class AdminKeyInputForm(forms.Form):
	key = AdminKeyField()
