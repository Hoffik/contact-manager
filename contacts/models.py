from django.db import models
from django.core.validators import MinValueValidator

class Contact(models.Model):
    """Contact documentation"""
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    # address = https://pypi.org/project/django-address/
    email = models.EmailField(max_length=254)
    # phone = https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models

    def __str__(self):
        return self.firstname + " " + self.lastname

class Skill(models.Model):
    """Skill documentation"""
    name = models.CharField(max_length=254) #Add validator for lowercase
    level = models.PositiveIntegerField(default=1, blank=True, validators=[MinValueValidator(1)])  
    contacts = models.ManyToManyField(Contact)

    def __str__(self):
        return self.name