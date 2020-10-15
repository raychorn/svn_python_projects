from django.db import models

class ToDo(models.Model):
    try:
        name = models.CharField('Name', max_length=150)
    except TypeError:
        name = models.CharField('Name', maxlength=150)
    duedate = models.DateTimeField('Due Date')
    status = models.BooleanField()

    class Admin:
        pass
    
    def __str__(self):
        return self.name
    
