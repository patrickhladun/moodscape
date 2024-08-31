import os

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def icon(name, size="md", class_name=""):
    """
    Generates an HTML span element containing an SVG icon.

    This function reads an SVG file from the static assets/icons directory and
    embeds it within a span element. If the specified SVG file is not found,
    it returns an HTML comment indicating that the icon was not found.

    Args:
        name (str): The name of the icon file (without .svg extension).
        size (str, optional): The size of the icon ('sm', 'md', or 'lg').
        Defaults to 'md'.

    Returns:
        str: The HTML string for the icon or a comment if the icon is not
        found.
    """

    sizes = {
        "sm": "w-4 h-4",
        "md": "w-6 h-6",
        "lg": "w-9 h-9",
    }

    size = sizes.get(size, "w-8 h-8")

    try:
        with open(os.path.join("static/icons", f"{name}.svg")) as f:
            icon = f.read()
            return mark_safe(
                f'<span class="flex transition-all{ ' ' + class_name if class_name else '' }"><span class="inline-block {size}">{icon}</span></span>'
            )
    except FileNotFoundError:
        return mark_safe("<!-- Icon not found -->")



@register.simple_tag(takes_context=True)
def active(context, link):
    active = context.get('active')
    return ' active' if active == link else ''

@register.simple_tag
def render_field(field, type="text", class_name=""):   
    classes = f" {class_name}" if class_name else "" 
    field_html = f"""
    <div class="field field__{type}{classes}">
        {field.label_tag()}
        {field}
        {field.errors}
    </div>
    """
    
    return mark_safe(field_html)