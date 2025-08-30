"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

import rollbar
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

application = get_wsgi_application()

# Rollbar initialization
try:
    if hasattr(settings, 'ROLLBAR') and settings.ROLLBAR.get('access_token'):
        rollbar.init(
            settings.ROLLBAR['access_token'],
            settings.ROLLBAR['environment'],
            root=settings.BASE_DIR,
            allow_logging_basic_config=False
        )
        
        # middleware
        class RollbarNotifierMiddleware:
            def __init__(self, get_response):
                self.get_response = get_response
                
            def __call__(self, request):
                return self.get_response(request)
                
            def process_exception(self, request, _exception):
                user_id = (
                    request.user.id 
                    if request.user.is_authenticated 
                    else None
                )
                
                rollbar.report_exc_info(
                    request=request,
                    extra_data={'user_id': user_id}
                )
                return None
        
        application = RollbarNotifierMiddleware(application)
except Exception as e:
    print(f"Error initializing Rollbar: {e}")