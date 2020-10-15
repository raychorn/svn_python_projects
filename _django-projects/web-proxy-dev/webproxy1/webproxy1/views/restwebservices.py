from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from vyperlogix.classes.SmartObject import SmartObject

from django.contrib.auth import authenticate, get_user, logout

from django.contrib.auth.models import User

from django.shortcuts import render

from models import Profile

from models import VirtualMachines as VMS

import logging

import datetime
import hashlib

from utils import sendEmail

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class SubmitLoginView(View):
    def post(self, request, *args, **kwargs):
        post_args = SmartObject(args=request.POST)
        
        try:
            user = User.objects.get(email=post_args.username)
        except:
            user = None
        
        username=post_args.username
        if (user is not None):
            username = user.username
        else:
            username = None

        user = authenticate(username=username, password=post_args.password)
        if user is not None:
            request.session['is_logged_in'] = True
            request.session['auth_user'] = username
        else:
            request.session['is_logged_in'] = False
        request.session.save()
        return HttpResponseRedirect('/')
    

@method_decorator(csrf_exempt, name='dispatch')
class RestLogoutView(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if (user.is_authenticated or request.session.get('is_logged_in', False)):
            logout(request)
            request.session['is_logged_in'] = False
            request.session['auth_user'] = None
        request.session.save()

        return HttpResponseRedirect('/')
    
    
@method_decorator(csrf_exempt, name='dispatch')
class RestRegisterView(View):
    def post(self, request, *args, **kwargs):
        post_args = SmartObject(args=request.POST)

        user = User.objects.create_user(post_args.username, post_args.username, post_args.password)
        user.is_active = False
        user.save()

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = post_args.username
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        activation_key = hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile()
        profile.user = u
        profile.activation_key = activation_key
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d %H:%M:%S")
        profile.save()
        
        sendEmail(self, request.POST)

        return HttpResponseRedirect('/')

    
@csrf_exempt
def submit_login(request):
    return HttpResponse(content='Login submitted.')

@csrf_exempt
def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
        else: #Activation successful
            profile.user.is_active = True
            profile.user.save()

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    return render(request, 'siteApp/activation.html', locals())


@csrf_exempt
def drop_virtualmachine(request, id):
    # drop vm code goes here...
    try:
        vms = VMS.objects.filter(id=id)
        vm = vms[0]
        vm.delete()
    except Exception, details:
        err_msg = 'Cannot delete VMS record due to <%s>!' % (details)
        del request.session['last_error']
        logger.error(err_msg)
    return render(request, 'main.html', {'last_error': err_msg})


@csrf_exempt
def view_main(request, err_msg=None):
    if (not err_msg):
        err_msg = request.session['last_error']
        del request.session['last_error']
    return render(request, 'main.html', {'last_error': err_msg})


@csrf_exempt
def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username']=user.username
        datas['email']=user.email
        datas['email_path']="/ResendEmail.txt"
        datas['email_subject']="Nouveau lien d'activation yourdomain"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
        request.session['new_link']=True #Display: new link sent

    return redirect(home)


@method_decorator(csrf_exempt, name='dispatch')
class VirtualMachines(View):
    @staticmethod
    def get_current_vms():
        list_of_vms = []
        for vm in VMS.objects.all():
            del vm.__dict__['_state']
            list_of_vms.append( vm.__dict__)
        return list_of_vms
    
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if (user.is_authenticated or request.session.get('is_logged_in', False)):
            # get list of vms
            pass

        return render(request, 'new-vm.html', locals())
    
    def post(self, request, *args, **kwargs):
        user = get_user(request)
        if (user.is_authenticated or request.session.get('is_logged_in', False)):
            # make new vm or update an existing or remove an existing vm
            try:
                user = User.objects.filter(username=request.session.get('auth_user', None))
                vm = VMS()
                vm.name = request.POST.get('name', '')
                vm.desc = request.POST.get('desc', '')
                vm.user = user[0]
                vm.save()
            except Exception, details:
                err_msg = 'Cannot save VMS record due to <%s>!' % (details)
                request.session['last_error'] = err_msg
                logger.error(err_msg)
            
        return HttpResponseRedirect('/view_main')
    

############################################################
# Unused 
############################################################

"""
@method_decorator(csrf_exempt, name='dispatch')
class VirtualMachineContainers(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if (user.is_authenticated or request.session.get('is_logged_in', False)):
            # get list of vcs in vms
            pass

        return render(request, 'new-vm.html', locals())
    
    def post(self, request, *args, **kwargs):
        user = get_user(request)
        if (user.is_authenticated or request.session.get('is_logged_in', False)):
            # make new vm or update an existing or remove an existing vm
            try:
                user = User.objects.filter(username=request.session.get('auth_user', None))
                vc = VCS()
                vms = VMS.objects.filter(id=request.POST.get('id', ''))
                vc.vm = vms[0]
                vc.name = request.POST.get('name', '')
                vc.desc = request.POST.get('desc', '')
                vc.save()
            except Exception, details:
                err_msg = 'Cannot save VCS record due to <%s>!' % (details)
                request.session['last_error'] = err_msg
                logger.error(err_msg)
            
        return HttpResponseRedirect('/view_main')
    
"""

