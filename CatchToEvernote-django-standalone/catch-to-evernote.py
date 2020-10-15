#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys

import time

import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore
from evernote.edam.error.ttypes import EDAMSystemException
from evernote.edam.error.ttypes import EDAMUserException
from evernote.edam.error.ttypes import EDAMNotFoundException

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

__token__ = 'S=s1:U=74ced:E=14808fc7d40:C=140b14b5142:P=1cd:A=en-devtoken:V=2:H=0036cbc467dce3dbbbe9fd99adece476'

def remove_python_paths_matching(pattern):
    i = 0
    _i_ = -1
    for f in sys.path:
        if (f.find(pattern) > -1):
            _i_ = i
            break
        i += 1
    if (_i_ > -1):
        del sys.path[_i_]
    libs = [f for f in sys.path if (f.find(pattern) > -1)]
    print libs

#remove_python_paths_matching('Django-1.5.1')
remove_python_paths_matching('_django-projects\\')

print 'BEGIN:'
for f in sys.path:
    print f
print 'END!!!'

import django
assert(float('%s.%s'%(django.VERSION[0:3][0],''.join([str(i) for i in list(django.VERSION[0:3][1:])]))) >= 1.5)
print django.VERSION

# parse command line to get the database and wether we want to
# create the database.
from optparse import OptionParser

parser = OptionParser("usage: %prog -d DATABASE [-s]")
parser.add_option('-d', '--database', dest='database', help="DATABASE file name", metavar="DATABASE")
parser.add_option('-s', '--syncdb', dest='syncdb', action="store_true", help="should the database be created?")
parser.add_option('-r', '--repl', dest='repl', action="store_true", help="start a REPL with access to your models")
parser.add_option('--d', '--dumpdata', dest='dumpdata', action="store_true", help="django dumpdata")
parser.add_option('-i', '--inspectdb', dest='inspectdb', action="store_true", help="django inspectdb")
parser.add_option('-p', '--process', dest='process', action="store_true", help="process source table")
parser.add_option('-a', '--api', dest='api', action="store_true", help="process using api")

options, args = parser.parse_args()

if not options.database:
    parser.error("You must specify the database name")

# fetch the settings and cache them for later use
from standalone.conf import settings

from vyperlogix.django import django_utils
DOMAIN_NAME = django_utils.socket.gethostname()
print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
if (DOMAIN_NAME in ['HPDV7-6163us']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': options.database,
            'USER' : 'root',
            'PASSWORD' : 'peekab00',
            'HOST' : '192.168.1.248',
            'PORT' : '3306',
        }
    }
elif (DOMAIN_NAME in ['HORNRA3']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': options.database,
            'USER' : 'root',
            'PASSWORD' : 'peekab00',
            'HOST' : '127.0.0.1',
            'PORT' : '33307',
        }
    }
settings = settings(
    DATABASES = DATABASES
)

__template__ = '''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
            <en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
            {{ content }}
            </en-note>
'''

__date_format__ = '20130730T205204Z'

__enex1__ = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="{{ export-date }}" application="Evernote" version="Evernote Mac">
    <note>
        <title>{{ title }}</title>
        <content>
            <![CDATA[{{ content }}]>
        </content>
        <created>{{ created }}</created>
        <updated>{{ updated }}</updated>
        <tag>{{ tags }}</tag>
        <note-attributes>
            <author>Ray C Horn</author>
        </note-attributes>
    </note>
</en-export>
'''

__enex__ = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export2.dtd">
<en-export export-date="{{ export-date }}" application="Evernote/Windows" version="4.x">
<note><title>{{ title }}</title><content><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note style="background: #cccccc;font-family: 'Helvetica Neue',  Helvetica, Arial, 'Liberation Sans', FreeSans, sans-serif;color: #585957;font-size: 14px;line-height: 1.3;">
{{ content }}
</en-note>
]]>
</content>
<created>{{ created }}</created>
<updated>{{ updated }}</updated>
{{ tags }}
</note>
</en-export>
'''

# build the models we want to have in the database
from standalone import models

class Notes(models.StandaloneModel):
    note_id = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.CharField(max_length=128, blank=True)
    modified_at = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=255, blank=True)
    stream_ids = models.CharField(max_length=255, blank=True)
    stream_names = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'notes'

class Uniques(models.StandaloneModel):
    note_id = models.CharField(max_length=255, unique=True, blank=True)
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.CharField(max_length=128, blank=True)
    modified_at = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=255, blank=True)
    stream_ids = models.CharField(max_length=255, blank=True)
    stream_names = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'uniques'

def makeNote(authToken, noteStore, noteTitle, noteBody, parentNotebook=None):

    nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
    nBody += "<en-note>%s</en-note>" % ('<![CDATA[%s]]>'%(_utils.ascii_only(noteBody)))

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = _utils.ascii_only(noteTitle)
    ourNote.content = nBody

    ## parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook and hasattr(parentNotebook, 'guid'):
        ourNote.notebookGuid = parentNotebook.guid

    ## Attempt to create note in Evernote account
    try:
        note = noteStore.createNote(authToken, ourNote)
    except EDAMUserException, edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print "EDAMUserException:", edue
        return None
    except EDAMNotFoundException, ednfe:
        ## Parent Notebook GUID doesn't correspond to an actual notebook
        print "EDAMNotFoundException: Invalid parent notebook GUID"
        return None
    ## Return created note object
    return note

def export_note(__stream__,__title__,__data__):
    __fpath__ = os.path.dirname(sys.argv[0])
    fpath = os.path.abspath('%s/exported_notes/%s' % (__fpath__,__stream__))
    print 'fpath=%s' % (fpath)
    _utils._makeDirs(fpath)
    if (os.path.exists(fpath)):
        fname = '/'.join([fpath,'%s.enex'%(__title__)])
        print 'EXPORTED: %s' % (fname)
        fOut = open(fname,'w')
        print >>fOut, _utils.ascii_only(__data__)
        fOut.flush()
        fOut.close()

from django.core.management import call_command

if options.syncdb:
    # run a simple command - here syncdb - from the management suite
    call_command('syncdb')
    sys.exit(1)
elif options.repl:
    # start the shell, access to your models through import standalone.models
    call_command('shell')
    sys.exit(1)
elif options.dumpdata:
    call_command('dumpdata')
    sys.exit(1)
elif options.inspectdb:
    call_command('inspectdb')
    sys.exit(1)
elif options.process:
    Uniques.objects.all().delete()
    notes = Notes.objects.all()
    print 'There are %s notes.' % (notes.count())
    for note in notes:
        fields = [k for k in note.__dict__.keys() if (k[0] != '_')]
        uniques = Uniques.objects.filter(note_id=note.note_id)
        record = SmartObject(dict([(k,v if (v is not None) else '') for k,v in note.__dict__.iteritems() if (k[0] != '_')]))
        if (uniques.count() == 0):
            print 'UNIQUE: %s' % (record)
            aUnique = Uniques()
            aUnique.note_id = record.note_id
            aUnique.text = record.text
            aUnique.tags = record.tags
            aUnique.created_at = record.created_at
            aUnique.modified_at = record.modified_at
            aUnique.location = record.location
            aUnique.stream_ids = record.stream_ids
            aUnique.stream_names = record.stream_names
            aUnique.save()
        else:
            print 'DUPE: %s' % (record)
        pass
    uniques = Uniques.objects.all()
    print 'There are %s unique notes.' % (uniques.count())
    print 'DONE !!'
    sys.exit(1)
elif options.api:
    uniques = Uniques.objects.all()
    streams = list(set([u.stream_names for u in uniques if (len(u.stream_names.strip()) > 0)]))
    print 'There are %s unique notes.' % (uniques.count())
    print 'There are %s streams %s.' % (len(streams),streams)

    client = EvernoteClient(token=__token__)
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()
    print 'BEGIN: Notebooks'
    for n in notebooks:
        print n.name
        #noteStore.expungeNotebook(__token__,n.guid)
    print 'END!! Notebooks'
    notebooks = noteStore.listNotebooks()
    print

    for stream in streams:
        uniques = Uniques.objects.filter(stream_names=stream)
        print '%s :: %s notes.' % (stream,uniques.count())

        __streams__ = stream.split(',')
        for __stream__ in __streams__:
            __stream__ = str(__stream__).strip()
            notebook = None
            for n in notebooks:
                if (n.name == __stream__):
                    notebook = n
                    break
            if (not notebook):
                notebook = Types.Notebook()
                notebook.name = __stream__
                notebook = noteStore.createNotebook(notebook)
                notebooks = noteStore.listNotebooks()
            
            for unique in uniques:
                makeNote(__token__,noteStore,'%s #%s'%(__stream__,unique.id),'<BR/>'.join(unique.text.split('\n')),notebook)
    sys.exit(1)
else:
    uniques = Uniques.objects.all()
    streams = list(set([u.stream_names for u in uniques if (len(u.stream_names.strip()) > 0)]))
    print 'There are %s unique notes.' % (uniques.count())
    print 'There are %s streams %s.' % (len(streams),streams)

    __parse_datetime__ = lambda value:_utils.getFromDateTimeStr(value,format='%s %s %s'%(_utils.formatDate_MMDDYYYY_slashes(),_utils.formatSimpleTimeStr(),_utils.formatAMPMStr()))
    __format_datetime__ = lambda datetime:_utils.getAsDateTimeStr(datetime,fmt=_utils._formatTimeStr().replace('-','').replace(':',''))+'Z'
    __format_secs__ = lambda value:time.strftime(_utils._formatTimeStr().replace('-','').replace(':',''), time.localtime(float(value)))+'Z'

    for stream in streams:
        uniques = Uniques.objects.filter(stream_names=stream)
        print '%s :: %s notes.' % (stream,uniques.count())

        __streams__ = stream.split(',')
        __stream__ = '+'.join([str(s).strip() for s in __streams__ if (len(s) > 0)])
        for unique in uniques:
            __title__ = '%s #%s'%(__stream__,unique.id)
            __content__ = __template__.replace('{{ content }}','<BR/>'.join(unique.text.split('\n')))
            try:
                __created__ = __format_datetime__(__parse_datetime__(unique.created_at))
            except ValueError:
                __created__ = __format_secs__(unique.created_at)
            try:
                __updated__ = __format_datetime__(__parse_datetime__(unique.modified_at))
            except ValueError:
                __updated__ = __format_secs__(unique.modified_at)
            __today__ = __format_datetime__(_utils.today_localtime())
            tags = [str(t).strip() for t in unique.tags.split(',') if (len(t) > 0)]
            __tags__ = ''.join(['<tag>%s</tag>'%(t) for t in tags])
            __data__ = str(__enex__).replace('{{ title }}',__title__).replace('{{ content }}',__content__).replace('{{ created }}',__created__).replace('{{ updated }}',__updated__).replace('{{ tags }}',__tags__).replace('{{ export-date }}',__today__)
            export_note(__stream__,__title__,__data__)
    print 'DONE !!!'

