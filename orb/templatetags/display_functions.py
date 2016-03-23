from django import template

register = template.Library()


@register.filter(name='cloud_text_size')
def cloud_text_size(count, diff):
    return int(14.0 + ((28.0 / diff) * count))
