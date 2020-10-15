from django.contrib import admin
from models import Tag, Entry, Language, Category, Comment, RssFeed, Setting, Installation

class TagAdmin(admin.ModelAdmin):
    list_display = ('Title',)
    list_filter = ('title',)

admin.site.register(Tag, TagAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('Title','Language','Tag','PublishOn','Views','Category',)
    list_filter = ('title','language','tag','publish_on','views','category')

admin.site.register(Entry, EntryAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('Title',)
    list_filter = ('title',)

admin.site.register(Language, LanguageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Title',)
    list_filter = ('title',)

admin.site.register(Category, CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry','user','Timestamp',)
    list_filter = ('entry','user','timestamp',)

admin.site.register(Comment, CommentAdmin)

class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('url','Timestamp',)
    list_filter = ('url','timestamp',)

admin.site.register(RssFeed, RssFeedAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ('name','value','Timestamp',)
    list_filter = ('name','value','timestamp',)

admin.site.register(Setting, SettingAdmin)

class InstallationAdmin(admin.ModelAdmin):
    list_display = ('domain','Timestamp',)
    list_filter = ('domain','timestamp',)

admin.site.register(Installation, InstallationAdmin)
