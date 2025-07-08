from django.contrib import admin
from .models import *


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_evenement', 'organisateur')


@admin.register(CategorieEvenement)
class CategorieEvenementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'billets_restant', 'prix', 'evenement')


@admin.register(QRCode)
class CategorieEvenementAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_image', 'valide', 'token', 'date_creation')


@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('acheteur', 'evenement', 'categorie_evenement', 'prix_billet', 'nombre_places_payees', 'date_achat')