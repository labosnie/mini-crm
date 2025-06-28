# Serializers package
from .client_serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ClientCreateUpdateSerializer,
    InteractionSerializer,
    InteractionCreateSerializer,
    TagSerializer,
)

from .facture_serializers import (
    FactureSerializer,
    FactureDetailSerializer,
    FactureCreateUpdateSerializer,
    FactureStatutUpdateSerializer,
)

from .projet_serializers import (
    ProjetSerializer,
    ProjetDetailSerializer,
    ProjetCreateUpdateSerializer,
    ProjetStatutUpdateSerializer,
)

from .user_serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)

__all__ = [
    # Client serializers
    "ClientSerializer",
    "ClientDetailSerializer",
    "ClientCreateUpdateSerializer",
    "InteractionSerializer",
    "InteractionCreateSerializer",
    "TagSerializer",
    # Facture serializers
    "FactureSerializer",
    "FactureDetailSerializer",
    "FactureCreateUpdateSerializer",
    "FactureStatutUpdateSerializer",
    # Projet serializers
    "ProjetSerializer",
    "ProjetDetailSerializer",
    "ProjetCreateUpdateSerializer",
    "ProjetStatutUpdateSerializer",
    # User serializers
    "UserSerializer",
    "UserCreateSerializer",
    "UserUpdateSerializer",
    "ChangePasswordSerializer",
]
