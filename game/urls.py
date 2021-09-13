from django.contrib import admin
from django.urls import path, re_path

from game.views import FacesHomepageView, LoginView

urlpatterns = [
    path('', FacesHomepageView.as_view(), name='homepage'),
    re_path(r'^\\?code=\\(?P<code>\w+)/$', FacesHomepageView.as_view(), name='homepage'),
    path('login', LoginView.as_view(), name='login'),
]
