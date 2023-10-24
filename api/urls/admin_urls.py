from django.urls import path
from api.views import admin_views as views

urlpatterns = [
    path("settings/", views.getAppSettings, name="get-app-settings"),
    path("settings/update/", views.updateAppSettings, name="update-app-settings"),
]
