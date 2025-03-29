from django import template

register = template.Library()

@register.filter
def clean_text(value):
    """Replaces underscores with spaces and capitalizes each word."""
    return value.replace("_", " ").title()
