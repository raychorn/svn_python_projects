from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

####################################################################################
## BEGIN: User Authentication Models
####################################################################################

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    
####################################################################################
## END! User Authentication Models
####################################################################################


####################################################################################
## BEGIN: Product Models
####################################################################################

class VirtualMachines(models.Model):  # These are called Virtual Machines in the UI however these are really Containers that are turned into Real Virtual Containers that are assigned to Real Virtual Machines.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    desc = models.CharField(max_length=128, unique=False)
    expires = models.DateTimeField(null=True)
    

class RealVirtualMachines(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    desc = models.CharField(max_length=128, unique=False)
    expires = models.DateTimeField(null=True)
    

class RealVirtualContainers(models.Model):
    vm = models.ForeignKey(RealVirtualMachines, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    desc = models.CharField(max_length=128, unique=False)
    expires = models.DateTimeField(null=True)
    
####################################################################################
## END! Product Models
####################################################################################
