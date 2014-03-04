from django.db import models
from django.contrib.auth.models import User

class BaseImageModel(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Image(BaseImageModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

    imageset = models.ForeignKey('ImageSet', null=True, blank=True)

    # def set

class ImageSet(BaseImageModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

     
