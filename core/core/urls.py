from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from core.settings import Config

config: Config = Config()

urlpatterns = [
    path(f"{config.ADMIN_URL}/", admin.site.urls),
    path("", include("blog.urls")),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/img/apple-touch-icon.png')),
    path('apple-touch-icon-precomposed.png', RedirectView.as_view(url='/static/img/apple-touch-icon-precomposed.png')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
