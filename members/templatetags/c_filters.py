from django.template.defaulttags import register
from django import template

register = template.Library()


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)
