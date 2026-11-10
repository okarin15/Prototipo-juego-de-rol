class HardeningSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # 1. Cabecera Content Security Policy (CSP) estricta
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:"
        
        # 2. Protección contra MIME-Sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # 3. Protección contra Clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # 4. Ocultar la versión del servidor de desarrollo
        if 'Server' in response:
            del response['Server']
            
        return response
