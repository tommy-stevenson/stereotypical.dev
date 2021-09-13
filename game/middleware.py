from django.http import HttpResponseRedirect
from django.urls import reverse
from re import compile

import settings

EXEMPT_URLS = []

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class SiteLoginRequiredMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not any(m.search(path) for m in EXEMPT_URLS) and 'code' not in request.GET:
            if not request.session.get('access_token', None):
                return HttpResponseRedirect(reverse('login'))

        return self.get_response(request)
