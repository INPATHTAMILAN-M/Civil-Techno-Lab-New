# yourapp/middleware/store_ip.py

import threading
_thread_locals = threading.local()

def get_current_ip():
    return getattr(_thread_locals, 'ip_address', None)

class StoreIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.headers.get("X-Forwarded-For") or request.META.get("REMOTE_ADDR")
        _thread_locals.ip_address = ip
        return self.get_response(request)
