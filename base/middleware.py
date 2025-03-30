class CurrentLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the currentLang cookie value
        request.current_lang = request.COOKIES.get(
            "currentLang", "en"
        )  # Default to 'en'

        response = self.get_response(request)
        return response
