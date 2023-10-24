from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =  [
    path("admin/", admin.site.urls),
    path("api/auth/", include("api.urls.auth_urls")),
    path("api/narratives/", include("api.urls.narrative_urls")),
    path("api/admin/", include("api.urls.admin_urls")),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
