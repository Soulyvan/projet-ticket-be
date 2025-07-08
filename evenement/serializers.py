from rest_framework import serializers
from .models import *


# Sérialiseur pour CategorieEvenement
class CategorieEvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieEvenement
        fields = ['id', 'nom', 'billets_restant', 'prix']
        # read_only_fields = ['evenement']


class CategorieEvenementSerializerCascade(serializers.ModelSerializer):
    class Meta:
        model = CategorieEvenement
        fields = ['id', 'nom', 'billets_restant', 'prix']


# Sérialiseur pour la création d'un événement
class EvenementSerializer(serializers.ModelSerializer):
    categories = CategorieEvenementSerializer(many=True)

    class Meta:
        model = Evenement
        fields = [
            'id', 'nom', 'slug', 'photo', 'description',
            'type_evenement', 'date_heure', 'lieu', 'organisateur', 'categories'
        ]
        read_only_fields = ['organisateur', 'slug']

    def create(self, validated_data):
        # Extraire les données des catégories
        categories_data = validated_data.pop('categories', [])

        # Créer l'événement principal
        evenement = Evenement.objects.create(**validated_data)

        # Créer les catégories associées
        categories = [
            CategorieEvenement(evenement=evenement, **categorie_data)
            for categorie_data in categories_data
        ]
        CategorieEvenement.objects.bulk_create(categories)  # Création en lot

        return evenement



class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'token', 'categorie_evenement', 'valide', 'date_creation', 'qr_image', 'utilisateur']


class QRCodeDetailSerializer(serializers.ModelSerializer):
    utilisateur_username = serializers.CharField(source="utilisateur.username", read_only=True)
    categorie_nom = serializers.CharField(source="categorie_evenement.nom", read_only=True)
    evenement_nom = serializers.CharField(source="categorie_evenement.evenement.nom", read_only=True)

    class Meta:
        model = QRCode
        fields = [
            'id',
            'token',
            'categorie_evenement',
            'categorie_nom',
            'evenement_nom',
            'valide',
            'date_creation',
            'qr_image',
            'utilisateur',
            'utilisateur_username'
        ]


class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = ['id', 'acheteur', 'evenement', 'categorie_evenement', 'prix_billet', 'nombre_places_payees', 'date_achat']

