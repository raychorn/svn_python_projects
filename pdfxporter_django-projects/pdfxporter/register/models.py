from django.db import models

class Registration(models.Model):
    order_id = models.CharField(maxlength=128,primary_key=True)
    order_date = models.DateTimeField('date ordered',null=False)
    activity_date = models.DateTimeField('date accessed',null=False)
    product_id = models.CharField(maxlength=299,null=False,unique=True)
    valid_until = models.DateTimeField('date limit',null=False)
    cname = models.CharField(maxlength=32,null=False)
    name = models.CharField(maxlength=100,null=False)
    pname = models.CharField(maxlength=32,null=False)
    email = models.EmailField(null=False)
    is_revoked = models.BooleanField(null=False)
    is_active = models.BooleanField(null=False)
    reason_revoked = models.CharField(maxlength=399,null=True)
    unique_together = ("order_id", "product_id")
    last_activity = models.DateTimeField('last activity',null=True)

