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
        contacts = validated_data.get('contacts', None)
        current_user = self.context['request'].user
        for new_contact in validated_data.get('contacts', None):
            if new_contact.owner == current_user:
                skill.contacts.add(new_contact)
        return skill

    def update(self, instance, validated_data):
        contacts = validated_data.get('contacts', [])
        if len(contacts)==0:
            # In case no contact is provided nothing happens.
            return instance
        new_name = validated_data.get('name', None)
        new_level = validated_data.get('level', None)
        current_user = self.context['request'].user
        if new_name is None and new_level is None:
            # In case basic parameters name and level are not provided each contact from the list has the skill removed.
            for contact in contacts:
                if contact.owner == current_user:
                    instance.contacts.remove(contact)
        else:
            # Each contact from the provided list of contacts has the skill (name and/or level) updated (new skill is created if necessary).
            skill, created = Skill.objects.get_or_create(
                name=new_name or instance.name, #If new_value is None, keep original value
                level=new_level or instance.name,
                defaults={},
            )
            for contact in contacts:
                if contact.owner == current_user:
                    instance.contacts.remove(contact)                
                    skill.contacts.add(contact)
        if len(instance.contacts.all())==0:
            # Original skill is removed if it has no contact left.
            instance.delete()
        return instance

class ContactSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'owner', 'firstname', 'lastname', 'fullname', 'address', 'email', 'phone', 'skills')

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname
