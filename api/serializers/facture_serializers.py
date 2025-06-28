from rest_framework import serializers
from factures.models import Facture
from clients.models import Client
from projets.models import Projet


class ClientMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les clients dans les factures"""

    class Meta:
        model = Client
        fields = ["id", "nom", "prenom", "email"]


class ProjetMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les projets dans les factures"""

    class Meta:
        model = Projet
        fields = ["id", "titre", "statut"]


class FactureSerializer(serializers.ModelSerializer):
    """Serializer principal pour les factures"""

    client = ClientMinimalSerializer(read_only=True)
    projet = ProjetMinimalSerializer(read_only=True)
    statut_paiement_display = serializers.CharField(
        source="get_statut_paiement_display", read_only=True
    )

    class Meta:
        model = Facture
        fields = [
            "id",
            "numero",
            "client",
            "projet",
            "montant",
            "date_emission",
            "date_echeance",
            "statut_paiement",
            "statut_paiement_display",
            "notes",
        ]
        read_only_fields = ["numero", "date_emission"]


class FactureDetailSerializer(FactureSerializer):
    """Serializer détaillé pour les factures"""

    class Meta(FactureSerializer.Meta):
        fields = FactureSerializer.Meta.fields


class FactureCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et modification des factures"""

    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    projet = serializers.PrimaryKeyRelatedField(queryset=Projet.objects.all())

    class Meta:
        model = Facture
        fields = [
            "client",
            "projet",
            "montant",
            "date_echeance",
            "statut_paiement",
            "notes",
        ]

    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que le projet appartient au client
        if data["projet"].client != data["client"]:
            raise serializers.ValidationError(
                "Le projet doit appartenir au client sélectionné."
            )

        # Vérifier que le montant est positif
        if data["montant"] <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à zéro.")

        return data

    def create(self, validated_data):
        """Création avec génération automatique du numéro"""
        facture = Facture.objects.create(**validated_data)
        return facture


class FactureStatutUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour uniquement le statut"""

    class Meta:
        model = Facture
        fields = ["statut_paiement"]
