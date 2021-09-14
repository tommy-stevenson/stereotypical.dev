import json

from django.conf import settings
from django.views.generic import TemplateView

import requests

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URL = settings.REDIRECT_URL


class FacesHomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['redirect_url'] = REDIRECT_URL
        context['client_id'] = CLIENT_ID

        access_token = self.request.session.get('access_token', '')
        context['access_token'] = access_token

        code = self.request.GET.get('code')

        if code:

            r = requests.post('https://github.com/login/oauth/access_token',
                              data={
                                  'client_id': CLIENT_ID,
                                  'client_secret': CLIENT_SECRET,
                                  'redirect_url': REDIRECT_URL,
                                  'code': code
                              })

            if r.status_code == 200:

                for i in r.content.decode('ascii').split('&'):

                    k, v = i.split('=')

                    if k == 'access_token':
                        self.request.session[k] = v

                    context[k] = v

        return context


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['redirect_url'] = REDIRECT_URL
        context['client_id'] = CLIENT_ID

        return context
