from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse

class SuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('users:login')
        allowed_paths = [reverse('users:login'), reverse('users:register')]
        
        if request.user.is_authenticated and request.path in allowed_paths:
            return redirect("index")
        
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect(login_url)
        
        protected_urls = ['/admin/']
        
        if request.path in protected_urls and not request.user.is_superuser:
                return HttpResponseForbidden("You do not have permission to access this page.")

        return self.get_response(request)
