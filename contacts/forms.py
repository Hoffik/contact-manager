from django import forms
from django.contrib.auth.forms import UserCreationForm
from djng.forms import fields, NgFormValidationMixin, NgModelFormMixin, NgModelForm, NgForm
# from djng.styling.bootstrap3.forms import Bootstrap3Form
from .models import Contact, Skill, User

class ContactForm(NgFormValidationMixin, NgModelForm):  #forms.ModelForm
    scope_prefix = 'contact'
    form_name = 'contact_form'

    class Meta:
        model = Contact
        fields = ('firstname', 'lastname', 'address', 'email', 'phone')

class SkillForm(NgFormValidationMixin, NgModelForm):  #forms.ModelForm
    scope_prefix = 'skill'
    form_name = 'skill_form'

    class Meta:
        model = Skill
        fields = ('name', 'level')

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
