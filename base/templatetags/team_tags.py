from django import template

register = template.Library()

@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):
    {% for i in 3|get_range %}
        {{ i }} {% endfor %}
    """
    try:
        value = int(value)
        if value < 0:
            value = 0
        return range(value)
    except (ValueError, TypeError):
        return range(0)

@register.filter
def abs(value):
    """
    Returns the absolute value of a number
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """
    Subtracts the arg from the value
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0 