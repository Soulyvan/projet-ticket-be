# 🎟️ Ticket Event API

API backend de gestion d’événements et de billetterie avec génération de QR Codes, développée avec Django et Django REST Framework.

Cette API permet :
- aux organisateurs de créer des événements
- aux utilisateurs d’acheter des billets via Stripe
- de générer automatiquement des QR codes uniques
- de gérer la validation des billets

---

## 📌 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Stack technique](#-stack-technique)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Authentification](#-authentification)
- [Endpoints API](#-endpoints-api)
- [Système de paiement](#-système-de-paiement)
- [QR Codes](#-qr-codes)
- [Middleware](#-middleware)
- [Structure du projet](#-structure-du-projet)
- [Améliorations possibles](#-améliorations-possibles)

---

## 📖 Présentation

Ce projet est une API REST complète permettant de gérer un système de billetterie pour événements.

Elle implémente :
- gestion des utilisateurs (organisateur / client)
- gestion des événements et catégories de billets
- paiement en ligne avec Stripe
- génération de QR codes uniques pour chaque billet
- validation des billets

---

## ⚙️ Fonctionnalités

### 🔐 Authentification
- Inscription avec email
- Connexion avec token
- Déconnexion
- Suppression de compte

### 🎫 Événements
- Création d’événements avec catégories
- Mise à jour / suppression
- Gestion des billets disponibles

### 💳 Paiement
- Intégration Stripe Checkout
- Webhook pour validation automatique
- Gestion du stock après paiement

### 📱 QR Codes
- Génération automatique après paiement
- QR unique par billet
- Validation (scan)
- Invalidation

### 📊 Historique
- Historique des achats
- Tracking des transactions

---

## 🧱 Stack technique

- Backend : Django 5
- API : Django REST Framework
- Auth : Token Authentication (DRF)
- Paiement : Stripe
- QR Code : qrcode
- Images : Pillow
- CORS : django-cors-headers
- Base de données : SQLite (dev)

---

## 🏗️ Architecture

Le projet est structuré en 2 apps principales :

### 1. authentification
Gestion des utilisateurs :
- CustomUser (avec rôle organisateur)
- Authentification par token

### 2. evenement
Cœur métier :
- événements
- catégories de billets
- QR codes
- paiement Stripe
- historique

---

## 📦 Installation

```bash
git clone https://github.com/Soulyvan/projet-ticket-be.git
cd projet-ticket-be
```


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
