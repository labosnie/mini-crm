from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api.views.client_views import ClientViewSet
from api.views.facture_views import FactureViewSet
from api.views.projet_views import ProjetViewSet
from api.views.auth_views import CustomObtainAuthToken, register, user_info, logout

app_name = "api"

# Configuration du routeur
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'factures', FactureViewSet)
router.register(r'projets', ProjetViewSet)

# URLs de l'API
urlpatterns = [
    # Documentation Swagger/OpenAPI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
    
    # Authentification
    path('auth/login/', CustomObtainAuthToken.as_view(), name='auth_login'),
    path('auth/register/', register, name='auth_register'),
    path('auth/user/', user_info, name='auth_user'),
    path('auth/logout/', logout, name='auth_logout'),
    
    # Endpoints principaux
    path('', include(router.urls)),
] 