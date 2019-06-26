from rest_framework import serializers
from .models import Contact, Skill

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'level') #, 'contacts'

    def create(self, validated_data):
        # If skill.name-level combination already exists, update contacts only
        skill, created = Skill.objects.get_or_create(
            name=validated_data.get('name', None),
            level=validated_data.get('level', None),
            defaults={},
        )
        for new_contact in validated_data.get('contacts', None):
            skill.contacts.add(new_contact)
        return skill

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.created = validated_data.get('created', instance.created)
    #     return instance

class ContactSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('id', 'firstname', 'lastname', 'fullname', 'address', 'email', 'phone', 'skills')

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        contact = Contact.objects.create(**validated_data)
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data["name"],
                level=skill_data["level"],
                defaults={},
            )
            contact.skills.add(skill)
        return contact

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname
