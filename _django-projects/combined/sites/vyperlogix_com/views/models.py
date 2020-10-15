from django.db import models

class Product(models.Model):
    try:
        name = models.CharField('Product Name', max_length=30)
    except TypeError:
        name = models.CharField('Product Name', maxlength=30)
    try:
        version = models.CharField('Version', max_length=10)
    except TypeError:
        version = models.CharField('Version', maxlength=10)

    class Admin:
        pass
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    try:
        iso = models.CharField('ISO', max_length=2)
    except TypeError:
        iso = models.CharField('ISO', maxlength=2)
    try:
        name = models.CharField('Name', max_length=80)
    except TypeError:
        name = models.CharField('Name', maxlength=80)
    try:
        printable_name = models.CharField('Printable Name', max_length=80)
    except TypeError:
        printable_name = models.CharField('Printable Name', maxlength=80)
    try:
        iso3 = models.CharField('ISO3', max_length=3)
    except TypeError:
        iso3 = models.CharField('ISO3', maxlength=3)
    numcode = models.SmallIntegerField('NumCode')

    class Admin:
        pass
    
    def __str__(self):
        return self.printable_name
    
class State(models.Model):
    try:
        name = models.CharField('Name', max_length=40)
    except TypeError:
        name = models.CharField('Name', maxlength=40)
    try:
        abbrev = models.CharField('Abbrev', max_length=2)
    except TypeError:
        abbrev = models.CharField('Abbrev', maxlength=2)

    class Admin:
        pass
    
    def __str__(self):
        return self.name
    
class User(models.Model):
    try:
        firstname = models.CharField('First Name', max_length=30)
    except TypeError:
        firstname = models.CharField('First Name', maxlength=30)
    try:
        lastname = models.CharField('Last Name', max_length=30)
    except TypeError:
        lastname = models.CharField('Last Name', maxlength=30)
    try:
        email_address = models.EmailField('Email Address', max_length=128, primary_key=True, unique=True)
    except TypeError:
        email_address = models.EmailField('Email Address', maxlength=128, primary_key=True, unique=True)
    try:
        companyname = models.CharField('Company Name', max_length=30)
    except TypeError:
        companyname = models.CharField('Company Name', maxlength=30)
    try:
        street_address = models.CharField('Street Address', max_length=60)
    except TypeError:
        street_address = models.CharField('Street Address', maxlength=60)
    try:
        city = models.CharField('City', max_length=30)
    except TypeError:
        city = models.CharField('City', maxlength=30)
    state = models.ForeignKey(State)
    country = models.ForeignKey(Country)
    try:
        zipcode = models.CharField('ZipCode', max_length=30)
    except TypeError:
        zipcode = models.CharField('ZipCode', maxlength=30)
    phone_number = models.PhoneNumberField()
    product = models.ForeignKey(Product)

    class Admin:
        pass
    
    def __str__(self):
        return self.email_address

class Activity(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return self.timestamp
    
class Activation(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return self.timestamp
    
