from django.urls import path
from .views import *

urlpatterns = [
    path('evenements/', EvenementListCreateAPIView.as_view(), name='evenement-liste-creer'),
    path('evenements/<int:pk>/afficher/', EvenementDetailAPIView.as_view(), name='evenement-afficher'),
    path('evenements/<int:pk>/modifier/', EvenementUpdateAPIView.as_view(), name='evenement-modifier'),
    path('evenements/<int:pk>/supprimer/', EvenementDeleteAPIView.as_view(), name='evenement-supprimer'),

    # Routes pour les catégories d'événements
    path('evenements/categories/<int:evenement_id>/', CategorieEvenementCreateAPIView.as_view(),
         name='categorie-create'),
    path('evenements/categories/<int:pk>/', CategorieEvenementDetailAPIView.as_view(), name='categorie-detail'),
    path('evenements/categories/<int:pk>/delete/', CategorieEvenementDeleteAPIView.as_view(), name='categorie-delete'),

    # Création d'un QR code après le paiement
    path('qrcode/creer/', CreateCheckoutSessionView.as_view(), name='qrcode-creer'),

    # affichage des infos d'un QR code
    path('qrcode/<uuid:token>/', QRCodeDetailView.as_view(), name='qrcode-detail'),

    # invalider un QR code
    path('qrcode/invalide/<uuid:token>/', QRCodeInvalidate.as_view(), name='qrcode-invalide'),

    path('historique/', HistoriqueListView.as_view(), name='historique-list'),

    # Webhook Stripe pour finaliser le processus
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),

    # récupérer tous mes qrcodes
    path('qrcodes/', QRCodeListAPIView.as_view(), name='get_qrcodes_by_user'),

    path('success/', paiement_succes, name='paiement-succes'),
]
