# Plan d'Architecture Multi-Tenant & Fournisseurs (Tâches Restantes)

Ce document répertorie les étapes restantes pour finaliser la transition vers l'architecture multi-tenant.

---

## 1. Définition Stricte des Contextes d'Accès (API & Vues)
Le cœur de la sécurité du système reposera désormais sur la distinction de 3 profils lorsqu'un utilisateur interroge l'API :

*   **Profil « Personnel »** : L'utilisateur n'est lié qu'à une seule salle (via `user.salle`).
    *   **Lecture (GET)** : Les vues DRF doivent filtrer `queryset.filter(salle=request.user.salle)`.
    *   **Écriture (POST)** : Ajout imposé de l'ID de la salle de l'utilisateur.

*   **Profil « Fournisseur »** : L'utilisateur gère potentiellement plusieurs salles (via `user.fournisseur.salles`).
    *   **Nécessité d'un Contexte Actif** : Le fournisseur doit travailler sur une salle à la fois. Le Front-End devra envoyer l'identifiant de la salle sélectionnée via un Header HTTP `X-Tenant-ID`.
    *   **Vérification de sécurité** : Dans les vues, le backend doit extraire le `X-Tenant-ID`, vérifier que ce Fournisseur est bien actif sur cette salle dans `SalleFournisseur`, puis filtrer `queryset.filter(salle_id=tenant_id)`.

*   **Profil « SuperAdmin » (Fondation EMS)** : Accès sans restriction (`.all()`) aux fins de maintenance et d'audit.

## 2. Adaptation de l'Authentification (AuthService)
- **Jwt Payload Enrichi** : Lors du login, si l'utilisateur possède une relation `Fournisseur`, le point d'entrée d'authentification doit remonter la liste de toutes ses salles autorisées (IDs, Noms, Logos).
- **Initialisation Frontend** : Cela permettra à l'application Angular de pré-loader le "Sélecteur de Salle" de l'utilisateur qui vient de se connecter.

## 3. Isolation de l'Administration Django
Surcharger le `get_queryset()` des différents `ModelAdmin` :
- **SuperAdmin** voit tout.
- **Personnel** voit uniquement les ressources de sa `user.salle`.
- **Fournisseur** verra une vue aggrégée des données pour `salle__in=mes_salles_fournisseurs_ids`.

## 4. Nouveau Module Financier : Gestion des Commissions
Avec l'ajout de `taux_commission`, il sera nécessaire d'implémenter :
- **Un End-Point de Reporting Fournisseur** permettant à un Fournisseur de consulter ses revenus par salle (montant des abonnements x `taux_commission`).
- Des filtres de dates et de statut pour calculer les paiements.

## 5. Frontend Angular : Le "Tenant Switcher"
- **Barre de navigation principale** : Intégrer un menu déroulant pour changer de contexte ("Passer à Salle Casablanca", "Passer à Salle Rabat").
- **Interceptor HTTP** : Implémenter un interceptor qui, à chaque requête vers Django, attrape l'ID de la salle sélectionnée dans le Store de l'application et l'incruste dans le header `X-Tenant-ID`.
- **Marque Blanche Dynamique** : À chaque changement de salle dans le "Tenant Switcher", ré-appliquer le logo et les couleurs (`couleur_primaire`) de la nouvelle salle ciblée.

