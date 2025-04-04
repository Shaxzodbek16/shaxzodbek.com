from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap


from core.settings import Config
from .sitemaps import StaticViewSitemap


config: Config = Config()
sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    # admin url
    path(f"{config.ADMIN_URL}/", admin.site.urls),
    # include apps urls
    path("", include("blog.urls")),
    path("", include("lessons.urls")),

    # icons
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/img/apple-touch-icon.png')),
    path('apple-touch-icon-precomposed.png', RedirectView.as_view(url='/static/img/apple-touch-icon-precomposed.png')),

    # sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # robots.txt
    path('robots.txt', RedirectView.as_view(url='/static/robots.txt', permanent=True)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
