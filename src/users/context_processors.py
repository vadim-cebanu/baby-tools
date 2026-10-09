from django.conf import settings


def author_processor(request):
    """Expose ``settings.AUTHOR`` to all templates as ``author``.

    Args:
        request: The current HTTP request.

    Returns:
        dict: Template context containing the author.
    """
    return {"author": settings.AUTHOR}
