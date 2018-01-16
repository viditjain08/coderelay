from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Code)
admin.site.register(Question)
admin.site.register(GameSwitch)
admin.site.register(Team)
