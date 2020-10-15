#!/usr/bin/env python

"""Please be aware this code is a stopgap measure that should go away when
more complete support for file uploading is added to newforms.

This demonstrates one way to do HTTP file upload using Django's groovy
new "newforms" approach.  There isn't a FileField-type class for newforms
yet (as of March 9th, 2007), so you must do some additional work to fetch
the uploaded content."""
import os, sys

from vyperlogix.misc import _utils
StringIO = _utils.stringIO
import zipfile

from django import http
try:
    from django import forms
    _Form = forms.Form
except AttributeError:
    from django import newforms as forms
    _Form = forms.Form
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import UploadFile, UserContract

from vyperlogix.hash import lists
from vyperlogix.classes import SmartObject

def do_upload(aUser,_fname=None,data=None):
    is_fname_valid = isinstance(_fname,str)
    anUpload = UploadFile.objects.filter(user=aUser,filename=_fname) if (is_fname_valid) else UploadFile.objects.filter(user=aUser)
    if ( (anUpload.count() == 0) and (is_fname_valid) ) or (anUpload.count() > 0):
        aContract = UserContract.objects.filter(user=aUser)
        if (aContract.count() == 1):
            allUploads = UploadFile.objects.filter(user=aUser)
            d_uploads = lists.HashedLists()
            for item in allUploads:
                d_uploads[item.timestamp.toordinal()] = item
            today = _utils.today_localtime()
            num_days = 0
            num_uploads = 0
            begin_ordinal = -1
            today_ordinal = today.toordinal()
            for k,v in d_uploads.iteritems():
                _k = int(k)
                if (begin_ordinal < 0):
                    begin_ordinal = min(_k,today_ordinal)
                    num_days += (max(_k,today_ordinal) - min(_k,today_ordinal))
                else:
                    num_days += (_k - begin_ordinal)
                num_uploads += len(v)
            normal_count = 1.0
            if (num_days == 0) and (num_uploads > 0):
                num_days = 1
            if (num_days > 0):
                normal_count = (float(num_days) / float(aContract[0].num_days)) * float(aContract[0].num_uploads)
            if (not is_fname_valid):
                return SmartObject.SmartObject({'contract_num_uploads':aContract[0].num_uploads,'contract_num_days':aContract[0].num_days,'num_uploads':num_uploads,'num_days':num_days,'normal_count':normal_count})
            if ( (num_days == 0) or (num_uploads <= normal_count) ):
                try:
                    if (data is not None):
                        _utils.writeFileFrom(_fname,data,mode='wb')
                    if (aUser is not None) and (is_fname_valid):
                        anUpload = UploadFile(user=aUser,filename=_fname)
                        anUpload.save()
                        return 'INFO: The uploaded file has been added to the work-queue and will be processed as-required by your current Service Contract, if any.  Users who have paid for a Service Contract get Priority Service ahead of all other requests in the order their requests were received.'
                    elif (is_fname_valid):
                        os.remove(_fname)
                        return 'WARNING: The uploaded file has been removed because you are not a valid user of this site.'
                    return None
                except Exception, details:
                    return 'WARNING: The uploaded file is a valid ZIP however there was another problem which was "%s".' % (details)
            else:
                return 'WARNING: You cannot upload any additional files due to the lack of a available uploads per your Usage Contract.  You are allowed %s upload(s) per %s days however you have used %s upload(s) per %s days.  Please contact our Support Department to get an initial Usage Contract or see our site to upgrade your Usage Contract.' % (aContract[0].num_uploads,aContract[0].num_days,num_uploads,num_days)
        else:
            return 'WARNING: You cannot upload any files due to the lack of a Usage Contract.  Please contact our Support Department to get an initial Usage Contract or see our site to upgrade your Usage Contract.'
    else:
        return 'WARNING: You cannot upload the same file more than once.'
    
def get_upload_stats(aUser):
    return do_upload(aUser)

class ZipUploadForm(_Form):
    """A django.newforms class that uses a FileInput widget to accept
    uploaded .ZIP files."""

    zip_file = forms.Field(widget=forms.FileInput(attrs={'size':60}),label='')

    def clean_zipfile(self):
        if 'zip_file' in self.clean_data:
            zip_file = self.clean_data['zip_file']
            if zip_file.get('content-type') != 'application/zip':
                msg = 'Only .ZIP archive files are allowed.'
                raise forms.ValidationError(msg)
            else:
                # Verify that it's a valid zipfile
                zip = zipfile.ZipFile(StringIO(zip_file['content']))
                bad_file = zip.testzip()
                zip.close()
                del zip
                if bad_file:
                    msg = '"%s" in the .ZIP archive is corrupt.' % (bad_file,)
                    raise forms.ValidationError(msg)
            return zip_file

    def save(self,request,saveTo):
        zipdata = self.clean_data['zip_file']['content']
        try:
            ioBuf = StringIO(zipdata)
            zip = zipfile.ZipFile(ioBuf)
            for filename in zip.namelist():
                # Do something here with each file in the .ZIP archive.
                #
                # For example, if you expect the archive to contain image
                # files, you could process each one with PIL, then create
                # and populate your models.Picture object and save it.
                #data = zip.read(filename)
                #pic = Picture(owner, filename, data)
                #pic.save()
                pass
            zip.close()
        except Exception, details:
            return 'WARNING: The uploaded file is not a ZIP or the file is corrupt, please upload a valid ZIP file.'
        aUser = request.session.get('user', None)
        _fname = os.path.join(os.path.join(saveTo,aUser.email_address),self.data['zip_file']['filename'])
        _utils.makeDirs(_fname)
        anUpload = UploadFile.objects.filter(user=aUser,filename=_fname)
        if (anUpload.count() == 0):
            aContract = UserContract.objects.filter(user=aUser)
            if (aContract.count() == 1):
                allUploads = UploadFile.objects.filter(user=aUser) # determine num uploads per day based on the data...
                d_uploads = lists.HashedLists()
                for item in allUploads:
                    d_uploads[item.timestamp.toordinal()] = item
                num_days = 0
                num_uploads = 0
                begin_ordinal = -1
                for k,v in d_uploads.iteritems():
                    if (begin_ordinal < 0):
                        begin_ordinal = k
                    else:
                        num_days += (k - begin_ordinal)
                    num_uploads += len(v)
                normal_count = 1.0
                if (num_days == 0) and (num_uploads > 0):
                    num_days = 1
                if (num_days > 0):
                    normal_count = (float(num_uploads) * float(aContract[0].num_days)) / float(num_days)
                if ( (num_days == 0) or (normal_count <= aContract[0].num_uploads) ):
                    try:
                        _utils.writeFileFrom(_fname,ioBuf.getvalue(),mode='wb')
                        if (aUser is not None):
                            anUpload = UploadFile(user=aUser,filename=_fname)
                            anUpload.save()
                            return 'INFO: The uploaded file has been added to the work-queue and will be processed as-required by your current Service Contract, if any.  Users who have paid for a Service Contract get Priority Service ahead of all other requests in the order their requests were received.'
                        else:
                            os.remove(_fname)
                            return 'WARNING: The uploaded file has been removed because you are not a valid user of this site.'
                        return None
                    except Exception, details:
                        return 'WARNING: The uploaded file is a valid ZIP however there was another problem which was "%s".' % (details)
                else:
                    return 'WARNING: You cannot upload any additional files due to the lack of a available uploads per your Usage Contract.  You are allowed %s upload(s) per %s days however you have used %s upload(s) per %s days.  Please contact our Support Department to get an initial Usage Contract or see our site to upgrade your Usage Contract.' % (aContract[0].num_uploads,aContract[0].num_days,num_uploads,num_days)
            else:
                return 'WARNING: You cannot upload any files due to the lack of a Usage Contract.  Please contact our Support Department to get an initial Usage Contract or see our site to upgrade your Usage Contract.'
        else:
            return 'WARNING: You cannot upload the same file more than once.'
        return 'ERROR: Cannot process you uploaded file due to some kind of system malfunction.'

# To-Do:
#
# 1). Handle the field name for the uploaded file to allow something other than "zip_file".
# 2). Handle where the file goes in terms of the user's name so we know who to notify...
# 3). Tie to a work queue to allow a background processor to do the work and notify the user...

def zip_upload(request,template='zipupload.html',onSuccess='',saveTo=''):
    from django.template import loader

    form = None

    # Typically, we'd do a permissions check here.
    #if not request.user.has_perm('pix.add_picture'):
    #    return http.HttpResponseForbidden('You cannot add pictures.')

    _error_msg = ''
    if (request.method.lower() == 'POST'.lower()):
        post_data = request.POST.copy()
        post_data.update(request.FILES)
        form = ZipUploadForm(post_data)
        if (form.is_valid()) and (os.path.exists(saveTo)):
            success = form.save(request,saveTo)
            if (success is not None) and (onSuccess not in ['',None]):
                _error_msg = success
            else:
                return http.HttpResponseRedirect(onSuccess)
        else:
            _error_msg = 'WARNING: Cannot save your uploaded file to the server due to a technical problem.  Please try back a bit later in the day.'
    else:
        form = ZipUploadForm()
    return loader.render_to_string(template, {'form':form, 'ERROR_MESSAGE':_error_msg})
