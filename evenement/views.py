import base64
import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify
from .models import Evenement
from .serializers import *
from authentification.models import CustomUser

stripe.api_key = settings.STRIPE_SECRET_KEY  # Clé secrète Stripe


# Permission personnalisée
class IsOrganisateur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.organisateur


# Liste et création des événements
class EvenementListCreateAPIView(APIView):
    def get(self, request):
        evenements = Evenement.objects.all()
        serializer = EvenementSerializer(evenements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Extraire le token de l'en-tête Authorization
        token = request.headers.get('Authorization')

        if token is None:
            raise AuthenticationFailed("Token non fourni")

        # Supprimer le préfixe "Bearer "
        if token.startswith('Bearer '):
            token = token[7:]

        try:
            # Utiliser TokenAuthentication pour valider le token et obtenir le user associé
            token_obj = Token.objects.get(key=token)
            user = token_obj.user  # Ici, user sera un instance de ton modèle `CustomUser`
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token invalide ou expiré")

        print(f"L'utilisateur correspondant au token est : {user}")
        data = request.data.dict()  # Créer une copie modifiable de request.data

        if 'categories' in data:
            try:
                data['categories'] = json.loads(data['categories'])
                for category in data['categories']:
                    category['billets_restant'] = int(category['billets_restant'])
                    category['prix'] = int(category['prix'])
            except json.JSONDecodeError:
                return Response({"detail": "Erreur lors de la conversion de 'categories'."},
                                status=status.HTTP_400_BAD_REQUEST)

        if 'photo' in request.FILES:
            data['photo'] = request.FILES['photo']

        # Affichage des données traitées
        print("Données ?")
        print(data)

        serializer = EvenementSerializer(data=data)
        if serializer.is_valid():
            try:
                # Créer l'événement et ses catégories
                serializer.save(organisateur=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"detail": "Erreur lors de la création. Vérifiez vos données."},
                                status=status.HTTP_400_BAD_REQUEST)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue personnalisée pour afficher un événement
class EvenementDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            evenement = Evenement.objects.get(pk=pk, organisateur=request.user)
            serializer = EvenementSerializer(evenement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Evenement.DoesNotExist:
            return Response({"detail": "Événement non trouvé."}, status=status.HTTP_404_NOT_FOUND)


# Mise à jour d'un événement
class EvenementUpdateAPIView(APIView):
    permission_classes = [IsOrganisateur]

    def put(self, request, pk):
        try:
            evenement = Evenement.objects.get(pk=pk, organisateur=request.user)
        except Evenement.DoesNotExist:
            return Response({"detail": "Événement introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EvenementSerializer(evenement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Suppression d'un événement
class EvenementDeleteAPIView(APIView):
    # permission_classes = [IsOrganisateur]

    def delete(self, request, pk):
        token = renvoyer_token(request)

        try:
            # Utiliser TokenAuthentication pour valider le token et obtenir le user associé
            token_obj = Token.objects.get(key=token)
            user = token_obj.user  # Ici, user sera un instance de ton modèle `CustomUser`
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token invalide ou expiré")

        try:
            evenement = Evenement.objects.get(pk=pk, organisateur=user)
            evenement.delete()
            return Response({"detail": "Événement supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Evenement.DoesNotExist:
            return Response({"detail": "Événement introuvable."}, status=status.HTTP_404_NOT_FOUND)


# Vue personnalisée pour créer une catégorie d'événement
class CategorieEvenementCreateAPIView(APIView):
    def get(self, request, evenement_id):
        categories = CategorieEvenement.objects.filter(evenement_id=evenement_id)
        serializer = CategorieEvenementSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, evenement_id):
        permission_classes = [IsOrganisateur]

        # Vérifie si l'événement existe et appartient à l'utilisateur
        try:
            evenement = Evenement.objects.get(id=evenement_id, organisateur=request.user)
        except Evenement.DoesNotExist:
            return Response({"detail": "Événement non trouvé ou accès refusé."}, status=status.HTTP_404_NOT_FOUND)

        # Sérialise les données reçues
        serializer = CategorieEvenementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(evenement=evenement)  # Associe la catégorie à l'événement trouvé
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue personnalisée pour afficher une catégorie d'événement
class CategorieEvenementDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            categorie = CategorieEvenement.objects.get(pk=pk, evenement__organisateur=request.user)
            serializer = CategorieEvenementSerializer(categorie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CategorieEvenement.DoesNotExist:
            return Response({"detail": "Catégorie non trouvée."}, status=status.HTTP_404_NOT_FOUND)


# Vue personnalisée pour supprimer une catégorie d'événement
class CategorieEvenementDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            categorie = CategorieEvenement.objects.get(pk=pk, evenement__organisateur=request.user)
            categorie.delete()
            return Response({"detail": "Catégorie supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except CategorieEvenement.DoesNotExist:
            return Response({"detail": "Catégorie non trouvée."}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')  # décorateur pour désactiver temporairement la sécurité csrf protection
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Récupération des données nécessaires
            print('Récupération des données:')
            data = json.loads(request.body)
            print(data)
            evenement_id = int(data.get('evenement_id'))  # request.POST['evenement_id']
            categorie_evenement_nom = data.get('categorie_evenement_nom')  # request.POST['categorie_evenement_nom']
            nombre_places = int(data.get('nombre_places'))  # int(request.POST['nombre_places'])
            token_user = Token.objects.get(key=data.get('token_user'))
            print(f"Token user: {token_user.user.id}")

            evenement = Evenement.objects.get(id=evenement_id)
            categorie = CategorieEvenement.objects.get(evenement=evenement, nom=categorie_evenement_nom)

            # Vérifier s'il reste suffisamment de billets
            if categorie.billets_restant < nombre_places or categorie.billets_restant <= 0:
                return JsonResponse({"error": "Pas assez de billets disponibles."}, status=400)

            # Calculer le prix total
            montant_total = categorie.prix * nombre_places
            print("ici")
            # Création de la session de paiement Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Paiement par carte
                line_items=[
                    {
                        'price_data': {
                            'currency': 'xof',  # Devise
                            'product_data': {
                                'name': categorie.nom,  # Nom de la catégorie
                            },
                            'unit_amount': int(categorie.prix),
                        },
                        'quantity': nombre_places,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/api/evenement/success/',
                cancel_url=settings.SITE_URL + '/api/evenement/cancel/',
                metadata={
                    "evenement_id": evenement_id,
                    "categorie_evenement": categorie_evenement_nom,
                    "nombre_places": nombre_places,
                    "user_id": token_user.user.id,  # Stocker l'ID utilisateur
                    "user": token_user.user
                }
            )
            # print("CS: " + checkout_session.id)
            print(f"CS+: {checkout_session}")
            return JsonResponse({
                'id': checkout_session['id'],  # L'ID de la session
                'url': checkout_session['url'],  # URL pour rediriger l'utilisateur
                'metadata': checkout_session['metadata'],  # Métadonnées utiles
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

        except ValueError as e:
            return JsonResponse({'error': 'Payload invalide'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': 'Signature invalide'}, status=400)

        # Traitement des événements Stripe
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            metadata = session['metadata']

            # Récupérer les informations depuis Stripe
            evenement_id = int(metadata['evenement_id'])
            categorie_evenement = metadata['categorie_evenement']
            nombre_places = int(metadata['nombre_places'])
            user_id = int(metadata['user_id'])

            # Générer les QR codes
            try:
                evenement = Evenement.objects.get(id=evenement_id)
                categorie = CategorieEvenement.objects.get(evenement=evenement, nom=categorie_evenement)
                user = CustomUser.objects.get(id=user_id)

                if categorie.billets_restant >= nombre_places:
                    qr_codes = []
                    for _ in range(nombre_places):
                        # Créer l'objet QRCode sans générer encore l'image
                        qr_code = QRCode(
                            categorie_evenement=categorie,
                            utilisateur=user
                        )

                        # Appeler la méthode save pour générer et enregistrer l'image QR
                        qr_code.save()  # Cela va appeler ta méthode save qui génère le QR code

                        # Ajout du QRCode à la liste
                        qr_codes.append(qr_code)
                        # print(f"QR code ajouté : {qr_code}")
                    QRCode.objects.bulk_create(qr_codes, ignore_conflicts=True)
                    # Réduire les billets restants
                    categorie.billets_restant -= nombre_places
                    categorie.save()

                    # On crée un Historique pour chaque transactions réussie
                    historique = Historique(
                        acheteur=user.email,  # Utiliser l'email ou le nom de l'utilisateur
                        evenement=evenement.nom,  # Nom de l'événement
                        categorie_evenement=categorie.nom,  # Nom de la catégorie
                        prix_billet=categorie.prix,  # Prix unitaire du billet (assurez-vous que ce champ existe)
                        nombre_places_payees=nombre_places,  # Nombre de billets achetés
                    )
                    historique.save()

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({'status': 'success'})


class QRCodeListAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        # Le token est récupéré dans le corps de la requête (POST)
        data = json.loads(request.body)
        token = data.get('token')

        try:
            # Vérifier que le token est valide
            token_user = Token.objects.get(key=token)
            user = token_user.user  # Utilisateur associé au token

            # Filtrer les QR codes associés à cet utilisateur
            qr_codes = QRCode.objects.filter(utilisateur=user)

            # Organiser les QR codes par événement et catégorie
            result = []
            for qr in qr_codes:
                # Remonter l'événement via CategorieEvenement
                categorie_evenement = qr.categorie_evenement
                evenement = categorie_evenement.evenement  # L'événement est lié à la catégorie de l'événement

                # Rechercher l'événement dans la liste des résultats déjà traités
                event_data = next((item for item in result if item["evenement"] == evenement.nom), None)

                if not event_data:
                    # Si l'événement n'est pas encore dans la réponse, on l'ajoute
                    event_data = {
                        "evenement": evenement.nom,
                        "categories": []
                    }
                    result.append(event_data)

                # Ajouter la catégorie à l'événement si elle n'existe pas encore dans les catégories de cet événement
                category_data = next(
                    (cat for cat in event_data["categories"] if cat["categorie"] == categorie_evenement.nom), None)

                if not category_data:
                    category_data = {
                        "categorie": categorie_evenement.nom,
                        "qrcodes": []
                    }
                    event_data["categories"].append(category_data)

                # Ajouter le QR code à la catégorie
                category_data["qrcodes"].append({
                    "id": qr.id,
                    "token": str(qr.token),
                    "valide": qr.valide,
                    "qr_image": qr.qr_image.url,  # Assurez-vous d'avoir le bon URL du QR code
                    "date_creation": qr.date_creation.isoformat()  # Formater la date en ISO
                })

            return JsonResponse({
                "result": result
            })

        except Token.DoesNotExist:
            return Response({"detail": "Token invalide ou utilisateur non trouvé."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def paiement_succes(request):
    return render(request, 'evenement/success.html')


def renvoyer_token(request):
    # Extraire le token de l'en-tête Authorization
    token = request.headers.get('Authorization')

    if token is None:
        raise AuthenticationFailed("Token non fourni")

    # Supprimer le préfixe "Bearer "
    if token.startswith('Bearer '):
        token = token[7:]

    return token


class QRCodeDetailView(APIView):
    def get(self, request, token):
        # Récupérer le token utilisateur depuis l'en-tête
        user_token = request.headers.get('Authorization')
        if not user_token or not user_token.startswith("Bearer "):
            return Response({"detail": "Token utilisateur manquant ou invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        user_token = user_token.split(" ")[1]  # Extraire le vrai token après 'Bearer'

        # Récupérer l'utilisateur associé au token
        try:
            utilisateur = CustomUser.objects.get(auth_token=user_token)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est un organisateur
        if not utilisateur.organisateur:  # Remplacez `is_organisateur` par le champ réel de votre modèle utilisateur
            return Response({"detail": "Accès refusé. Vous devez être un organisateur."},
                            status=status.HTTP_403_FORBIDDEN)

        # Récupérer l'objet QRCode correspondant au token
        qrcode = get_object_or_404(QRCode, token=token)
        serializer = QRCodeDetailSerializer(qrcode)
        return Response(serializer.data)


class QRCodeInvalidate(APIView):
    def get(self, request, token):
        # Récupérer le token utilisateur depuis l'en-tête
        user_token = request.headers.get('Authorization')
        if not user_token or not user_token.startswith("Bearer "):
            return Response({"detail": "Token utilisateur manquant ou invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        user_token = user_token.split(" ")[1]  # Extraire le vrai token après 'Bearer'

        # Récupérer l'utilisateur associé au token
        try:
            utilisateur = CustomUser.objects.get(auth_token=user_token)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est un organisateur
        if not utilisateur.organisateur:  # Remplacez `is_organisateur` par le champ réel de votre modèle utilisateur
            return Response({"detail": "Accès refusé. Vous devez être un organisateur."},
                            status=status.HTTP_403_FORBIDDEN)

        # Récupérer l'objet QRCode correspondant au token
        qrcode = get_object_or_404(QRCode, token=token)

        # Vérifier si le QR Code est déjà invalide
        if not qrcode.valide:
            return Response({"detail": "Le QR Code est déjà invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Modifier l'attribut `valide` et sauvegarder
        qrcode.valide = False
        qrcode.save()

        serializer = QRCodeDetailSerializer(qrcode)
        return Response(serializer.data)
        # return Response({"detail": "Le QR Code a été marqué comme invalide."}, status=status.HTTP_200_OK)


class HistoriqueListView(APIView):
    def get(self, request, *args, **kwargs):
        historiques = Historique.objects.all()
        serializer = HistoriqueSerializer(historiques, many=True)
        return Response(serializer.data)