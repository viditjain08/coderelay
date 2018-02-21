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
    name = models.CharField(max_length=50)
    idno = models.CharField(max_length=20)
    ip = models.CharField(null=True,max_length=20)

    def __str__(self):
        return self.teamname + "-" + self.idno


class Question(models.Model):
    heading = models.TextField(max_length=200, default='')
    question_text = RichTextField()

    def __str__(self):
        return "Question #" + str(self.pk)

class Team(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2', blank=True, null=True)
    time = models.IntegerField(default=0)
    enable = models.BooleanField(default=True)
    user1q = models.ForeignKey(Question, related_name='user1q', blank=True, null=True)
    user2q = models.ForeignKey(Question, related_name='user2q', blank=True, null=True)
    swap = models.BooleanField(default=False)
    def __str__(self):
        return self.user1.teamname




class Code(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    code = models.TextField(max_length=2000)
    lang = models.IntegerField(default=4)
    swap = models.BooleanField(default=False)

    def __str__(self):
        return self.team.user1.teamname + "-" + str(self.lang)

class GameSwitch(models.Model):
    name=models.CharField(null=False,max_length=10)
    game_active = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default = 0)

    def __str__(self):
        return self.name
