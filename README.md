## 🌐 API DOCUMENTATION

## AUTHENTIFICATION (/api/authentification/)

POST /inscription/
{
  "email": "user@email.com",
  "password": "password123",
  "organisateur": true
}

POST /connexion/
{
  "email": "user@email.com",
  "password": "password123"
}

POST /deconnexion/
HEADERS:
Authorization: Bearer <token>

DELETE /suppression/
HEADERS:
Authorization: Bearer <token>

---

## EVENEMENTS (/api/evenement/)

GET /evenements/

POST /evenements/
HEADERS:
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "nom": "Concert",
  "type_evenement": "concert",
  "date_heure": "2026-01-01T20:00:00Z",
  "lieu": "Dakar",
  "description": "Event",
  "categories": [
    {
      "nom": "VIP",
      "billets_restant": 100,
      "prix": 10000
    }
  ]
}

GET /evenements/{id}/afficher/

PUT /evenements/{id}/modifier/
HEADERS:
Authorization: Bearer <token>

DELETE /evenements/{id}/supprimer/
HEADERS:
Authorization: Bearer <token>

---

## CATEGORIES

GET /evenements/categories/{evenement_id}/

POST /evenements/categories/{evenement_id}/
{
  "nom": "VIP",
  "billets_restant": 50,
  "prix": 15000
}

GET /evenements/categories/{id}/

DELETE /evenements/categories/{id}/delete/

---

## PAIEMENT STRIPE

POST /qrcode/creer/
{
  "evenement_id": 1,
  "categorie_evenement_nom": "VIP",
  "nombre_places": 2,
  "token_user": "token"
}

POST /stripe/webhook/

GET /success/

---

## QR CODES

POST /qrcodes/
{
  "token": "user_token"
}

GET /qrcode/{token}/
HEADERS:
Authorization: Bearer <token>

GET /qrcode/invalide/{token}/
HEADERS:
Authorization: Bearer <token>

---

## HISTORIQUE

GET /historique/

---

## SYSTEME

- Authentification par Token (DRF)
- Stripe Checkout pour paiement
- QR Code généré automatiquement après paiement
- 1 QR code = 1 billet
- Middleware suppression événements expirés automatiquement
- Signals suppression images (événements + QR codes)
- Mise à jour stock billets après achat
