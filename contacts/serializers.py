from rest_framework import serializers
from .models import Contact, Skill

class SkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    level = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'level', 'contacts')

    def create(self, validated_data):
        # If skill.name-level combination already exists, add new contacts only
        skill, created = Skill.objects.get_or_create(
            name=validated_data.get('name', None),
            level=validated_data.get('level', None),
            defaults={},
        )
        for new_contact in validated_data.get('contacts', None):
            skill.contacts.add(new_contact)
        return skill

    def update(self, instance, validated_data):
        contacts = validated_data.get('contacts', [])
        if len(contacts)==0:
            # In case no contact is provided nothing happens.
            return instance
        new_name = validated_data.get('name', None)
        new_level = validated_data.get('level', None)
        if new_name is None and new_level is None:
            # In case basic parameters name and level are not provided each contact from the list has the skill removed.
            for contact in contacts:
                instance.contacts.remove(contact)
        else:
            # Each contact from the provided list of contacts has the skill (name and/or level) updated (new skill is created if necessary).
            skill, created = Skill.objects.get_or_create(
                name=new_name,
                level=new_level,
                defaults={},
            )
            for contact in contacts:
                instance.contacts.remove(contact)                
                skill.contacts.add(contact)
        if len(instance.contacts.all())==0:
            # Original skill is removed if it has no contact left.
            instance.delete()
        return instance

class ContactSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    # skills = SkillSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('id', 'firstname', 'lastname', 'fullname', 'address', 'email', 'phone', 'skills')

    # def create(self, validated_data):
    #     skills_data = validated_data.pop('skills')
    #     contact = Contact.objects.create(**validated_data)
    #     for skill_data in skills_data:
    #         skill, created = Skill.objects.get_or_create(
    #             name=skill_data["name"],
    #             level=skill_data["level"],
    #             defaults={},
    #         )
    #         contact.skills.add(skill)
    #     return contact

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname
