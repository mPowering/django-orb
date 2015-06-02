# orb/context_processors.py
from django.conf import settings
import orb
from orb.models import Category, Tag, TagOwner

def get_menu(request):
    categories = Category.objects.filter(top_level=True).order_by('order_by') 
    for c in categories:
        c.tags = Tag.objects.filter(category=c,parent_tag=None).order_by('order_by') 
    
    if request.user.is_authenticated():
        tags = TagOwner.objects.filter(user=request.user)
    else:
        tags = None   
        
    return {'header_menu_categories': categories, 
            'header_owns_tags': tags,
            'settings': settings,}
    
def get_version(request):
    version = "v" + str(orb.VERSION[0]) + "." + str(orb.VERSION[1]) + "." + str(orb.VERSION[2])
    return {'version': version,
            'ORB_GOOGLE_ANALYTICS_CODE': settings.ORB_GOOGLE_ANALYTICS_CODE }

def base_context_processor(request):
    return {
         'BASE_URL': request.build_absolute_uri("/").rstrip("/")
     }