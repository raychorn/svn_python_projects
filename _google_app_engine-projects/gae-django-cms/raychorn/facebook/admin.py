from django.contrib import admin
from facebook.models import FacebookUser

class FacebookUserAdmin(admin.ModelAdmin):
    list_display = ('uid','expires','base_domain','perms','session_key','Timestamp',)
    list_filter = ('uid','expires','base_domain','perms','session_key','timestamp',)

admin.site.register(FacebookUser, FacebookUserAdmin)
