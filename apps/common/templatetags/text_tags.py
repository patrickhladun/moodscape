from django import template

register = template.Library()

@register.filter('addstr')
def addstr(value, arg):
    return str(value) + str(arg)