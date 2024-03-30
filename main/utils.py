def get_template_path(request, base_path):
    """
    Utility function to get the template path based on the language stored in cookies.
    
    Args:
        request: Django HTTP request object.
        base_path: Base path of the template without language prefix.

    Returns:
        Tuple containing the modified template path.
    """
    # Get the language from cookies, defaulting to 'en' if not found
    language = request.COOKIES.get('language', 'ar').split('-')[0]

    template_path = f'{language}/{base_path}'


    return template_path