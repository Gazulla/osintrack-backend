from django.urls import path
from api.views import narrative_views as views

urlpatterns = [
    path("", views.getNarratives, name="narratives"),
    path("create/", views.createNarrative, name="create-narrative"),
    path("<str:pk>/", views.getNarrative, name="narrative-details"),
    path("update/<str:pk>/", views.updateNarrative, name="update-narrative"),
    path("delete/<str:pk>/", views.deleteNarrative, name="delete-narrative"),
]
