from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Quiz API",
      default_version='v1',
      description="API documentation for the Quiz app",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include('blog.urls')),
    path('cv/', include('cv.urls')),
    path('accaunts/', include('authentication.urls')),
    path('api/', include('api.urls')),
    path('problems/', include('problems.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
