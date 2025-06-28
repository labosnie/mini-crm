from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from projets.models import Projet
from api.serializers import (
    ProjetSerializer,
    ProjetDetailSerializer,
    ProjetCreateUpdateSerializer,
    ProjetStatutUpdateSerializer,
)


class ProjetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets via API
    """
    queryset = Projet.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'client']
    search_fields = ['titre', 'description', 'client__nom']
    ordering_fields = ['titre', 'date_debut', 'date_fin', 'statut', 'montant']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'retrieve':
            return ProjetDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjetCreateUpdateSerializer
        elif self.action == 'update_statut':
            return ProjetStatutUpdateSerializer
        return ProjetSerializer

    def get_queryset(self):
        """Filtrage personnalisé du queryset"""
        queryset = Projet.objects.all()
        
        # Filtrage par date de début
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(date_debut__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date_debut__lte=date_fin)
        
        return queryset

    @action(detail=True, methods=['get'])
    def factures(self, request, pk=None):
        """Récupérer les factures d'un projet"""
        projet = self.get_object()
        factures = projet.factures.all()
        from api.serializers import FactureSerializer
        serializer = FactureSerializer(factures, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_statut(self, request, pk=None):
        """Mettre à jour uniquement le statut d'un projet"""
        projet = self.get_object()
        serializer = self.get_serializer(projet, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def en_cours(self, request):
        """Récupérer les projets en cours"""
        projets = Projet.objects.filter(statut='en_cours')
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def termines(self, request):
        """Récupérer les projets terminés"""
        projets = Projet.objects.filter(statut='termine')
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des projets"""
        total_projets = Projet.objects.count()
        projets_en_cours = Projet.objects.filter(statut='en_cours').count()
        projets_termines = Projet.objects.filter(statut='termine').count()
        projets_en_attente = Projet.objects.filter(statut='en_attente').count()
        projets_annules = Projet.objects.filter(statut='annule').count()
        
        # Calcul du montant total
        montant_total = sum(p.montant for p in Projet.objects.all() if p.montant)
        
        return Response({
            'total_projets': total_projets,
            'projets_en_cours': projets_en_cours,
            'projets_termines': projets_termines,
            'projets_en_attente': projets_en_attente,
            'projets_annules': projets_annules,
            'montant_total': float(montant_total) if montant_total else 0,
        })

    def perform_create(self, serializer):
        """Logique personnalisée lors de la création"""
        serializer.save()

    def perform_update(self, serializer):
        """Logique personnalisée lors de la mise à jour"""
        serializer.save() 