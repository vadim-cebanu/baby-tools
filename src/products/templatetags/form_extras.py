from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    """Append a CSS class to a form field's widget.

    Usage: ``{{ field|add_class:"form-control" }}``

    Args:
        field: The bound form field.
        css: The CSS class(es) to add.

    Returns:
        The same field, so filters can be chained.
    """
    existing = field.field.widget.attrs.get("class", "")
    field.field.widget.attrs["class"] = (existing + " " + css).strip()
    return field


@register.filter
def attr(field, arg):
    """Set an HTML attribute on a form field's widget.

    Usage: ``{{ field|attr:"placeholder=Write here" }}``

    Args:
        field: The bound form field.
        arg: The attribute as a ``key=value`` string.

    Returns:
        The same field, so filters can be chained.
    """
    key, _, val = arg.partition("=")
    if key:
        field.field.widget.attrs[key] = val
    return field
