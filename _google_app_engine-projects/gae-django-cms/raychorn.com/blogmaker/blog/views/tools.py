''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import calendar, datetime, time, StringIO
from time import strftime

from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django import newforms as forms
from django.newforms import widgets, form_for_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils.translation import gettext
from PIL import Image

from blogmaker.util import formatChanges

from blogmaker.blog.models import Tag, Entry

@user_passes_test(lambda u: u.has_perm('blogmaker.entry'))
def existing_entries(request):
    ''' View tools index'''
    
    sort = request.GET.get('sort', '-pub_date')
    entries = Entry.objects.all().order_by(sort)
    
    return render_to_response('blog/tools/entry_list.html', {'entries': entries, 'sort': sort})
    
    
class EntryForm(forms.Form):
    headline = forms.CharField(max_length=255, required=True, label=gettext('Title'), widget=widgets.TextInput(attrs={"size": 75}))
    slug = forms.CharField(max_length=120, required=True, widget=widgets.TextInput(attrs={"size": 75}))
    pub_date = forms.DateTimeField(required=True, label=gettext('Date and Time'),
                help_text=gettext("Format: 'YYYY-MM-DD HH:MM:SS'"))
    #summary = forms.CharField(maxlength=255, null=True, blank=True, help_text="Leave this field blank")
    image = forms.Field(widget=widgets.FileInput, required=False, label=gettext('Image'), 
            help_text=gettext('Width should be less than 468px'))
    copyright = forms.CharField(max_length=255, required=False, help_text="Attribution info", widget=widgets.TextInput(attrs={"size": 75}))
    body = forms.Field(widget=widgets.Textarea(attrs={"rows": 25, "cols": 73}))
    active = forms.BooleanField(help_text="Is post viewable on site?")
    
    _userChoices = [ (user.id, user.username) for user in User.objects.all() ]
    _tagChoices = [ (tag.id, tag.tag) for tag in Tag.objects.all() ]
    _entryChoices = [ (entry.id, entry.headline[:95]) for entry in Entry.objects.all() ]
    
    user = forms.ChoiceField(choices=_userChoices, required=True)
    tags = forms.MultipleChoiceField(choices=_tagChoices, required=False)
    related_entries = forms.MultipleChoiceField(choices=_entryChoices, required=False)
    externalId = forms.IntegerField(required=False)
    
    def clean_image(self):
        if self.clean_data.get('image'):
            image_data = self.clean_data['image']
            if 'error' in image_data:
                raise forms.ValidationError(gettext('Upload a valid image. The file you uploaded was either not an image or was a corrupted image.'))
                
            content_type = image_data.get('content_type')
            if content_type:
                main, sub = content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'gif', 'png', 'jpg', 'x-png', 'pjpeg']):
                    raise forms.ValidationError(gettext('JPG, PNG, GIF only.'))
                    
            size = len(image_data['content'])
            if size > 1000000:
                raise forms.ValidationError(gettext('Image is too big!'))
                
            width, height = image_data['dimensions']
            if width > 468:
                raise forms.ValidationError(gettext('Max width is 468px'))
        return self.clean_data['image']

    
@user_passes_test(lambda u: u.has_perm('blogmaker.entry'))
def edit_entry(request, id=None):
    ''' Edit and preview an existing entry'''
      
    # if editing existing entry  
    if id:
        entry = get_object_or_404(Entry, id=id)
        current_image = entry.image
        preview = True
        initial = dict(pub_date=entry.pub_date, headline=entry.headline, slug=entry.slug, copyright=entry.copyright,
                       body=entry.body, active=entry.active, user=entry.user_id, image=entry.image,
                       tags=[ t.id for t in entry.tags.all() ], 
                       related_entries=[ e.id for e in entry.related_entries.all() ])
    
    # if adding new entry
    else:
        entry = None
        current_image = None
        preview = False
        now = datetime.datetime.now()
        delay = datetime.timedelta(minutes=30)
        pub_date = now+delay
        initial = {'pub_date': pub_date.strftime("%Y-%m-%d %H:%M:%S"), 'active': True, 'user': settings.DEFAULT_BLOG_USER}
        
    if request.method == 'POST':
        if not entry:
            entry = Entry()
            new_entry = True
        else:
            new_entry = False
            
        # validate the form, save the object, and redirect results
        if 'image' in request.FILES:
            img = Image.open(StringIO.StringIO(request.FILES['image']['content']))
            request.FILES['image']['dimensions'] = img.size
            
        new_data = request.POST.copy()
        if 'active' in new_data:
            new_data['active'] = True
        else:
            new_data['active'] = False
        new_data.update(request.FILES)
        form = EntryForm(new_data)
        
        if form.is_valid():
            clean_data = form.clean_data
            
            # log changes if existing entry prior to changing and saving new fields
            if not new_entry:
                changes = []
                for field in clean_data:
                    if field != 'related_entries' and field != 'tags' and field != 'user':
                        old_value = getattr(entry, field)
                        new_value = clean_data[field]
                        if field == 'body' or field == 'headline':
                            new_value = new_value.decode('utf-8')
                            old_value = old_value.decode('utf-8')
                    elif field == 'related_entries':
                        old_value = [ e.headline for e in entry.related_entries.all() ]
                        new_value = [ Entry.objects.get(id=id).headline for id in clean_data['related_entries'] ]
                    elif field == 'tags':
                        old_value = [ t.tag for t in entry.tags.all() ]
                        old_value = sorted(old_value)
                        new_value = [ Tag.objects.get(id=id).tag for id in clean_data['tags'] ]
                        new_value = sorted(new_value)
                    elif field == 'user':
                        old_value = getattr(entry, field)
                        new_value = User.objects.get(id=clean_data['user'])
                    if new_value != old_value:
                        changes.append( (entry.id, field, old_value, new_value) )
                log_changes = formatChanges('Blogmaker tools', changes)
                if changes:
                    LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Entry).id,
                                                entry.id, entry.headline, CHANGE, log_changes)
            
            entry.headline = clean_data['headline'].decode('utf-8')
            entry.slug = clean_data['slug']
            entry.pub_date = clean_data['pub_date']
            entry.copyright = clean_data['copyright']
            entry.body = clean_data['body'].decode('utf-8')
            entry.active = clean_data['active']
            entry.user_id = clean_data['user']
            entry.save()  # save prior to adding M2M fields which require a pk
            entry.tags = clean_data['tags']
            entry.related_entries = clean_data['related_entries']
            entry.externalId = clean_data['externalId']
            
            if clean_data['image']:
                image = clean_data['image']
                entry.save_image_file(image['filename'], image['content'])
            
            entry.save()
            
            # log if new entry after saving the entry and filling all fields
            if new_entry:
                changes = []
                for field in clean_data:
                    if field != 'related_entries' and field != 'tags' and field != 'user':
                        new_value = clean_data[field]
                        if field == 'body' or field == 'headline':
                            new_value = new_value.decode('utf-8')
                    elif field == 'related_entries':
                        new_value = [ Entry.objects.get(id=id).headline for id in clean_data['related_entries'] ]
                    elif field == 'tags':
                        new_value = [ Tag.objects.get(id=id).tag for id in clean_data['tags'] ]
                    elif field == 'user':
                        new_value = User.objects.get(id=clean_data['user'])
                    changes.append( (entry.id, field, 'NEW ENTRY', new_value) )
                log_changes = formatChanges('Blogmaker tools', changes)
                LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Entry).id,
                                            entry.id, entry.headline, ADDITION, log_changes)
            
            # redirect to the same page with preview or to the entries list
            if request.POST.has_key('preview'):
                this_entry = '%stools/entry/%s/' % (settings.BLOG_ROOT, entry.id)
                return HttpResponseRedirect(this_entry)
            if request.POST.has_key('close'):
                all_entries = '%stools/entry/' % settings.BLOG_ROOT
                return HttpResponseRedirect(all_entries)
        else:
            return render_to_response('blog/tools/edit_entry.html', {'form': form, 'object': entry, 'preview': False}) 
    	
    else:
        form = EntryForm(initial=initial)
        return render_to_response('blog/tools/edit_entry.html', {'form': form, 'object': entry, 'preview': preview, 'current_image': current_image})