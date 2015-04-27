# orb/emailer.py
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from orb.models import ResourceCriteria

def user_welcome(to_user):
    template_html = 'orb/email/welcome.html'
    template_text = 'orb/email/welcome.txt'
    
    from_email = settings.SERVER_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + _(u"Welcome to ORB")
    
    data = {"firstname": to_user.first_name,
            "lastname": to_user.last_name,
            "info_email": settings.ORB_INFO_EMAIL }
    
    text_content = render_to_string(template_text, data)
    html_content = render_to_string(template_html, data)

    send_mail(subject, 
              text_content, 
              from_email,
              [to_user.email], 
              fail_silently=False, 
              html_message=html_content)
            
    return 

def password_reset(to_user, new_password):
    template_html = 'orb/email/password_reset.html'
    template_text = 'orb/email/password_reset.txt'
    
    from_email = settings.SERVER_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + _(u"Password reset")
    
    text_content = render_to_string(template_text, {"new_password": new_password})
    html_content = render_to_string(template_html, {"new_password": new_password})

    send_mail(subject, 
              text_content, 
              from_email,
              [to_user.email], 
              fail_silently=False, 
              html_message=html_content)
            
    return

def first_resource(to_user, resource):
    template_html = 'orb/email/first_resource.html'
    template_text = 'orb/email/first_resource.txt'
    
    from_email = settings.SERVER_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + _(u"Resource Submitted") + ": " + resource.title
    
    data = {"title": resource.title,
            "firstname": to_user.first_name,
            "lastname": to_user.last_name,
            "info_email": settings.ORB_INFO_EMAIL }
    
    text_content = render_to_string(template_text, data)
    html_content = render_to_string(template_html, data)

    send_mail(subject, 
              text_content, 
              from_email,
              [to_user.email], 
              fail_silently=False, 
              html_message=html_content)
            
    return

def resource_approved(request, to_user, resource):
    template_html = 'orb/email/resource_approved.html'
    template_text = 'orb/email/resource_approved.txt'
    
    from_email = settings.SERVER_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + _(u"Resource Submission") + ": " + resource.title
    
    data = {"title": resource.title,
            "firstname": to_user.first_name,
            "lastname": to_user.last_name,
            "info_email": settings.ORB_INFO_EMAIL,
            "resource_link":  request.build_absolute_uri(reverse('orb_resource', args=[resource.slug]))}
    
    text_content = render_to_string(template_text, data)
    html_content = render_to_string(template_html, data)

    send_mail(subject, 
              text_content, 
              from_email,
              [to_user.email], 
              fail_silently=False, 
              html_message=html_content)
            
    return

def resource_rejected(to_user, resource, criteria, notes):
    template_html = 'orb/email/resource_rejected.html'
    template_text = 'orb/email/resource_rejected.txt'
    
    from_email = settings.SERVER_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + _(u"Resource Submission") + ": " + resource.title
    
    rejection_criteria = ResourceCriteria.objects.filter(id__in=criteria)
    data = {"title": resource.title,
            "firstname": to_user.first_name,
            "lastname": to_user.last_name,
            "info_email": settings.ORB_INFO_EMAIL,
            "criteria": rejection_criteria,
            "notes": notes }
    
    text_content = render_to_string(template_text, data)
    html_content = render_to_string(template_html, data)

    send_mail(subject, 
              text_content, 
              from_email,
              [to_user.email], 
              fail_silently=False, 
              html_message=html_content)
            
    return