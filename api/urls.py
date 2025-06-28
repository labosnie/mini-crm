from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api.views import ClientViewSet, FactureViewSet, ProjetViewSet

# Configuration du router pour les ViewSets
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'factures', FactureViewSet, basename='facture')
router.register(r'projets', ProjetViewSet, basename='projet')

# URLs de l'API
urlpatterns = [
    # Endpoints d'authentification
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Endpoints des ViewSets
    path('', include(router.urls)),
    
    # Endpoint racine de l'API
    path('', include('rest_framework.urls')),
] 