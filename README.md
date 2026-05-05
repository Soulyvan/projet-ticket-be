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
