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
def active(context, link, custom_classes=''):
    current_active = context.get('active', '')
    
    if current_active == link:
        return f' {custom_classes}' if custom_classes else ' active'
    return ''


@register.simple_tag
def render_field(field, **kwargs):
    type = kwargs.get('type', 'text')
    class_name = kwargs.get('class', '')
    id_attr = f' id="{kwargs.get("id")}"' if kwargs.get('id') else ''
    data_cy = f' data-cy="{kwargs.get("cy")}"' if kwargs.get('cy') else ''
    show_label = kwargs.get('show_label', True)

    classes = f"field field__{type} {class_name}".strip()

    # Prepare additional attributes string for the div container
    additional_attrs = ""
    # Prepare aria attributes specifically for the field
    aria_attrs = {}
    for key, value in kwargs.items():
        if key.startswith('aria_'):
            # Properly format key for HTML (replace underscores with hyphens)
            aria_key = key.replace('_', '-')
            aria_attrs[aria_key] = value
        elif key not in ['type', 'class', 'id', 'cy', 'show_label', 'aria_label', 'aria_describedby']:
            additional_attrs += f' {key}="{value}"'

    # Set ARIA attributes on the field widget
    field.field.widget.attrs.update(aria_attrs)

    label_html = field.label_tag() if show_label else ''
    
    field_html = f"""
    <div class="{classes}"{id_attr}{data_cy}{additional_attrs}>
        {label_html}
        {field}
        {field.errors}
    </div>
    """

    return mark_safe(field_html)


@register.simple_tag
def render_date(date):
    return date.strftime("%d %b %Y")


@register.simple_tag
def render_status(status):
    
    status_map = {
        "pending": "bg-yellow-100 text-yellow-800",
        "approved": "bg-green-100 text-green-800",
        "rejected": "bg-red-100 text-red-800",
        "completed": "bg-blue-100 text-blue-800",
    }

    status_class = status_map.get(status, "bg-gray-100 text-gray-800")
    html = f"<span class='inline-block py-1 px-3 mb-2 rounded-md {status_class}'>{status.capitalize()}</span>"
    return mark_safe(html)


@register.simple_tag
def render_stars(rating):
    """
    Returns the HTML for star rating using the same SVG icon, 
    filling up to the rating and leaving others empty.
    """
    icon_path = os.path.join("static/icons", "icon-star.svg")
    
    try:
        with open(icon_path) as f:
            icon_svg = f.read()  # Load the SVG content once
    except FileNotFoundError:
        return mark_safe("<!-- Icon not found -->")

    filled_star = f'<span class="flex fill-blue-800"><span class="inline-block w-4 h-4">{icon_svg}</span></span>'
    empty_star = f'<span class="flex fill-blue-200"><span class="inline-block w-4 h-4">{icon_svg}</span></span>'
    
    stars_html = filled_star * rating
    stars_html += empty_star * (5 - rating)
    html = f'<div class="flex items-center">{stars_html}</div>'

    return mark_safe(html)