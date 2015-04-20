# orb/emailer.py
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

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