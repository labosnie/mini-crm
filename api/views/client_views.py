from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from clients.models import Client, Interaction
from api.serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ClientCreateUpdateSerializer,
    InteractionSerializer,
    InteractionCreateSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des clients via API
    """
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'ville', 'pays']
    search_fields = ['nom', 'prenom', 'email', 'ville']
    ordering_fields = ['nom', 'prenom', 'date_creation', 'statut']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'retrieve':
            return ClientDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClientCreateUpdateSerializer
        return ClientSerializer

    def get_queryset(self):
        """Filtrage personnalisé du queryset"""
        queryset = Client.objects.all()
        
        # Filtrage par date de création
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(date_creation__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date_creation__lte=date_fin)
        
        return queryset

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """Récupérer les interactions d'un client"""
        client = self.get_object()
        interactions = client.interactions.all()
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_interaction(self, request, pk=None):
        """Ajouter une interaction à un client"""
        client = self.get_object()
        serializer = InteractionCreateSerializer(
            data=request.data,
            context={'client_id': client.id, 'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des clients"""
        total_clients = Client.objects.count()
        clients_actifs = Client.objects.filter(statut='actif').count()
        clients_prospects = Client.objects.filter(statut='prospect').count()
        clients_inactifs = Client.objects.filter(statut='inactif').count()
        
        return Response({
            'total_clients': total_clients,
            'clients_actifs': clients_actifs,
            'clients_prospects': clients_prospects,
            'clients_inactifs': clients_inactifs,
        })

    def perform_create(self, serializer):
        """Logique personnalisée lors de la création"""
        serializer.save()

    def perform_update(self, serializer):
        """Logique personnalisée lors de la mise à jour"""
        serializer.save() 