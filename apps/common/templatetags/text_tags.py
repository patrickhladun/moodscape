from django import template

register = template.Library()


@register.filter("addstr")
def addstr(value, arg):
    return str(value) + str(arg)


@register.filter(name="break_after_commas")
def break_after_commas(value):
    return value.replace(",", ",<br>")
