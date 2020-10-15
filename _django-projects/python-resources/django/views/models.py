from django.db import models

class Library(models.Model):
    folder = models.CharField(maxlength=128,primary_key=True)
    url1 = models.CharField(maxlength=256,null=True)
    url2 = models.CharField(maxlength=256,null=True)
    creation_date = models.DateTimeField('date created',null=False)
    modification_date = models.DateTimeField('date modified',null=False)
    is_active = models.BooleanField(null=False)

class Node(models.Model):
    id = models.IntegerField(null=False,primary_key=True)
    name = models.CharField(maxlength=128,null=False)
    parent = models.IntegerField(null=True)
    creation_date = models.DateTimeField('date created',null=False)
    modification_date = models.DateTimeField('date modified',null=False)
    is_active = models.BooleanField(null=False)
    is_file = models.BooleanField(null=False)
    is_url = models.BooleanField(null=False)

class Country(models.Model):
    id = models.IntegerField(null=False,primary_key=True)
    iso = models.CharField(maxlength=80,null=False)
    name = models.CharField(maxlength=80,null=False)
    printable_name = models.CharField(maxlength=80,null=False)
    iso3 = models.CharField(maxlength=3,null=False)
    numcode = models.SmallIntegerField(null=False)
