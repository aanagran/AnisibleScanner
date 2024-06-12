import secure
from django.conf import settings

"""
== Option Can we passed to Enable Headers in Response:
server      - set the Server header, secure.Secure(server=secure.Server()) (default=False)
hsts        - set the Strict-Transport-Security header secure.Secure(hsts=secure.StrictTransportSecurity()) (default=True)
xfo         - set the X-Frame-Options header secure.Secure(xfo=secure.XFrameOptions()) (default=True)
xxp         - set the X-XSS-Protection header secure.Secure(xxp=secure.XXSSProtection()) (default=True)
content     - set the X-Content-Type-Options header secure.Secure(content=secure.XContentTypeOptions()) (default=True)
csp         - set the Content-Security-Policy secure.Secure(csp=secure.ContentSecurityPolicy()) (default=False) *
referrer    - set the Referrer-Policy header secure.Secure(referrer=secure.ReferrerPolicy()) (default=True)
cache       - set the Cache-control header secure.Secure(cache=secure.CacheControl()) (default=True)
permissions - set the Permissions-Policy header secure.Secure(permissions=secure.PermissionsPolicy()) (default=False)
"""

def set_secure_headers(get_response):
    def middleware(request):
        response = get_response(request)
        return response
    return middleware