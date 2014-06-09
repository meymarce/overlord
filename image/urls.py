from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'overlord_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RandomImageSetView.as_view(), name='home'),
    url(r'^(?P<owner_id>\d+)/(?P<imageset_id>\d+)/(?P<image>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(_(?P<thumbnail>[a-f]))?/$', ImageView.as_view(), name='image'),
    url(r'^(?P<owner_id>\d+)/(?P<imageset_id>\d+)/(?P<image>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(_(?P<thumbnail>[a-f]))?/edit/$', ImageEditView.as_view(), name='image_edit'),
    url(r'^(?P<owner_id>\d+)/(?P<imageset_id>\d+)/(?P<image>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(_(?P<thumbnail>[a-f]))?/delete/$', ImageDeleteView.as_view(), name='image_delete'),
    url(r'^(?P<owner_id>\d+)/(?P<imageset_id>\d+)/(?P<image>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(_(?P<thumbnail>[a-f]))?/publish/$', ImagePublishView.as_view(), name='image_publish'),
    url(r'^upload/$', ImageUploadView.as_view(), name='upload'),
    url(r'^set/$', ImageSetsView.as_view(), {'page': 1}, name='imagesets'),
    url(r'^set/ajax/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/$', ImageSetView.as_view(), {'template_name': 'image/ajax/imageSet.html'}),
    url(r'^set/public/$', ImagePublicSetsView.as_view(), {'page': 1}, name='imagesets_public'),
    url(r'^set/(?P<page>\d+)/$', ImageSetsView.as_view(), name='imagesets_paged'),
    url(r'^set/add/$', ImageSetAddView.as_view(), name='imageset_add'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/$', ImageSetView.as_view(), name='imageset'),
    url(r'^set/embed/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/$', ImageSetEmbeddedView.as_view(), name='imageset_embed'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/list/$', ImageSetListView.as_view(), {'page': 1}, name='imageset_list'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/list/(?P<page>\d+)/$', ImageSetListView.as_view(), name='imageset_list_paged'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/edit/$', ImageSetEditView.as_view(), name='imageset_edit'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/delete/$', ImageSetDeleteView.as_view(), name='imageset_delete'),
    url(r'^set/(?P<owner_id>\d+)/(?P<imageset_id>\d+)/publish/$', ImageSetPublishView.as_view(), name='imageset_publish'),
)
