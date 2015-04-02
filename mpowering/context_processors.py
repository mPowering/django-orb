# mpowering/context_processors.py
from django.conf import settings
from mpowering.models import Category, Tag, TagOwner

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