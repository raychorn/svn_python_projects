from django.contrib import admin

from models import Geolocation

class GeolocationAdmin(admin.ModelAdmin):
    list_display = ('gps',)
    search_fields = ('gps',)
    ordering = ['gps']

admin.site.register(Geolocation, GeolocationAdmin)
    

