from django.db import models

class Contact(models.Model):
    """Contact documentation"""
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    # address = https://pypi.org/project/django-address/
    email = models.EmailField(max_length=254)
    # phone = https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    # skills

    def __str__(self):
        return self.firstname + " " + self.lastname