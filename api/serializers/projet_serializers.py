from rest_framework import serializers
from projets.models import Projet
from clients.models import Client
from factures.models import Facture


class ClientMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les clients dans les projets"""
    class Meta:
        model = Client
        fields = ['id', 'nom', 'prenom', 'email']


class FactureMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les factures dans les projets"""
    statut_paiement_display = serializers.CharField(
        source='get_statut_paiement_display', 
        read_only=True
    )
    
    class Meta:
        model = Facture
        fields = ['id', 'numero', 'montant', 'statut_paiement', 'statut_paiement_display']


class ProjetSerializer(serializers.ModelSerializer):
    """Serializer principal pour les projets"""
    client = ClientMinimalSerializer(read_only=True)
    statut_display = serializers.CharField(
        source='get_statut_display', 
        read_only=True
    )
    factures_count = serializers.SerializerMethodField()
    montant_total_factures = serializers.SerializerMethodField()
    
    class Meta:
        model = Projet
        fields = [
            'id', 'titre', 'description', 'client', 'date_debut', 'date_fin',
            'statut', 'statut_display', 'montant', 'date_creation',
            'date_modification', 'factures_count', 'montant_total_factures'
        ]
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_factures_count(self, obj):
        return obj.factures.count()
    
    def get_montant_total_factures(self, obj):
        return sum(facture.montant for facture in obj.factures.all())


class ProjetDetailSerializer(ProjetSerializer):
    """Serializer détaillé pour les projets avec factures"""
    factures = FactureMinimalSerializer(many=True, read_only=True)
    
    class Meta(ProjetSerializer.Meta):
        fields = ProjetSerializer.Meta.fields + ['factures']


class ProjetCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et modification des projets"""
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    
    class Meta:
        model = Projet
        fields = [
            'titre', 'description', 'client', 'date_debut', 'date_fin',
            'statut', 'montant'
        ]
    
    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que la date de fin est après la date de début
        if data.get('date_fin') and data['date_fin'] < data['date_debut']:
            raise serializers.ValidationError(
                "La date de fin doit être postérieure à la date de début."
            )
        
        # Vérifier que le montant est positif s'il est fourni
        if data.get('montant') and data['montant'] <= 0:
            raise serializers.ValidationError(
                "Le montant doit être supérieur à zéro."
            )
        
        return data


class ProjetStatutUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour uniquement le statut"""
    class Meta:
        model = Projet
        fields = ['statut'] 