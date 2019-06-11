from rest_framework import serializers
from .models import Contact, Skill

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'firstname', 'lastname', 'fullname', 'email',)

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname

class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'level',)