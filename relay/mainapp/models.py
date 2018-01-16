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

class Team(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2', blank=True, null=True)
    time = models.IntegerField(default=0)
    enable = models.BooleanField(default=True)
    question = models.CharField(max_length=10,default="0000")
    def __str__(self):
        return self.user1.teamname


class Question(models.Model):
    question_text = RichTextField()

    def __str__(self):
        return "Question #" + str(self.pk)


class Code(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    code = models.TextField(max_length=2000)
    lang = models.IntegerField(default=1)

    def __str__(self):
        return self.user.ip + "-" + str(self.lang)

class GameSwitch(models.Model):
    name=models.CharField(null=False,max_length=10)
    game_active = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default = 0)

    def __str__(self):
        return self.name
