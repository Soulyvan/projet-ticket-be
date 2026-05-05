<div align="center">
  <img src="https://user-images.githubusercontent.com/123456/200000000.png" alt="Ticket Event API" width="800"/>
  <h1>🎟️ Ticket Event API</h1>
  <p><strong>API Backend de gestion d'événements et billetterie avec QR Codes</strong></p>
  <p><em>Développée avec Django & Django REST Framework</em></p>
  
  <img alt="Django" src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img alt="DRF" src="https://img.shields.io/badge/DRF-3.14-00D775?style=for-the-badge&logo=django-rest-framework&logoColor=white">
  <img alt="Stripe" src="https://img.shields.io/badge/Stripe-%2363B8EE?style=for-the-badge&logo=stripe&logoColor=white">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" style="height: 23px;">
</div>

<br>

## ✨ **Fonctionnalités**
🔐 **Authentification

🎫 **Événements

💳 **Paiement

📱 **QR Codes

Inscription email

Création événements

Stripe Checkout

Génération auto

Connexion token

Catégories billets

Webhook sécurisé

Validation scan

Rôles organisateur

Gestion stock

Stock auto

1 QR = 1 billet

🛠️ Stack Technique
mermaid

Copy code
graph TD
    A[Django 5.x] --> B[DRF API]
    B --> C[Token Auth]
    C --> D[Stripe Paiement]
    D --> E[QR Codes]
    E --> F[SQLite/PostgreSQL]
🚀 Démarrage rapide (2 min ⏱️)
bash

Copy code
git clone https://github.com/Soulyvan/projet-ticket-be.git
cd projet-ticket-be
pip install -r requirements.txt
cp .env.example .env
# Ajouter tes clés Stripe
python manage.py migrate
python manage.py runserver
API prête : http://localhost:8000

🔐 Authentification
bash

Copy code
# 1. Inscription
curl -X POST http://localhost:8000/api/authentification/inscription/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@email.com","password":"123456","organisateur":true}'

# 2. Connexion
curl -X POST http://localhost:8000/api/authentification/connexion/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@email.com","password":"123456"}'
Token reçu → Authorization: Bearer ton_token

🎪 Endpoints Principaux
Méthode

Endpoint

Description

Auth

GET

/api/evenement/evenements/

Lister événements

❌

POST

/api/evenement/evenements/

Créer événement

✅

POST

/api/qrcode/creer/

Paiement Stripe

✅

GET

/api/qrcode/{token}/

Afficher QR

✅

POST

/api/qrcode/valider/{token}/

Valider billet

✅

💳 Exemple : Acheter un billet
json

Copy code
POST /api/qrcode/creer/
{
  "evenement_id": 1,
  "categorie_evenement_nom": "VIP",
  "nombre_places": 2,
  "token_user": "user_token"
}
→ Redirection Stripe Checkout → QR généré automatiquement !

🛡️ Sécurité incluse
✅ Token Authentication DRF
✅ CORS configuré
✅ Rate Limiting
✅ Signals suppression images
✅ Middleware auto-cleanup
✅ Stock temps réel

📊 Base de données
sql

Copy code
-- Modèles principaux
CustomUser (email, role_organisateur)
Evenement (nom, date, lieu, image)
CategorieEvenement (nom, prix, billets_restant)
QRCode (token_unique, valide, user)
Transaction (stripe_id, montant, statut)
🔧 Configuration .env
env

Copy code
SECRET_KEY=your-secret-key-here
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
ALLOWED_HOSTS=localhost,127.0.0.1
🚀 Déploiement Production
bash

Copy code
# 1. PostgreSQL + Gunicorn
pip install gunicorn psycopg2-binary

# 2. Render/Heroku/Vercel
gunicorn projet_ticket_be.wsgi

# 3. Docker (bientôt)
docker-compose up -d
📈 Roadmap
v2.0

v2.1

v3.0

Google Auth

SMS/Email

Dashboard

Multi-devises

Analytics

Mobile App

Docker

PDF Tickets

Webhooks

<div align="center">
🤝 Contribuer
bash

Copy code
git clone https://github.com/Soulyvan/projet-ticket-be.git
# Crée ta feature branch
# Commit & PR
⭐ Star si utile !

Footer

👨‍💻 par Soulyvan | 📧 soulyvan@email.com

</div> ```
