from django.contrib import admin
from django.urls import path,include,re_path


# ==================drf_yasg=============
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="counst API",
      default_version='v1',
      description="Test description",
      contact=openapi.Contact(email="kienndk09@gmail.com"),
      license=openapi.License(name="Nguyễn Đức Kiên"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# ========== end drf_yasg ==================



urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("__debug__/", include("debug_toolbar.urls")),
]
