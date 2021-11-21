from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path("home/",views.home,name="home"),
   path("download",views.download_pdf,name="download"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)