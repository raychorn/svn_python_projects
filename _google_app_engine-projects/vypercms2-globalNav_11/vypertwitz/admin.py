from django.contrib import admin
from models import RssFeed, UsedLink, Link, UsedLinkStat, Word, WordType

class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('Link', 'Timestamp')
    list_filter = ('link',)

admin.site.register(RssFeed, RssFeedAdmin)

class UsedLinkAdmin(admin.ModelAdmin):
    list_display = ('Feed', 'url', 'Timestamp')
    list_filter = ('feed',)

admin.site.register(UsedLink, UsedLinkAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('descr', 'url', 'Timestamp')

admin.site.register(Link, LinkAdmin)

class UsedLinkStatAdmin(admin.ModelAdmin):
    list_display = ('Feed', 'url', 'count', 'Timestamp')
    list_filter = ('feed', 'count')

admin.site.register(UsedLinkStat, UsedLinkStatAdmin)

class WordTypeAdmin(admin.ModelAdmin):
    list_display = ('Word_Type', 'Timestamp')

admin.site.register(WordType, WordTypeAdmin)

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'Word_Type', 'Timestamp')
    list_filter = ('word_type',)
    ordering  = ('word', 'word_type')

admin.site.register(Word, WordAdmin)
