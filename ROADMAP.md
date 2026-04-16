# État du Projet Pulse Lab (SaaS EMS)

## 🎯 Vision
Construire une plateforme SaaS multi-tenant premium pour la gestion des centres EMS, permettant une isolation totale des données et une personnalisation de marque pour chaque studio.

---

## ✅ Réalisations Actuelles

### 1. Architecture Multi-Tenancy
- **Backend** : Isolation automatique des données via `TenantMiddleware` et `TenantManager`. Filtrage dynamique par `X-Tenant-ID`.
- **Frontend** : Interception globale des requêtes pour injecter le contexte de la salle active.
- **Branding Dynamique** : Système d'injection de couleurs primaires/secondaires via variables CSS selon la salle connectée.

### 2. Gestion des Rôles & Sécurité
- **SuperAdmin (Plateforme)** : Accès vertical total, gestion du catalogue des salles, paramétrage global.
- **Admin (Studio)** : Gestionnaire du personnel, des produits et des clients d'un studio spécifique.
- **Personnel** : Accès opérationnel limité au studio assigné.
- **Sécurité** : Protection des routes via des Guards Angular et permissions DRF personnalisées.

### 3. Modules Opérationnels
- **Salles** : CRUD complet pour le SuperAdmin (Logo, Branding, Plan SaaS).
- **Auth** : Système de login avec redirection intelligente par rôle et persistance du contexte.
- **Dashboard** : Structure de base prête à accueillir les KPIs.

---

## 🚀 Prochaines Étapes (Roadmap)

### Phase 1 : Consolidation & BI
- [ ] **Reporting** : Graphiques de performance (ventes, abonnements) filtrés par salle.
- [ ] **Gestion des Fournisseurs** : Module de calcul automatique des commissions et rapports financiers.

### Phase 2 : Expérience Utilisateur
- [ ] **Switcher de Salle** : Menu déroulant élégant dans la Sidebar pour changer de contexte en un clic.
- [ ] **Notifications** : Système d'alertes en temps réel (nouveaux abonnements, stock faible).

### Phase 3 : SaaS & Facturation
- [ ] **Paiement Stripe** : Automatisation des abonnements des studios à la plateforme.
- [ ] **Plans de Fonctionnalités** : Activation/Désactivation de modules (ex: module Ventes) selon le pack choisi.

---

## 🛠️ Stack Technique
- **Backend** : Django 5, DRF, JWT, UUID.
- **Frontend** : Angular (Signals, Components Standalone), Vanilla CSS Premium.
- **Base de données** : PostgreSQL (Production) / SQLite (Local).
- **Isolation** : Header-based multitenancy.
