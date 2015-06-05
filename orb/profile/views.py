# orb/profile/views.py
import datetime
import hashlib
import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from orb.models import UserProfile, Tag, Category
from orb.profile.forms import LoginForm, RegisterForm, ResetForm, ProfileForm
from orb.emailer import password_reset
from orb.signals import user_registered
from tastypie.models import ApiKey


def login_view(request):
    username = password = ''
    
    # if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('orb_home'))
    
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
                return HttpResponseRedirect(reverse('orb_home'))
    else:
        form = LoginForm(initial={'next':request.GET.get('next'),})
        
    return render(request, 'orb/form.html',{'username': username, 'form': form, 'title': _(u'Login')})

def register(request):
    
    if request.method == 'POST': # if form submitted...
        form = RegisterForm(request.POST)
        build_form_options(form)

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
            if form.cleaned_data.get("gender") != '0':
                user_profile.gender = form.cleaned_data.get("gender")
            if form.cleaned_data.get("age_range") != '0':
                user_profile.age_range = form.cleaned_data.get("age_range")
            if form.cleaned_data.get("role") != '0':
                role = Tag.objects.get(pk=form.cleaned_data.get("role"))
                user_profile.role = role
            user_profile.role_other = form.cleaned_data.get("role_other")
            
            if form.cleaned_data.get("organisation").strip() != '':
                category = Category.objects.get(slug='organisation')
                try:
                    organisation = Tag.objects.get(name=form.cleaned_data.get("organisation"), category=category)
                except Tag.DoesNotExist:
                    organisation = Tag()
                    organisation.name = form.cleaned_data.get("organisation")
                    organisation.category = category
                    organisation.create_user = user
                    organisation.update_user = user
                    organisation.save()
                user_profile.organisation = organisation
            
            user_profile.mailing= form.cleaned_data.get("mailing")
            
            user_profile.save()
            
            # send welcome email
            user_registered.send(sender=user, user=user,request=request)
            
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return HttpResponseRedirect('thanks/')
            return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = RegisterForm(initial={'next':request.GET.get('next'), 'mailing':True })
        build_form_options(form)

    return render(request, 'orb/form.html', {'form': form, 'title': _(u'Register')})

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

            password_reset(user,newpass)

            return HttpResponseRedirect('sent')
    else:
        form = ResetForm() # An unbound form

    return render(request, 'orb/form.html', {'form': form,'title': _(u'Reset password')})

@login_required
def edit(request):
    key = ApiKey.objects.get(user__id = request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        build_form_options(form, blank_options=False)
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
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile()
                user_profile.user = request.user
              
            if form.cleaned_data.get("organisation").strip() != '':  
                category = Category.objects.get(slug='organisation')
                try:
                    organisation = Tag.objects.get(name=form.cleaned_data.get("organisation"), category=category)
                except Tag.DoesNotExist:
                    organisation = Tag()
                    organisation.name = form.cleaned_data.get("organisation")
                    organisation.category = category
                    organisation.create_user = request.user
                    organisation.update_user = request.user
                    organisation.save()
                
                user_profile.organisation = organisation
                
            if form.cleaned_data.get("role") != '0':
                role = Tag.objects.get(pk=form.cleaned_data.get("role"))
                user_profile.role = role
            else: 
                user_profile.role = None
            user_profile.role_other = form.cleaned_data.get("role_other")
            user_profile.gender = form.cleaned_data.get("gender")
            user_profile.age_range = form.cleaned_data.get("age_range")
            user_profile.mailing = form.cleaned_data.get("mailing")
            user_profile.website = form.cleaned_data.get("website")
            user_profile.twitter = form.cleaned_data.get("twitter")
            user_profile.about = form.cleaned_data.get("about")
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
        
        if user_profile.role is not None:
            role = user_profile.role.id
        else:
            role = 0
        form = ProfileForm(initial={'username':request.user.username,
                                    'email':request.user.email,
                                    'first_name':request.user.first_name,
                                    'last_name':request.user.last_name,
                                    'api_key': key.key,
                                    'organisation': user_profile.organisation,
                                    'role': role,
                                    'role_other': user_profile.role_other,
                                    'age_range': user_profile.age_range,
                                    'gender': user_profile.gender,
                                    'mailing': user_profile.mailing,
                                    'about': user_profile.about,
                                    'website': user_profile.website,
                                    'twitter': user_profile.twitter })
        build_form_options(form, blank_options=False)
        
    return render(request, 'orb/profile/profile.html', {'form': form,})

def view_profile(request,id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404()
    
    gravatar_url = "https://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id':hashlib.md5(user.email).hexdigest(),
        'size':64
    })
    
    return render(request, 'orb/profile/view.html', {'user': user, 'gravatar_url': gravatar_url })

# Helper Methods
def build_form_options(form, blank_options=True):
    # roles
    form.fields['role'].choices = [('0','--')]    
    for t in Tag.objects.filter(category__slug='audience').order_by('order_by','name'):
        form.fields['role'].choices.append((t.id, t.name))
     
    if blank_options == True: 
        form.fields['age_range'].choices = [('0','--')]
        form.fields['gender'].choices = [('0','--')]
    else: 
        form.fields['age_range'].choices = []
        form.fields['gender'].choices = []
           
    # age range
    for x,y in UserProfile.AGE_RANGE:
        form.fields['age_range'].choices.append((x, y))

    # gender
    for x,y in UserProfile.GENDER:
        form.fields['gender'].choices.append((x, y))
    return 