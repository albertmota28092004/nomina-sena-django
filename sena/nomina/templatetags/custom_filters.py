from django import template

register = template.Library()

@register.filter
def round_number(value, decimal_places):
    try:
        return f"{value:.{decimal_places}f}"
    except (ValueError, TypeError):
        return value
