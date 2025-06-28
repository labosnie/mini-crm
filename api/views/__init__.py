# Views package
from .client_views import ClientViewSet
from .facture_views import FactureViewSet
from .projet_views import ProjetViewSet

__all__ = [
    'ClientViewSet',
    'FactureViewSet', 
    'ProjetViewSet',
] 