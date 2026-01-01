from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip maintenance for admin and yourself if needed
        if request.path.startswith('/admin/') or request.path.startswith('/maintenance-off/'):
            return self.get_response(request)
        
        # Check if maintenance mode is ON
        if getattr(settings, 'MAINTENANCE_MODE', False):
            html = render_to_string('maintenance.html')
            return HttpResponse(html, status=503)
        
        return self.get_response(request)