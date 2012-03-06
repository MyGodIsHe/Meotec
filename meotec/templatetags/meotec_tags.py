from django import template

register = template.Library()


@register.filter
def class_name(Class):
    return Class.__class__.__name__