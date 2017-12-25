from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
import re
from django.core import validators
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #extending user model
    teamname = models.CharField(max_length=200)
    idno = models.CharField(max_length=20,validators=[\
        validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P$'),message='Enter your valid BITS-mail',code='invalid!')])
    ip = models.CharField(null=True,max_length=20)

    def __str__(self):
        return self.teamname + "-" + self.idno


class Question(models.Model):
    question_text = RichTextField()

    def __str__(self):
        return "Question #" + str(self.pk)


class Code(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    code = RichTextField()
    lang = models.IntegerField(default=1)

    def __str__(self):
        return self.user + "-" + self.lang

