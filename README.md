<div align="center">
  <img width="100" src="https://raw.githubusercontent.com/Soulyvan/projet-ticket-be/main/media/logo.png" alt="Logo">
  <h1>🎟️ Ticket Event API</h1>
  <p>
    <strong>API Backend complète de billetterie événementielle</strong><br>
    <em>Django + DRF + Stripe + QR Codes</em>
  </p>
  <br>
  <img src="https://img.shields.io/badge/Django-5.0-blue?style=flat&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.14-green?style=flat&logo=django-rest&logoColor=white" alt="DRF">
  <img src="https://img.shields.io/badge/Stripe-635BFF?style=flat&logo=stripe&logoColor=white" alt="Stripe">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat&logo=mit" alt="License">
</div>

---

## 📖 Aperçu rapide

**Ticket Event API** est une solution complète de billetterie pour :
- **Organisateurs** : Créer/gérer événements
- **Utilisateurs** : Acheter billets (Stripe)
- **Validation** : QR Codes uniques + scan

**[Démo live](http://localhost:8000) → [Documentation Swagger](http://localhost:8000/api/schema/swagger-ui/)**

---

## 🚀 Démarrage en 60s

```bash
# Clone & setup
git clone https://github.com/Soulyvan/projet-ticket-be.git
cd projet-ticket-be

# Environnement
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
✅ API prête : http://localhost:8000

🧪 Test rapide
bash

Copy code
# 1. S'inscrire (organisateur)
curl -X POST http://localhost:8000/api/authentification/inscription/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@organisateur.com",
    "password": "motdepasse123",
    "organisateur": true
  }'

# 2. Se connecter
curl -X POST http://localhost:8000/api/authentification/connexion/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@organisateur.com", 
    "password": "motdepasse123"
  }'
Sauvegardez le TOKEN reçu ! 👇

🔐 Authentification
Endpoint

Méthode

Auth

Description

/api/authentification/inscription/

POST

❌

Créer compte

/api/authentification/connexion/

POST

❌

Obtenir token

/api/authentification/deconnexion/

POST

✅

Logout

/api/authentification/suppression/

DELETE

✅

Supprimer compte

Headers obligatoires (endpoints protégés) :

bash

Copy code
Authorization: Bearer VOTRE_TOKEN
Content-Type: application/json
Exemple inscription :

json

Copy code
{
  "email": "user@example.com",
  "password": "MonMotDePasse123!",
  "organisateur": true
}
🎪 Événements
Endpoint

Méthode

Auth

Description

/api/evenement/evenements/

GET

❌

Lister tous

/api/evenement/evenements/

POST

✅

Créer

/api/evenement/evenements/{id}/afficher/

GET

❌

Détails

/api/evenement/evenements/{id}/modifier/

PUT

✅

Modifier

/api/evenement/evenements/{id}/supprimer/

DELETE

✅

Supprimer

Créer un événement :

bash

Copy code
curl -X POST http://localhost:8000/api/evenement/evenements/ \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Concert Live",
    "type_evenement": "concert",
    "date_heure": "2026-01-15T20:00:00Z",
    "lieu": "Arena Dakar",
    "description": "Concert exceptionnel",
    "categories": [
      {
        "nom": "VIP",
        "billets_restant": 50,
        "prix": 25000
      },
      {
        "nom": "Standard",
        "billets_restant": 200,
        "prix": 15000
      }
    ]
  }'
🏷️ Catégories de billets
Endpoint

Méthode

Auth

Description

/api/evenement/evenements/categories/{evenement_id}/

GET/POST

✅

Lister/Créer

/api/evenement/categories/{id}/

GET

❌

Détails

/api/evenement/categories/{id}/delete/

DELETE

✅

Supprimer

Ajouter catégorie :

json

Copy code
{
  "nom": "Première Rangée",
  "billets_restant": 20,
  "prix": 35000
}
💳 Paiement Stripe
1. Lancer checkout (utilisateur)
bash

Copy code
curl -X POST http://localhost:8000/api/qrcode/creer/ \
  -H "Content-Type: application/json" \
  -d '{
    "evenement_id": 1,
    "categorie_evenement_nom": "VIP",
    "nombre_places": 2,
    "token_user": "USER_TOKEN"
  }'
Réponse : { "url": "https://checkout.stripe.com/..." }

2. Webhook (automatique)

Copy code
POST /api/stripe/webhook/
Génère QR codes après paiement réussi

3. Succès

Copy code
GET /success/
📱 QR Codes
Endpoint

Méthode

Auth

Description

/api/qrcodes/

POST

✅

Lister mes QR

/api/qrcode/{token}/

GET

✅

Afficher QR

/api/qrcode/invalide/{token}/

GET

✅

Invalider

Lister QR :

json

Copy code
{
  "token": "USER_TOKEN"
}
✅ 1 QR Code = 1 billet unique

📊 Historique
bash

Copy code
curl -H "Authorization: Bearer VOTRE_TOKEN" \
  http://localhost:8000/api/historique/
🛠️ Configuration
.env (obligatoire)
env

Copy code
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
Scripts utiles
bash

Copy code
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
🔒 Sécurité & Features
Fonctionnalité

Statut

Token DRF

✅

CORS

✅

Rate Limiting

✅

Stock temps réel

✅

Middleware cleanup ✅

Signals images ✅

📈 Roadmap
[ ] Google OAuth
[ ] Notifications Email/SMS
[ ] Dashboard Analytics
[ ] Docker
[ ] Tests E2E
<div align="center">
🤝 Contribuer
bash

Copy code
git clone https://github.com/Soulyvan/projet-ticket-be.git
# → Créez une PR !
⭐ Star si utile !

GitHub
Twitter

© 2024 Soulyvan - MIT License

</div> ```
