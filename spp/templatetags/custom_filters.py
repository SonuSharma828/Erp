from django import template

register = template.Library()

@register.filter
def strip_lower(value):
    if isinstance(value, str):
        return value.strip().lower()
    return value

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

