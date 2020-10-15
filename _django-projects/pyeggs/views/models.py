from django.db import models
from django.contrib.contenttypes.models import ContentType

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
        companyname = models.CharField('Company Name', max_length=30)
    except TypeError:
        companyname = models.CharField('Company Name', maxlength=30)
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
        password = models.CharField('Password', max_length=100, editable=False, blank=True, null=True)
    except TypeError:
        password = models.CharField('Password', maxlength=100, editable=False, blank=True, null=True)
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
    try:
        phone_number = models.CharField('Phone Number', max_length=20)
    except TypeError:
        phone_number = models.CharField('Phone Number', maxlength=20)

    class Admin:
        pass
    
    def __str__(self):
        return self.email_address

import os, sys
_root_ = os.path.dirname(__file__)
_uploads_ = os.path.join(os.path.dirname(_root_),'uploads')

class UploadFile(models.Model):
    user = models.ForeignKey(User)
    filename  = models.FileField(upload_to=_uploads_)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return '%s,%s,%s' % (self.filename,self.user,self.timestamp)

class WorkQueue(models.Model):
    user = models.ForeignKey(User)
    source = models.ForeignKey(UploadFile)
    filename  = models.FileField(upload_to=_uploads_)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return '%s,%s,%s,%s' % (self.source,self.filename,self.user,self.timestamp)

class PaymentHistory(models.Model):
    user = models.ForeignKey(User)
    try:
        amount = models.DecimalField(max_digits=10, decimal_places=2)
    except AttributeError:
        amount = models.FloatField(max_digits=10, decimal_places=2)
    start_date = models.DateField(name='Start Date')
    end_date = models.DateField(name='End Date')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return '%s,%s,%s,%s,%s' % (self.user,self.amount,self.start_date,self.end_date,self.timestamp)

class UserActivity(models.Model):
    user = models.ForeignKey(User)
    try:
        action = models.CharField('Action', max_length=30)
    except TypeError:
        action = models.CharField('Action', maxlength=30)
    ip = models.IPAddressField('IP')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass
    
    def __str__(self):
        return '%s,%s,%s,%s' % (self.user,self.action,self.ip,self.timestamp)

class UserContract(models.Model):
    user = models.ForeignKey(User)
    num_days = models.PositiveIntegerField(name='Number of Days per Period Unit of Time')
    num_uploads = models.PositiveIntegerField(name='Number of Uploads')

    class Admin:
        pass
    
    def __str__(self):
        return '%s,%s per %s days' % (self.user,self.num_uploads,self.num_days)
