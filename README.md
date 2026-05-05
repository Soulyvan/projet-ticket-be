<div align="center">

# 🎟️ **Ticket Event API**

**API Backend de gestion d'événements et billetterie avec QR Codes**  
*Développée avec Django & Django REST Framework*

[![Django](https://img.shields.io/badge/Django-5.0-blue.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-green.svg)](https://www.django-rest-framework.org/)
[![Stripe](https://img.shields.io/badge/Stripe-Payments-purple.svg)](https://stripe.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 **Présentation**

Une **API RESTful complète** pour la gestion de billetterie événementielle, permettant aux **organisateurs** de créer des événements et aux **utilisateurs** d'acheter des billets sécurisés.

### **Fonctionnalités principales**
- 🔐 **Authentification** JWT sécurisée
- 🎫 **Gestion complète** des événements & catégories de billets
- 💳 **Paiement sécurisé** via Stripe Checkout
- 📱 **QR Codes uniques** générés automatiquement
- ✅ **Validation** & invalidation des billets
- 📊 **Historique** des transactions

---

## 🛠️ **Stack Technique**
Catégorie

Technologie

Backend

Django 5.x

API

Django REST Framework

Authentification

Token Authentication (DRF)

Paiement

Stripe

QR Codes

qrcode + Pillow

Base de données

SQLite (dev) / PostgreSQL

CORS

django-cors-headers

🏗️ Architecture

Copy code
projet-ticket-be/
├── authentification/     # Gestion utilisateurs & auth
├── evenement/           # Cœur métier (événements, billets, QR)
├── qrcode/              # Génération & validation QR
└── core/                # Middleware & utils
2 apps principales :

authentification : CustomUser, rôles organisateur
evenement : Événements, catégories, paiements, QR codes
📦 Installation rapide
bash

Copy code
# Cloner le projet
git clone https://github.com/Soulyvan/projet-ticket-be.git
cd projet-ticket-be

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés STRIPE

# Migrations & superuser
python manage.py migrate
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
URL de base : http://localhost:8000

🔐 Authentification
1. Inscription
bash

Copy code
POST /api/authentification/inscription/
json

Copy code
{
  "email": "organisateur@email.com",
  "password": "MotDePasse123!",
  "organisateur": true
}
2. Connexion
bash

Copy code
POST /api/authentification/connexion/
json

Copy code
{
  "email": "user@email.com",
  "password": "MotDePasse123!"
}
Réponse : { "token": "votre_token_jwt" }

Headers pour les requêtes protégées :

Copy code
Authorization: Bearer votre_token_jwt
🎪 Gestion des Événements
📋 Lister tous les événements
bash

Copy code
GET /api/evenement/evenements/
➕ Créer un événement
bash

Copy code
POST /api/evenement/evenements/
json

Copy code
{
  "nom": "Concert Sadio Mané",
  "type_evenement": "concert",
  "date_heure": "2026-01-15T20:00:00Z",
  "lieu": "Arena Dakar",
  "description": "Concert exclusif...",
  "image": "upload/image.jpg",
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
}
✏️ Modifier / Supprimer
bash

Copy code
PUT /api/evenement/evenements/{id}/modifier/
DELETE /api/evenement/evenements/{id}/supprimer/
💳 Système de Paiement (Stripe)
1. Créer une session de paiement
bash

Copy code
POST /api/qrcode/creer/
json

Copy code
{
  "evenement_id": 1,
  "categorie_evenement_nom": "VIP",
  "nombre_places": 2,
  "token_user": "user_jwt_token"
}
Réponse : URL Stripe Checkout

2. Webhook Stripe (automatique)
bash

Copy code
POST /api/stripe/webhook/
Validation automatique du paiement & génération QR codes

3. Page de succès
bash

Copy code
GET /api/success/
📱 QR Codes
Action

Endpoint

Auth

Générer QR

POST /api/qrcodes/

✅

Afficher QR

GET /api/qrcode/{token}/

✅

Valider QR

POST /api/qrcode/valider/{token}/

✅

Invalider QR

GET /api/qrcode/invalide/{token}/

✅

1 QR Code = 1 billet unique

📊 Historique & Stats
bash

Copy code
GET /api/historique/  # Tous les achats utilisateur
GET /api/admin/stats/ # Dashboard admin (organisateurs)
🔧 Configuration avancée
.env requis
env

Copy code
SECRET_KEY=votre_secret_key
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
DATABASE_URL=sqlite:///db.sqlite3
Scripts utiles
bash

Copy code
# Nettoyage auto événements expirés
python manage.py clean_expired_events

# Génération QR en masse (admin)
python manage.py generate_pending_qrcodes
🛡️ Sécurité & Middleware
✅ Token Authentication DRF
✅ CORS configuré
✅ Rate Limiting intégré
✅ Signals suppression images auto
✅ Middleware nettoyage événements expirés
✅ Validation stock billets temps réel
🚀 Déploiement
bash

Copy code
# Production (exemple Render/Heroku)
pip install gunicorn psycopg2-binary
gunicorn projet_ticket_be.wsgi:application

# Docker (coming soon)
docker-compose up -d
📈 Améliorations prévues
Feature

Statut

Priorité

Auth Google/OAuth2

🔄 En cours

⭐⭐⭐

Notifications SMS/Email

⏳ Planifié

⭐⭐⭐

Analytics Dashboard

⏳ Planifié

⭐⭐

Multi-devises

⏳ Planifié

⭐⭐

Docker & CI/CD

⏳ Planifié

⭐⭐⭐

<div align="center">
🤝 Contribuer
Fork le projet
Créer une feature branch (git checkout -b feature/nouvelle-fonction)
Commit vos changements (git commit -m 'Ajout: nouvelle feature')
Push vers la branch (git push origin feature/nouvelle-fonction)
Ouvrir une Pull Request
</div>
<div align="center">
👨‍💻 Développé avec ❤️ par Soulyvan
