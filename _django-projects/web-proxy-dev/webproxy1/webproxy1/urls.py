"""webproxy1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from views.restwebservices import SubmitLoginView, RestLogoutView, RestRegisterView, activation, new_activation_link, drop_virtualmachine, view_main

from views.restwebservices import VirtualMachines

class MainTemplateView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainTemplateView, self).get_context_data(**kwargs)
        context['current_vms'] = VirtualMachines.get_current_vms()
        return context
    
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainTemplateView.as_view()),
    url(r'^rest/login/$', SubmitLoginView.as_view()),
    url(r'^rest/logout/$', RestLogoutView.as_view()),
    url(r'^rest/register/$', RestRegisterView.as_view()),
    url(r'^rest/newvm/$', VirtualMachines.as_view()),
    #url(r'^rest/newcn/$', VirtualMachineContainers.as_view()),
    url(r'^rest/dropvm/(?P<id>\d+)/$', drop_virtualmachine),
    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^register/$', TemplateView.as_view(template_name="register.html")),
    url(r'^activate/(?P<key>.+)$', activation),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', new_activation_link),
    url(r'^new-virtual-machine/$', VirtualMachines.as_view()),
    url(r'^view_main/$', view_main),
]

