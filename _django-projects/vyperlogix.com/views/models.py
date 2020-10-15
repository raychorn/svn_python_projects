from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

from django.contrib import admin

class Product(models.Model):
    name = models.CharField('Product Name', max_length=30)
    version = models.CharField('Version', max_length=10)

    class Admin:
        pass
    
    def __str__(self):
        return self.name

admin.site.register(Product)

class Country(models.Model):
    iso = models.CharField('ISO', max_length=2)
    name = models.CharField('Name', max_length=80)
    printable_name = models.CharField('Printable Name', max_length=80)
    iso3 = models.CharField('ISO3', max_length=3)
    numcode = models.SmallIntegerField('NumCode')

    class Admin:
        pass
    
    def __str__(self):
        return self.printable_name
    
admin.site.register(Country)

class State(models.Model):
    name = models.CharField('Name', max_length=40)
    abbrev = models.CharField('Abbrev', max_length=2)

    class Admin:
        pass
    
    def __str__(self):
        return self.name
    
admin.site.register(State)

class User(models.Model):
    firstname = models.CharField('First Name', max_length=30)
    lastname = models.CharField('Last Name', max_length=30)
    email_address = models.EmailField('Email Address', max_length=128, primary_key=True, unique=True)
    companyname = models.CharField('Company Name', max_length=30)
    street_address = models.CharField('Street Address', max_length=60)
    city = models.CharField('City', max_length=30)
    state = models.ForeignKey(State)
    country = models.ForeignKey(Country)
    zipcode = models.CharField('ZipCode', max_length=30)
    phone_number = PhoneNumberField()
    product = models.ForeignKey(Product)

    class Admin:
        pass
    
    def __str__(self):
        return self.email_address

admin.site.register(User)

class Activity(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return self.timestamp

admin.site.register(Activity)

class Activation(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return self.timestamp
    
admin.site.register(Activation)
