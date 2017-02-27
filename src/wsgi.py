import os

from dj_static import Cling, MediaCling
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

if settings.DEBUG:
    application = Cling(MediaCling(get_wsgi_application()))
else:
    application = get_wsgi_application()
