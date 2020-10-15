from django.contrib import admin

from users.registration import RegistrationProfile
from users.models import GoogleAuthenticator

class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user','activation_key','timestamp')
    search_fields = ('user','activation_key','timestamp',)
    ordering = ['user','activation_key','timestamp']

admin.site.register(RegistrationProfile, RegistrationProfileAdmin)
    

class GoogleAuthenticatorAdmin(admin.ModelAdmin):
    list_display = ('otpseed','sitename','href')
    search_fields = ('sitename','otpseed',)
    ordering = ['sitename','otpseed','href']

admin.site.register(GoogleAuthenticator, GoogleAuthenticatorAdmin)
