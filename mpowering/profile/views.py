# mpowering/profile/views.py
import datetime
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login, views)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from mpowering.models import UserProfile, Organisation
from mpowering.profile.forms import LoginForm, RegisterForm, ResetForm, ProfileForm
from tastypie.models import ApiKey


def login_view(request):
    username = password = ''
    
    # if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('mpowering_home'))
    
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request,user)
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('mpowering_home'))
    else:
        form = LoginForm(initial={'next':request.GET.get('next'),})
        
    return render(request, 'mpowering/form.html',{'username': username, 'form': form, 'title': _(u'Login')})

def register(request):
    
    if request.method == 'POST': # if form submitted...
        form = RegisterForm(request.POST)
        if form.is_valid(): # All validation rules pass
            # Create new user
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.job_title = form.cleaned_data.get("job_title")
            try:
                organisation = Organisation.objects.get(name=form.cleaned_data.get("organisation"))
            except Organisation.DoesNotExist:
                organisation = Organisation()
                organisation.name = form.cleaned_data.get("organisation")
                organisation.create_user = user
                organisation.update_user = user
                organisation.save()
            user_profile.organisation = organisation
            user_profile.save()
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return HttpResponseRedirect('thanks/')
            return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = RegisterForm(initial={'next':request.GET.get('next'),})

    return render(request, 'mpowering/form.html', {'form': form, 'title': _(u'Register')})

def reset(request):
    if request.method == 'POST': # if form submitted...
        form = ResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                user = User.objects.get(email__exact=username)
            newpass = User.objects.make_random_password(length=8)
            user.set_password(newpass)
            user.save()
            if request.is_secure():
                prefix = 'https://'
            else:
                prefix = 'http://'
            # TODO - better way to manage email message content
            send_mail('mPowering: Password reset', 'Here is your new password for mPowering: '+newpass 
                      + '\n\nWhen you next log in you can update your password to something more memorable.' 
                      + '\n\n' + prefix + request.META['SERVER_NAME'] , 
                      settings.SERVER_EMAIL, [user.email], fail_silently=False)
            return HttpResponseRedirect('sent')
    else:
        form = ResetForm() # An unbound form

    return render(request, 'mpowering/form.html', {'form': form,'title': _(u'Reset password')})

def edit(request):
    key = ApiKey.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # update basic data
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            
            try:
                organisation = Organisation.objects.get(name=form.cleaned_data.get("organisation"))
            except Organisation.DoesNotExist:
                organisation = Organisation()
                organisation.name = form.cleaned_data.get("organisation")
                organisation.create_user = request.user
                organisation.update_user = request.user
                organisation.save()
                
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.job_title = form.cleaned_data.get("job_title")
                user_profile.organisation = organisation
                user_profile.save()
            except UserProfile.DoesNotExist:
                user_profile = UserProfile()
                user_profile.user = request.user
                user_profile.job_title = form.cleaned_data.get("job_title")
                user_profile.organisation = organisation
                user_profile.save()
            messages.success(request, _(u"Profile updated"))
            
            # if password should be changed
            password = form.cleaned_data.get("password")
            if password:
                request.user.set_password(password)
                request.user.save()
                messages.success(request, _(u"Password updated"))
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile()
        form = ProfileForm(initial={'username':request.user.username,
                                    'email':request.user.email,
                                    'first_name':request.user.first_name,
                                    'last_name':request.user.last_name,
                                    'api_key': key.key,
                                    'job_title': user_profile.job_title,
                                    'organisation': user_profile.organisation,})
        
    return render(request, 'mpowering/profile/profile.html', {'form': form,})
