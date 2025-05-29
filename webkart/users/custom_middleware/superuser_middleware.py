from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse

class SuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('users:login')
        
        if request.path == login_url:
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return redirect(login_url)
        
        protected_urls = ['/admin/']
        
        if request.path in protected_urls and not request.user.is_superuser:
                return HttpResponseForbidden("You do not have permission to access this page.")

        return self.get_response(request)
