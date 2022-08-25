from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .urls import *
urlpatterns = [
    *urlpatterns,

    # https://docs.djangoproject.com/en/2.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    # add support static files at wsgi mode, (not by manage.py runserver)
    # https://stackoverflow.com/questions/12800862/how-to-make-django-serve-static-files-with-gunicorn
    *staticfiles_urlpatterns(),
]
