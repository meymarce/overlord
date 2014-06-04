from django import forms

from .models import *

class ImageUploadForm(forms.ModelForm):

    class Meta:
	model = Image
	fields = ('title', 'description', 'imageset', 'published')

    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
	self.request = kwargs.pop('request')
	super(ImageUploadForm, self).__init__(*args, **kwargs)
	self.fields['imageset'].queryset = ImageSet.objects.filter(owner=self.request.user).order_by('created_at')
	self.fields['imageset'].empty_label = None

class ImageSetEditForm(forms.ModelForm):

    class Meta:
	model = ImageSet
	fields = ('title', 'description', 'published')

class ImageEditForm(forms.ModelForm):

    class Meta:
	model = Image
	fields = ('title', 'description', 'imageset', 'published')

    def __init__(self, *args, **kwargs):
	self.request = kwargs.pop('request')
	super(ImageEditForm, self).__init__(*args, **kwargs)
	self.fields['imageset'].queryset = ImageSet.objects.filter(owner=self.request.user).order_by('created_at')
	self.fields['imageset'].empty_label = None
