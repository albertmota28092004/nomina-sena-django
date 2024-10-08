from django.utils.deprecation import MiddlewareMixin


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/recibo/') or request.path.startswith('/liquidacion/'):
            response['Content-Security-Policy'] = "frame-ancestors 'self' http://127.0.0.1:8000"
        return response


class DebugHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(response.headers)
        return response


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if 'X-Frame-Options' in response:
            del response['X-Frame-Options']
        return response
