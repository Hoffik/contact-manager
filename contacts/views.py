from rest_framework import viewsets
from .models import Contact, Skill
from .serializers import ContactSerializer, SkillSerializer

class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit contacts.

    retrieve:
        Return a contact instance.

    list:
        Return all contacts, ordered by most recently joined.

    create:
        Create a new contact.

    delete:
        Remove an existing contact.

    partial_update:
        Update one or more fields on an existing contact.

    update:
        Update a contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit skills.

    retrieve:
        Return a skill instance.

    list:
        Return all skills, ordered by most recently joined.

    create:
        Create a new skill.

    delete:
        Remove an existing skill.

    partial_update:
        Update one or more fields on an existing skill.

    update:
        Update a skill.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer