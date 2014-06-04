from class_based_auth_views.views import LoginView
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from image.models import ImageSet_id_seq, ImageSet

import os

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
	imageset_id, created = ImageSet_id_seq.objects.get_or_create(pk=form.get_user().pk, defaults={'imageset_id_seq': '1'})
	imageset, created = ImageSet.objects.get_or_create(imageset_id=imageset_id.pk, defaults={'imageset_id': imageset_id.pk, 'owner': form.get_user()})
	
	dirpath = os.path.join(settings.MEDIA_ROOT, str(form.get_user().pk))
	if( not os.path.isdir(dirpath) ):
	    os.mkdir(dirpath)
        if created:
	    imageset_id.imageset_id_seq = imageset_id.imageset_id_seq + 1
	    imageset_id.save()
        
	    imageset.title = form.get_user().username + "'s imageset"
	    imageset.owner = form.get_user()
	    imageset.save()
	
	login(self.request, form.get_user())
	return HttpResponseRedirect(reverse('home'))
