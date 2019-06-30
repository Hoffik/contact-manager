from rest_framework import viewsets
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from .models import Contact, Skill
from .serializers import ContactSerializer, SkillSerializer
from .permissions import ContactPermission, SkillPermission
from .forms import SignUpForm

# Application views
class ContactListView(LoginRequiredMixin, TemplateView):
    template_name = "contact_list.html"

class ContactDetailView(LoginRequiredMixin, TemplateView):
    template_name = "contact_detail.html"

# Authentication views
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('contacts:contact-list-view')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return HttpResponse("Your username is %s." % request.user.username)

def empty_view(request):
    return redirect('contacts:contact-list-view')

# # Rest API views
class ContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit contacts.

    retrieve:
        Return a contact instance.
        All authenticated users can read any contact.

    list:
        Return all contacts, ordered by most recently joined.
        All authenticated users can read all contacts.

    create:
        Create a new contact.
        All authenticated users can create new contacts.

    delete:
        Remove an existing contact.
        User must have owner or administrator rights to delete a contact.

    partial_update:
        Update one or more fields on an existing contact.
        User must have owner or administrator rights to update a contact.

    update:
        Update a contact.
        User must have owner or administrator rights to update a contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (ContactPermission, )

    def perform_create(self, serializer):
        """Force contact owner to current user on save."""
        serializer.save(owner=self.request.user)

class SkillViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit skills.

    retrieve:
        Return a skill instance.
        All authenticated users can read any skill.

    list:
        Return all skills, ordered by most recently joined.
        All authenticated users can read all skills.

    create:
        Create a new skill.
        Creates a new skill for each contact in the contact list.
        User must be owner of a contact or administrator to create a skill for the contact.

    delete:
        Remove an existing skill.
        Removes skill reference from each contact and deletes the skill.
        User must have administrator rights to delete a skill.

    partial_update:
        Update one or more fields on an existing skill.
        Updates the skill name and/or level for each contact in the contact list.
        In case name and level parameters are not provided each contact from the list has the skill removed.
        User must be owner of a contact or administrator to update or remove a skill from the contact.

    update:
        Update a skill.
        Updates the skill name and level for each contact in the contact list.
        In case name and level parameters are not provided each contact from the list has the skill removed.
        User must be owner of a contact or administrator to update or remove a skill from the contact.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (SkillPermission, )
