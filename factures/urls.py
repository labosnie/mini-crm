from django.urls import path
from . import views

app_name = 'factures'

urlpatterns = [
    path('', views.facture_list, name='facture_list'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('nouvelle/', views.facture_create, name='facture_create'),
    path('<int:pk>/modifier/', views.facture_update, name='facture_update'),
    path('<int:pk>/supprimer/', views.facture_delete, name='facture_delete'),
    path('get-projets-client/', views.get_projets_client, name='get_projets_client'),
] 