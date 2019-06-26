from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
# from address.models import AddressField
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return self.username

class Contact(models.Model):
    """Contact documentation"""
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    # address = AddressField(on_delete=models.CASCADE, null=True, blank=True) #https://pypi.org/project/django-address/
    address = models.CharField(max_length=254)
    email = models.EmailField()
    # phone = PhoneNumberField()  #https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+99999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=16, validators=[phone_regex])
    # phone = models.CharField(max_length=16)

    owner = models.ForeignKey(
        User,
        related_name='contacts',
        on_delete=models.CASCADE,
        # null=True,  #Temporary until user login implemented
        # blank=True
    )

    def __str__(self):
        return self.firstname + " " + self.lastname

class Skill(models.Model):
    """Skill documentation"""
    name = models.CharField(max_length=254) #Add validator for lowercase
    level = models.PositiveIntegerField(default=1, blank=True, validators=[MinValueValidator(1)])  
    contacts = models.ManyToManyField(Contact, related_name='skills', blank=True)

    def __str__(self):
        return self.name
