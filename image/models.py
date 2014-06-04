from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

import uuid
import hashlib
import datetime
import os

def getUserspecificUploadPath(instance, filename):
    uuidinit = int(hashlib.sha512(str(datetime.datetime.utcnow()) + filename).hexdigest()[-12:], 16)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid1(uuidinit), ext)
    return os.path.join(settings.MEDIA_ROOT, str(instance.owner.pk), str(instance.imageset.pk), filename)


class BaseImageModel(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Image(BaseImageModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

    imageset = models.ForeignKey('ImageSet', null=True, blank=True)

    image = models.CharField(max_length=100, primary_key=True)
    image_type = models.CharField(max_length=5)
#    image = models.ImageField(upload_to=getUserspecificUploadPath)

    def __unicode__(self):
	return self.title

    def get_success_url(self):
	return reverse('imageset', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id})

    def get_edit_url(self):
	return reverse('image_edit', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id, 'image': self.image})
    
    def get_delete_url(self):
	return reverse('image_delete', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id, 'image': self.image})

    def get_publish_url(self):
	return reverse('image_publish', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id, 'image': self.image})

    def get_image_url(self):
	return reverse('image', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id, 'image': self.image})

    def get_image_thumbnail_url(self):
	return reverse('image', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id, 'image': (self.image + "_b")})

    def get_list_url(self):
	return reverse('imageset_list', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset.imageset_id})

class ImageSet(BaseImageModel):
    class Meta:
	unique_together =(('imageset_id', 'owner'),)

    primary_key = models.CharField(max_length=511, primary_key=True)
    imageset_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def save(self, *args, **kwargs):
	print self.owner
	self.primary_key = str(self.owner.pk) + '.' + str(self.imageset_id)
	super(BaseImageModel, self).save(*args, **kwargs)

    def __unicode__(self):
	return self.title

    def get_absolute_url(self):
	return reverse('imageset', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset_id})

    def get_upload_url(self):
	return reverse('upload')

    def get_edit_url(self):
	return reverse('imageset_edit', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset_id})

    def get_delete_url(self):
	return reverse('imageset_delete', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset_id})

    def get_publish_url(self):
	return reverse('imageset_publish', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset_id})

    def get_list_url(self):
	return reverse('imagesets')
    
    def get_image_list_url(self):
	return reverse('imageset_list', kwargs={'owner_id': self.owner.pk, 'imageset_id': self.imageset_id})

class ImageSet_id_seq(models.Model):
    owner = models.ForeignKey(User, primary_key=True)
    imageset_id_seq = models.IntegerField()
