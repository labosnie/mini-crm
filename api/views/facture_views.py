from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)
import os
from datetime import datetime

from factures.models import Facture
from api.serializers import (
    FactureSerializer,
    FactureDetailSerializer,
    FactureCreateUpdateSerializer,
    FactureStatutUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Liste des factures",
        description="Récupère la liste paginée de toutes les factures avec possibilité de filtrage et recherche",
        tags=["factures"],
        parameters=[
            OpenApiParameter(
                name="search",
                description="Recherche dans numéro, client, projet",
                required=False,
            ),
            OpenApiParameter(
                name="statut_paiement",
                description="Filtrer par statut de paiement",
                required=False,
            ),
            OpenApiParameter(
                name="client", description="Filtrer par client", required=False
            ),
            OpenApiParameter(
                name="projet", description="Filtrer par projet", required=False
            ),
            OpenApiParameter(
                name="date_debut",
                description="Date de début (YYYY-MM-DD)",
                required=False,
            ),
            OpenApiParameter(
                name="date_fin", description="Date de fin (YYYY-MM-DD)", required=False
            ),
        ],
    ),
    create=extend_schema(
        summary="Créer une facture",
        description="Crée une nouvelle facture avec génération automatique du numéro",
        tags=["factures"],
    ),
    retrieve=extend_schema(
        summary="Détails d'une facture",
        description="Récupère les détails complets d'une facture",
        tags=["factures"],
    ),
    update=extend_schema(
        summary="Modifier une facture",
        description="Met à jour complètement une facture",
        tags=["factures"],
    ),
    partial_update=extend_schema(
        summary="Modifier partiellement une facture",
        description="Met à jour partiellement une facture",
        tags=["factures"],
    ),
    destroy=extend_schema(
        summary="Supprimer une facture",
        description="Supprime définitivement une facture",
        tags=["factures"],
    ),
)
class FactureViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des factures via API
    """

    queryset = Facture.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["statut_paiement", "client", "projet"]
    search_fields = ["numero", "client__nom", "projet__titre"]
    ordering_fields = [
        "numero",
        "date_emission",
        "date_echeance",
        "montant",
        "statut_paiement",
    ]
    ordering = ["-date_emission"]

    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == "retrieve":
            return FactureDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return FactureCreateUpdateSerializer
        elif self.action == "update_statut":
            return FactureStatutUpdateSerializer
        return FactureSerializer

    def get_queryset(self):
        """Filtrage personnalisé du queryset"""
        queryset = Facture.objects.all()

        # Filtrage par date d'émission
        date_debut = self.request.query_params.get("date_debut", None)
        date_fin = self.request.query_params.get("date_fin", None)

        if date_debut:
            queryset = queryset.filter(date_emission__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date_emission__lte=date_fin)

        return queryset

    @extend_schema(
        summary="Télécharger PDF",
        description="Génère et télécharge le PDF d'une facture",
        tags=["factures"],
        responses={200: None, 500: None},
    )
    @action(detail=True, methods=["get"])
    def pdf(self, request, pk=None):
        """Télécharger le PDF d'une facture"""
        facture = self.get_object()
        try:
            filepath = facture.generer_pdf()
            if os.path.exists(filepath):
                response = FileResponse(
                    open(filepath, "rb"), content_type="application/pdf"
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="facture_{facture.numero}.pdf"'
                )
                return response
            else:
                return Response(
                    {"error": "Le PDF n'a pas pu être généré"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la génération du PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Mettre à jour le statut",
        description="Met à jour uniquement le statut de paiement d'une facture",
        tags=["factures"],
    )
    @action(detail=True, methods=["patch"])
    def update_statut(self, request, pk=None):
        """Mettre à jour uniquement le statut d'une facture"""
        facture = self.get_object()
        serializer = self.get_serializer(facture, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Factures en retard",
        description="Récupère toutes les factures en retard de paiement",
        tags=["factures"],
    )
    @action(detail=False, methods=["get"])
    def en_retard(self, request):
        """Récupérer les factures en retard"""
        factures = Facture.objects.filter(statut_paiement="en_retard")
        serializer = self.get_serializer(factures, many=True)
        return Response({"factures_en_retard": serializer.data})

    @extend_schema(
        summary="Statistiques des factures",
        description="Récupère les statistiques globales des factures",
        tags=["factures"],
    )
    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Statistiques des factures"""
        total_factures = Facture.objects.count()
        factures_payees = Facture.objects.filter(statut_paiement="payée").count()
        factures_en_retard = Facture.objects.filter(statut_paiement="en_retard").count()
        factures_envoyees = Facture.objects.filter(statut_paiement="envoyée").count()
        factures_en_attente = Facture.objects.filter(statut_paiement="envoyée").count()

        # Calcul du montant total
        montant_total = sum(f.montant for f in Facture.objects.all())
        montant_paye = sum(
            f.montant for f in Facture.objects.filter(statut_paiement="payée")
        )

        return Response(
            {
                "total_factures": total_factures,
                "factures_payees": factures_payees,
                "factures_en_retard": factures_en_retard,
                "factures_envoyees": factures_envoyees,
                "factures_en_attente": factures_en_attente,
                "montant_total": float(montant_total),
                "montant_paye": float(montant_paye),
                "taux_paiement": (
                    float(montant_paye / montant_total * 100)
                    if montant_total > 0
                    else 0
                ),
            }
        )

    def perform_create(self, serializer):
        """Logique personnalisée lors de la création"""
        serializer.save()

    def perform_update(self, serializer):
        """Logique personnalisée lors de la mise à jour"""
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        output_serializer = FactureDetailSerializer(
            instance, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        output_serializer = FactureDetailSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(output_serializer.data)
