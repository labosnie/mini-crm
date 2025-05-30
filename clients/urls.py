from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListViews.as_view(), name='client_list'),
    path('<int:pk>/', views.ClientDetailViews.as_view(), name='client_detail'),
    path('nouveau/', views.ClientCreateViews.as_view(), name='client_create'),
    path('<int:pk>/modifier/', views.ClientUpdateViews.as_view(), name='client_update'),
    path('<int:pk>/supprimer/', views.ClientDeleteViews.as_view(), name='client_delete'),
]
