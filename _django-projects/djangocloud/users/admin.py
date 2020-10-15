from django.contrib import admin

from users.registration import RegistrationProfile

class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user','activation_key','timestamp')
    search_fields = ('user','activation_key','timestamp',)
    ordering = ['user','activation_key','timestamp']

admin.site.register(RegistrationProfile, RegistrationProfileAdmin)
    

