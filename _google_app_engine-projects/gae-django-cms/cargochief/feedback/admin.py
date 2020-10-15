from django.contrib import admin
from feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'Timestamp')
    list_filter = ('subject', 'message', 'timestamp')

admin.site.register(Feedback, FeedbackAdmin)
