from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Contact, Skill

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Skill)