from rest_framework import viewsets
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Contact, Skill
from .serializers import ContactSerializer, SkillSerializer
from .forms import SignUpForm, ContactForm

# Application views
import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

class ContactFormView(FormView):
    template_name = 'contact_add.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:contact-list-view')

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

# Rest API views
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

    def perform_create(self, serializer):
        """Force contact owner to current user on save"""
        serializer.save(owner=self.request.user)

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