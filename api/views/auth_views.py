from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from clients.models import Client
from api.serializers import UserSerializer, UserCreateSerializer


@extend_schema(
    summary="Obtenir un token d'authentification",
    description="Authentifie un utilisateur et retourne un token d'accès",
    tags=["authentification"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': 'Nom d\'utilisateur'},
                'password': {'type': 'string', 'description': 'Mot de passe'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'description': 'Authentification réussie',
            'type': 'object',
            'properties': {
                'token': {'type': 'string', 'description': 'Token d\'accès'},
                'user_id': {'type': 'integer', 'description': 'ID de l\'utilisateur'},
                'username': {'type': 'string', 'description': 'Nom d\'utilisateur'},
                'email': {'type': 'string', 'description': 'Email de l\'utilisateur'},
            }
        },
        400: {
            'description': 'Données invalides',
            'type': 'object',
            'properties': {
                'non_field_errors': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Messages d\'erreur'
                }
            }
        }
    },
    examples=[
        OpenApiExample(
            'Exemple de succès',
            value={
                'token': '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
                'user_id': 1,
                'username': 'admin',
                'email': 'admin@example.com'
            },
            response_only=True,
            status_codes=['200']
        ),
        OpenApiExample(
            'Exemple d\'erreur',
            value={
                'non_field_errors': ['Impossible de se connecter avec les identifiants fournis.']
            },
            response_only=True,
            status_codes=['400']
        )
    ]
)
class CustomObtainAuthToken(ObtainAuthToken):
    """
    Vue personnalisée pour l'obtention de token d'authentification
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Inscription d'un nouvel utilisateur",
    description="Crée un nouveau compte utilisateur avec validation des données",
    tags=["authentification"],
    request=UserCreateSerializer,
    responses={
        201: {
            'description': 'Utilisateur créé avec succès',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'description': 'ID de l\'utilisateur'},
                'username': {'type': 'string', 'description': 'Nom d\'utilisateur'},
                'email': {'type': 'string', 'description': 'Email de l\'utilisateur'},
                'first_name': {'type': 'string', 'description': 'Prénom'},
                'last_name': {'type': 'string', 'description': 'Nom'},
            }
        },
        400: {
            'description': 'Données invalides',
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Erreurs de validation du nom d\'utilisateur'
                },
                'email': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Erreurs de validation de l\'email'
                },
                'password': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Erreurs de validation du mot de passe'
                }
            }
        }
    },
    examples=[
        OpenApiExample(
            'Exemple de succès',
            value={
                'id': 2,
                'username': 'nouveau_user',
                'email': 'nouveau@example.com',
                'first_name': 'Jean',
                'last_name': 'Dupont'
            },
            response_only=True,
            status_codes=['201']
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Inscription d'un nouvel utilisateur
    """
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Retourner les données avec UserSerializer pour masquer le mot de passe
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Vérifier l'authentification",
    description="Vérifie si l'utilisateur est authentifié et retourne ses informations",
    tags=["authentification"],
    responses={
        200: {
            'description': 'Utilisateur authentifié',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'description': 'ID de l\'utilisateur'},
                'username': {'type': 'string', 'description': 'Nom d\'utilisateur'},
                'email': {'type': 'string', 'description': 'Email de l\'utilisateur'},
                'first_name': {'type': 'string', 'description': 'Prénom'},
                'last_name': {'type': 'string', 'description': 'Nom'},
                'is_authenticated': {'type': 'boolean', 'description': 'Statut d\'authentification'},
            }
        },
        401: {
            'description': 'Non authentifié',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'description': 'Message d\'erreur'}
            }
        }
    }
)
@api_view(['GET'])
def user_info(request):
    """
    Récupérer les informations de l'utilisateur connecté
    """
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        data = serializer.data
        data['is_authenticated'] = True
        return Response(data)
    return Response(
        {'detail': 'Non authentifié'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    summary="Déconnexion",
    description="Invalide le token d'authentification de l'utilisateur",
    tags=["authentification"],
    responses={
        200: {
            'description': 'Déconnexion réussie',
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'description': 'Message de confirmation'}
            }
        }
    }
)
@api_view(['POST'])
def logout(request):
    """
    Déconnexion de l'utilisateur (invalidation du token)
    """
    try:
        # Supprimer le token de l'utilisateur
        request.user.auth_token.delete()
        return Response({'message': 'Déconnexion réussie'})
    except:
        return Response({'message': 'Déconnexion réussie'}) 