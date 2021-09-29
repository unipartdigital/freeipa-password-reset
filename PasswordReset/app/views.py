# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from django.utils.safestring import mark_safe

from .pwdmanager import *
from django.conf import settings

def index(request):
    template = loader.get_template('index.html')

    context = {
        'providers': get_providers(),
        'home': settings.HOME,
        'prefid': settings.PREFIX
    }
    return HttpResponse(template.render(context, request))

class GetToken(View):
    def post(self, request, *args, **kwargs):
        try:
            PasswdManager().first_phase(uid=request.POST['uid'], provider_id=request.POST['provider'])
        except Exception as e:
            template = loader.get_template('index.html')
            context = {
                'msg': e,
                'error': True,
                'providers': get_providers(),
            }
            return HttpResponse(template.render(context, request), status=500)
        else:
            return redirect("{0}/setpassword/?uid={1}".format(settings.PREFIX, request.POST['uid']))


class SetPassword(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('setpassword.html')
        context = {
            'uid': request.GET['uid'],
            'home': settings.HOME
        }
        return HttpResponse(template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        try:
            PasswdManager().second_phase(request.POST['uid'], request.POST['token'], request.POST['password1'])
        except Exception as e:
            template = loader.get_template('setpassword.html')
            context = {
                'msg': e,
                'error': True,
                'uid': request.POST['uid'],
                'home': settings.HOME
            }
            return HttpResponse(template.render(context, request), status=500)
        else:
            template = loader.get_template('setpassword.html')
            context = {
                'msg': mark_safe('Password successfully changed. <a href="{0}">You can login here.</a>'.format(settings.HOME)),
                'error': False,
                'uid': request.POST['uid'],
                'home': settings.HOME
            }
            return HttpResponse(template.render(context, request))
