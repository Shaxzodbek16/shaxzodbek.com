from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include('blog.urls')),
    path('cv/', include('cv.urls')),
    path('accaunts/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
