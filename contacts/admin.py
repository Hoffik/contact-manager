from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Contact, Skill

admin.site.unregister(Group)
admin.site.register(Contact)
admin.site.register(Skill)