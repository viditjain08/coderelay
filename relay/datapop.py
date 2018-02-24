from mainapp.models import *

t = Team.objects.all()
for obj in t:
    obj.enable = True
    obj.save()

