from django.contrib import admin
from models import State

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'fieldName', 'fieldLen', 'abbrev' )

admin.site.register(State, StateAdmin)
