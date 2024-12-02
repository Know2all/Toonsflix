from django.shortcuts import redirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

class Auth:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            login_url = reverse('login')
        except NoReverseMatch:
            login_url = '/login'  # Fallback if reverse fails

        # List of named URL patterns to exclude from authentication check
        exclude_paths = [
            'categorys',
            'cartoons',
            'getlatestvideos',
            'help',
            'image_extract',
            'video_extract',
            'filter_by_category',
            'filter_by_cartoon',
            'search'
        ]

        print(request.path)
        
        # Retrieve the current URL name
        current_url_name = request.path.split("/")[1]

        if not request.user.is_authenticated and request.path != login_url:
            if current_url_name not in exclude_paths:
                return redirect(login_url)

        response = self.get_response(request)
        return response
