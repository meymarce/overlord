rom django.conf import settings


MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', os.path.join(BASE_DIR, 'image/data/'))
