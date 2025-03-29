# app/middleware.py
class DisableAdminLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we're in the admin site
        if request.path.startswith('/admin/'):
            # Disable admin logging for this request
            from django.contrib.admin.models import LogEntry
            original_save = LogEntry.save
            
            def dummy_save(instance, *args, **kwargs):
                # Do nothing - effectively disabling admin logging
                return None
                
            LogEntry.save = dummy_save
            response = self.get_response(request)
            LogEntry.save = original_save
            return response
        return self.get_response(request)