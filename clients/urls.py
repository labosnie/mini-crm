from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('<int:pk>/', views.client_detail, name='client_detail'),
    path('nouveau/', views.client_create, name='client_create'),
    path('<int:pk>/modifier/', views.client_update, name='client_update'),
    path('<int:pk>/supprimer/', views.client_delete, name='client_delete'),
]
