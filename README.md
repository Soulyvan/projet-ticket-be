<div align="center">
  <h1>🎟️ Ticket Event API</h1>
  <p><strong>API Backend de gestion d'événements et billetterie avec QR Codes</strong></p>
  <p><em>Développée avec Django & Django REST Framework</em></p>
</div>

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Stack technique](#-stack-technique)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Endpoints API](#-endpoints-api)
- [Système de paiement](#-système-de-paiement)
- [QR Codes](#-qr-codes)
- [Système](#-système)

---

## 📖 Présentation

**Ticket Event API** est une API REST complète pour gérer un système de billetterie événementielle.

### Ce que permet l'API :
- ✅ **Organisateurs** : Créer et gérer des événements
- ✅ **Utilisateurs** : Acheter des billets via Stripe
- ✅ **Automatisation** : Génération QR codes uniques
- ✅ **Validation** : Scan et gestion des billets

---

## ⚙️ Fonctionnalités

### 🔐 **Authentification**
- Inscription avec email
- Connexion avec token JWT
- Déconnexion
- Suppression de compte

### 🎫 **Événements**
- Création avec catégories de billets
- Mise à jour / suppression
- Gestion stock billets

### 💳 **Paiement**
- Stripe Checkout intégré
- Webhook validation automatique
- Mise à jour stock post-paiement

### 📱 **QR Codes**
- Génération automatique après paiement
- QR unique par billet
- Validation par scan
- Invalidation

### 📊 **Historique**
- Suivi des achats
- Tracking transactions

---

## 🧱 Stack technique
Technologie

Version

Rôle

Django

5.x

Backend

DRF

3.14

API REST

Token Auth

DRF

Authentification

Stripe

Latest

Paiements

qrcode

Latest

QR Codes

Pillow

Latest

Images

SQLite

Dev

Base de données

🏗️ Architecture
2 applications principales :


Copy code
authentification/
├── CustomUser (rôle organisateur)
└── Token Authentication

evenement/
├── Evenement
├── CategorieEvenement
├── QRCode
├── Paiement Stripe
└── Historique
📦 Installation
bash

Copy code
git clone https://github.com/Soulyvan/projet-ticket-be.git
cd projet-ticket-be

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
URL API : http://localhost:8000

🔐 Authentification
Base URL : /api/authentification/

1. Inscription
bash

Copy code
POST /inscription/
json

Copy code
{
  "email": "user@email.com",
  "password": "password123",
  "organisateur": true
}
2. Connexion
bash

Copy code
POST /connexion/
json

Copy code
{
  "email": "user@email.com",
  "password": "password123"
}
Réponse : {"token": "votre_token"}

3. Headers pour endpoints protégés

Copy code
Authorization: Bearer votre_token
Content-Type: application/json
4. Autres
bash

Copy code
POST /deconnexion/
DELETE /suppression/
🎪 Événements
Base URL : /api/evenement/

Lister événements
bash

Copy code
GET /evenements/
Créer événement
bash

Copy code
POST /evenements/
json

Copy code
{
  "nom": "Concert",
  "type_evenement": "concert",
  "date_heure": "2026-01-01T20:00:00Z",
  "lieu": "Dakar",
  "description": "Event description",
  "categories": [
    {
      "nom": "VIP",
      "billets_restant": 100,
      "prix": 10000
    }
  ]
}
Headers : Authorization: Bearer <token>

Gérer un événement
bash

Copy code
GET    /evenements/{id}/afficher/
PUT    /evenements/{id}/modifier/
DELETE /evenements/{id}/supprimer/
🏷️ Catégories
bash

Copy code
# Pour un événement spécifique
GET  /evenements/categories/{evenement_id}/
POST /evenements/categories/{evenement_id}/

# Gérer une catégorie
GET    /evenements/categories/{id}/
DELETE /evenements/categories/{id}/delete/
Exemple création :

json

Copy code
{
  "nom": "VIP",
  "billets_restant": 50,
  "prix": 15000
}
💳 Système de paiement
1. Créer session paiement
bash

Copy code
POST /qrcode/creer/
json

Copy code
{
  "evenement_id": 1,
  "categorie_evenement_nom": "VIP",
  "nombre_places": 2,
  "token_user": "user_token"
}
Réponse : URL Stripe Checkout

2. Webhook Stripe (automatique)
bash

Copy code
POST /stripe/webhook/
3. Succès
bash

Copy code
GET /success/
📱 QR Codes
Action

Endpoint

Auth

Lister

POST /qrcodes/

✅

Afficher

GET /qrcode/{token}/

✅

Invalider

GET /qrcode/invalide/{token}/

✅

Exemple requête :

json

Copy code
{
  "token": "user_token"
}
1 QR Code = 1 billet unique

📊 Historique
bash

Copy code
GET /historique/
⚙️ Système
Fonctionnalité

Description

Auth

Token Authentication (DRF)

Paiement

Stripe Checkout

QR

Génération auto post-paiement

Stock

Mise à jour après achat

Middleware

Suppression événements expirés

Signals

Nettoyage images auto

<div align="center">
👨‍💻 Développé par Soulyvan
GitHub

</div> ```
