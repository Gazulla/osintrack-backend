from django.urls import path
from api.views import profile_views as views

urlpatterns = [
    path("", views.getProfile, name="get-profile"),
    path("update/", views.updateProfile, name="update-profile"),
    path("image/update/", views.updateProfileImage, name="update-profile-image"),
    path("password/update/", views.updatePassword, name="update-password"),

]
