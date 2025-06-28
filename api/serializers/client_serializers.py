from rest_framework import serializers
from clients.models import Client, Interaction, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer pour les tags"""

    class Meta:
        model = Tag
        fields = ["id", "nom", "couleur"]


class InteractionSerializer(serializers.ModelSerializer):
    """Serializer pour les interactions"""

    utilisateur = serializers.ReadOnlyField(source="utilisateur.username")

    class Meta:
        model = Interaction
        fields = ["id", "type", "date", "description", "utilisateur"]
        read_only_fields = ["date", "utilisateur"]


class ClientSerializer(serializers.ModelSerializer):
    """Serializer principal pour les clients"""

    tags = TagSerializer(many=True, read_only=True)
    interactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "id",
            "nom",
            "prenom",
            "email",
            "telephone",
            "adresse",
            "ville",
            "code_postal",
            "pays",
            "statut",
            "notes",
            "date_creation",
            "date_modification",
            "tags",
            "interactions_count",
        ]
        read_only_fields = ["date_creation", "date_modification"]

    def get_interactions_count(self, obj):
        return obj.interactions.count()


class ClientDetailSerializer(ClientSerializer):
    """Serializer détaillé pour les clients avec interactions"""

    interactions = InteractionSerializer(many=True, read_only=True)

    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + ["interactions"]


class ClientCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et modification des clients"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )

    class Meta:
        model = Client
        fields = [
            "nom",
            "prenom",
            "email",
            "telephone",
            "adresse",
            "ville",
            "code_postal",
            "pays",
            "statut",
            "notes",
            "tags",
        ]

    def validate_email(self, value):
        """Validation personnalisée pour l'email"""
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un client avec cet email existe déjà.")
        return value


class InteractionCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une interaction"""

    class Meta:
        model = Interaction
        fields = ["type", "description"]

    def create(self, validated_data):
        validated_data["client_id"] = self.context["client_id"]
        validated_data["utilisateur"] = self.context["request"].user
        return super().create(validated_data)
