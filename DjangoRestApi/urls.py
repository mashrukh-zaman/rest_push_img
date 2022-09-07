from django.urls import include, re_path, path

from tutorials.views import tutorial_list
from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tutorials.views import *

urlpatterns = [ 
    path('', include('tutorials.urls')),
    path('image_upload', tutorial_list, name = 'image_upload'),
    # path('success', success, name = 'success'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)