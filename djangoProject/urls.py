from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from djangoProject import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Test Project",
        default_version='v1',
        description=f"TEST TEST TEST",
        contact=openapi.Contact(email="a@a.uz")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = \
    [
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('admin/', admin.site.urls),
        path('api/v1/', include('apps.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
