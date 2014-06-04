from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from django.conf import settings
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image as PILImage

from .models import *
from .forms import *

import hashlib
import uuid
import datetime
import os

# Create your views here.

class ImageEditView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageEditForm
    template_name = 'image/imageEdit.html'

    def get_form_kwargs(self):
	kwargs = super(ImageEditView, self).get_form_kwargs()
	kwargs['request'] = self.request
	return kwargs

    def get_object(self, queryset=None):
	return get_object_or_404(Image, pk=self.kwargs.get('image'), owner=self.request.user, imageset=str(self.request.user.pk) + '.' + str(self.kwargs.get('imageset_id')) )

    def form_valid(self, form):
	if(self.request.user.pk != int(self.kwargs.get('owner_id'))):
	    raise Http404

	image = form.save()
	return HttpResponseRedirect(image.get_success_url())

class ImagePublishView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
	if(self.request.user.pk != int(self.kwargs.get('owner_id'))):
	    raise Http404
	image = get_object_or_404(Image, pk=self.kwargs.get('image'), owner=self.request.user, imageset=str(self.request.user.pk) + '.' + str(self.kwargs.get('imageset_id')) )
	image.published = not image.published
	image.save()

	return HttpResponseRedirect(image.get_list_url())

class ImageDeleteView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
	if(self.request.user.pk != int(self.kwargs.get('owner_id'))):
	    raise Http404
	image = get_object_or_404(Image, pk=self.kwargs.get('image'), owner=self.request.user, imageset=str(self.request.user.pk) + '.' + str(self.kwargs.get('imageset_id')) )
	image.delete()

	return HttpResponseRedirect(image.get_list_url())

class ImageUploadView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageUploadForm
    template_name = 'image/imageUpload.html'

    def get_form_kwargs(self):
	kwargs = super(ImageUploadView, self).get_form_kwargs()
	kwargs['request'] = self.request
	return kwargs
    
    def form_valid(self, form):
	image = form.save(commit=False)
	image.owner = self.request.user
	image.image, image.image_type = self.handle_image(self.request.FILES['image'], image.imageset, image.owner)
	image.save()

	return HttpResponseRedirect(image.get_success_url())

    def handle_image(self, image_file, imageset, user):
	uuidinit = int(hashlib.sha512(str(datetime.datetime.utcnow()) + image_file.name).hexdigest()[-12:], 16)
	imageuuid = uuid.uuid1(uuidinit)
	ext = image_file.name.split('.')[-1]
	filename = "%s.%s" % (imageuuid, ext)
	filepath = os.path.join(settings.MEDIA_ROOT, str(user.pk), str(imageset.pk))
	filepathname = os.path.join(filepath, filename)

	if not os.path.exists(filepath):
	    os.makedirs(filepath)

	with open(filepathname, 'wb+') as destination:
            for chunk in image_file.chunks():
	        destination.write(chunk)

        im = PILImage.open(filepathname)
	width, height = im.size
	if height > 1200:
	    thumbnail = im
	    thumbnail.thumbnail((1600, 1200), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_f', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)
	
	if height > 1050:
	    thumbnail = im
	    thumbnail.thumbnail((1400, 1050), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_e', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)

	if height > 800:
	    thumbnail = im
	    thumbnail.thumbnail((1067, 800), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_d', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)
	
	if height > 576:
	    thumbnail = im
	    thumbnail.thumbnail((720, 576), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_c', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)

	if width > 400:
	    thumbnail = im
	    thumbnail.thumbnail((400, 300), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_b', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)

	if width > 250:
	    thumbnail = im
	    thumbnail.thumbnail((250, 190), PILImage.ANTIALIAS)
	    thumbnailfilename = "%s%s.%s" % (imageuuid, '_a', ext)
	    thumbnailfilepathname = os.path.join(filepath, thumbnailfilename)
	    thumbnail.save(thumbnailfilepathname)
	
	return (imageuuid, ext)


class ImageView(DetailView):
    model = Image
    template_name = 'image/image.html'

    def get(self, request, *args, **kwargs):
	image = get_object_or_404(Image, imageset=str(self.kwargs.get('owner_id')) + '.' + str(self.kwargs.get('imageset_id')), owner_id=self.kwargs.get('owner_id'), pk=self.kwargs.get('image'))
	if image.published is False and image.owner != self.request.user:
           raise Http404

	image_path = image.image + "." + image.image_type
	if not (self.kwargs.get('thumbnail') is None):
	    thumbnail = self.kwargs.get('thumbnail')
            image_thumbnail_path = image.image + "_" + thumbnail + "." + image.image_type
	    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(image.owner.pk), str(image.imageset.pk), image_thumbnail_path)):
		image_path = image_thumbnail_path
	    
	image_data = open(os.path.join(settings.MEDIA_ROOT, str(image.owner.pk), str(image.imageset.pk), image_path), "rb").read()
        return HttpResponse(image_data, content_type="image/" + image.image_type)

#	return super(ImageView, self).get(self, request, *args, **kwargs)

class RandomImageSetView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'image/imageSet.html'

    def get(self, request, *args, **kwargs):
	if( self.request.user.is_authenticated() ):
	    imageset = ImageSet.objects.filter(Q(published=True) | Q(owner=self.request.user)).order_by('?')
	else:
	    imageset = ImageSet.objects.filter(published=True).order_by('?')
	if( not imageset):
	    return HttpResponseRedirect(reverse('accounts_login'))
	return redirect(imageset[0])
	

class ImageSetView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'image/imageSet.html'

    def get_context_data(self, **kwargs):
	context = super(ImageSetView, self).get_context_data(**kwargs)
	context['imageset'] = get_object_or_404(ImageSet, imageset_id=self.kwargs.get('imageset_id'), owner=self.kwargs.get('owner_id'))
	return context

    def get_queryset(self):
	imageset = get_object_or_404(ImageSet, imageset_id=self.kwargs.get('imageset_id'), owner=self.kwargs.get('owner_id'))
	if imageset.published is False and imageset.owner != self.request.user:
	    raise Http404
	if imageset.owner == self.request.user:
            return Image.objects.filter(imageset=imageset).order_by('-created_at')

        return Image.objects.filter(imageset=imageset, published=True).order_by('-created_at')

class ImageSetsView(LoginRequiredMixin, ListView):
    model = ImageSet
    context_object_name = 'imagesets'
    template_name = 'image/imageSets.html'

    def get_queryset(self):
	page = 1
	if( self.kwargs.get('page') is not None ):
	    page = self.kwargs.get('page')

	imagesets = get_list_or_404(ImageSet.objects.order_by('created_at'), owner=self.request.user)
	paginator = Paginator(imagesets, 10)
	return paginator.page(page)

class ImagePublicSetsView(ListView):
    model = ImageSet
    context_object_name = 'imagesets'
    template_name = 'image/imageSets.html'

    def get_queryset(self):
	page = 1
	if( self.kwargs.get('page') is not None ):
	    page = self.kwargs.get('page')
	if( self.request.user.is_authenticated() ):
	    imagesets = get_list_or_404(ImageSet.objects.order_by('created_at'), Q(published=True) | Q(owner=self.request.user) )
	else:
	    imagesets = get_list_or_404(ImageSet.objects.order_by('created_at'), published=True )
	paginator = Paginator(imagesets, 10)
	return paginator.page(page)

class ImageSetListView(LoginRequiredMixin, ListView):
    model = ImageSet
    context_object_name = 'images'
    template_name = 'image/imageSetList.html'
    
    def get_context_data(self, **kwargs):
	context = super(ImageSetListView, self).get_context_data(**kwargs)
	context['imageset'] = get_object_or_404(ImageSet, imageset_id=self.kwargs.get('imageset_id'), owner=self.kwargs.get('owner_id'))
	return context

    def get_queryset(self):
	page = 1
        if( self.kwargs.get('page') is not None ):
            page = self.kwargs.get('page')

	imageset = get_object_or_404(ImageSet, imageset_id=self.kwargs.get('imageset_id'), owner=self.request.user)
        images = Image.objects.filter(imageset=imageset).order_by('-created_at')
	paginator = Paginator(images, 25)
	return paginator.page(page)

class ImageSetEditView(LoginRequiredMixin, UpdateView):
    model = ImageSet
    form_class = ImageSetEditForm
    template_name = 'image/imageSetEdit.html'
    
    def get(self, request, *args, **kwargs):
	if( int(self.kwargs.get('owner_id')) != self.request.user.pk ):
	    raise Http404
	return super(UpdateView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
	return get_object_or_404(ImageSet, owner=self.request.user, imageset_id=self.kwargs.get('imageset_id'))

    def form_valid(self, form):
	if(self.request.user.pk != int(self.kwargs.get('owner_id'))):
	    raise Http404

	imageset = form.save()
	return HttpResponseRedirect(imageset.get_absolute_url())

class ImageSetDeleteView(LoginRequiredMixin, UpdateView):
    model = ImageSet
    template_name = 'image/imageSets.html'

    def get(self, request, *args, **kwargs):
	if( int(self.kwargs.get('owner_id')) != self.request.user.pk ):
	    raise Http404
	imageset = get_object_or_404(ImageSet, imageset_id=self.kwargs.get('imageset_id'), owner=self.request.user)
        images = Image.objects.filter(imageset=imageset)
	for image in images:
	    folderpath = os.path.join(settings.MEDIA_ROOT, str(image.owner.pk), str(image.imageset.pk), str(image.image))
	    
	    imagepath = folderpath + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath)
	    imagepath = folderpath + "_f" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath)
	    imagepath = folderpath + "_e" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath)
	    imagepath = folderpath + "_d" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath) 
	    imagepath = folderpath + "_c" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath) 
	    imagepath = folderpath + "_b" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath) 
	    imagepath = folderpath + "_a" + str(image.type)
	    if( os.path.isfile(imagepath) ):
		os.remove(imagepath)
	folderpath = os.path.join(settings.MEDIA_ROOT, str(imageset.owner.pk), str(imageset.pk))
	if( os.path.isdir(folderpath) ):
	    os.rmdir(folderpath)
		
	images.delete()
	imageset.delete()
	return HttpResponseRedirect(imageset.get_list_url())

class ImageSetPublishView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
	if(self.request.user.pk != int(self.kwargs.get('owner_id'))):
	    raise Http404
	imageset = get_object_or_404(ImageSet, owner=self.request.user, imageset_id=self.kwargs.get('imageset_id'))
	imageset.published = not imageset.published
	imageset.save()

	return HttpResponseRedirect(imageset.get_list_url())


class ImageSetAddView(LoginRequiredMixin, CreateView):
    model = ImageSet
    form_class = ImageSetEditForm
    template_name = 'image/imageSetEdit.html'

    def get(self, request, *args, **kwargs):
	return super(CreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
	imageset = form.save(commit=False)
	
	imageset_id = get_object_or_404(ImageSet_id_seq, pk=self.request.user)
	imageset_id.imageset_id_seq = imageset_id.imageset_id_seq + 1
	imageset_id.save()
	
	imageset.imageset_id = imageset_id.imageset_id_seq
	imageset.owner = self.request.user
	imageset.save()

	os.mkdir(os.path.join(settings.MEDIA_ROOT, str(imageset.owner.pk), str(imageset.pk)))
	
	return HttpResponseRedirect(imageset.get_upload_url())
