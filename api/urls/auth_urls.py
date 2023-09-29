from django.urls import path
from api.views import auth_views as views

urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="login"),
]
