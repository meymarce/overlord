from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.views.generic.base import RedirectView

from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'overlord_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r'^image/', include('image.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
