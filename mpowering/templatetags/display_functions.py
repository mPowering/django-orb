from django import template

register = template.Library()

@register.filter(name='cloud_text_size')
def cloud_text_size(count, diff):
    return 10 + ((40/(diff))*count)