from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.liste_notifications, name="liste"),
    path(
        "<int:notification_id>/marquer-lu/", views.marquer_comme_lu, name="marquer_lu"
    ),
]
