from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = patterns(
    '',
    url(r'^profile/$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r'^login/$', MyLoginView.as_view(),  {'template_name': 'accounts/login.html'}, name='accounts_login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='accounts_logout'),
)

