# mpowering/context_processors.py
from django.conf import settings
from mpowering.models import Category, Tag

def get_menu(request):
    categories = Category.objects.filter(top_level=True).order_by('order_by') 
    for c in categories:
        c.tags = Tag.objects.filter(category=c).order_by('order_by') 
       
    return {'header_menu_categories': categories, }