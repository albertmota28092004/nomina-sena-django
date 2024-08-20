from django import template

register = template.Library()

@register.filter
def round_number(value, decimal_places):
    try:
        return f"{value:.{decimal_places}f}"
    except (ValueError, TypeError):
        return value

@register.filter
def remove_duplicates(value_list):
    """
    Remove duplicate items from a list.

    Args:
        value_list (list): The list from which to remove duplicates.

    Returns:
        list: A new list without duplicates.
    """
    return list(dict.fromkeys(value_list))