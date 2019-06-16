from rest_framework import serializers
from .models import Contact, Skill

class ContactSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'firstname', 'lastname', 'fullname', 'address', 'email', 'phone', 'skills')

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'level', 'contacts')