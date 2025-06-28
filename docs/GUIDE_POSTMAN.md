# 🚀 Guide d'Utilisation Postman - API Catégorisation

## 📋 Prérequis

- **Postman** installé sur votre machine
- **API en cours d'exécution** : `docker-compose up -d`
- **Base de données MySQL** (XAMPP) démarrée

## 🔧 Configuration Initiale

### 1. Importer la Collection

1. **Ouvrir Postman**
2. **Cliquer sur "Import"** (bouton en haut à gauche)
3. **Sélectionner le fichier** : `docs/postman_collection.json`
4. **Cliquer sur "Import"**

### 2. Configurer l'Environnement

1. **Créer un nouvel environnement** :
   - Cliquer sur l'icône ⚙️ (engrenage) en haut à droite
   - Cliquer sur "Add"
   - Nom : `API Catégorisation - Local`

2. **Ajouter les variables** :
   - `base_url` : `http://localhost:8000/api`
   - `token` : (laissé vide, sera rempli automatiquement)

3. **Sélectionner l'environnement** dans le menu déroulant

## 🔑 Authentification

### 1. Se Connecter

1. **Ouvrir la requête** : `🔑 Authentification > Login`
2. **Vérifier les données** :
   ```json
   {
       "phoneNumber": "99595766",
       "password": "test123"
   }
   ```
3. **Cliquer sur "Send"**

### 2. Vérifier la Connexion

**Réponse attendue (200 OK) :**
```json
{
    "message": "Connexion réussie",
    "user": {
        "user_id": "uuid-utilisateur",
        "phoneNumber": "+22899595766",
        "role": "admin"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

**✅ Le token est automatiquement sauvegardé dans l'environnement !**

## 📝 Enregistrer des Messages

### 1. Test avec Exemples Complets

1. **Ouvrir** : `📝 Enregistrement de Messages > Enregistrer Messages - Exemples Complets`
2. **Vérifier le contenu** : 7 exemples de messages réalistes
3. **Cliquer sur "Send"**

**Réponse attendue (201 Created) :**
```json
{
    "status": "success",
    "created": 7,
    "duplicates": 0,
    "total_received": 7,
    "processing_triggered": true
}
```

### 2. Test avec Message Simple

1. **Ouvrir** : `📝 Enregistrement de Messages > Enregistrer Message Simple`
2. **Modifier le message** si nécessaire
3. **Cliquer sur "Send"**

## 📊 Consulter les Messages Traités

### 1. Page 1 (Par Défaut)

1. **Ouvrir** : `📊 Consultation des Messages Traités > Page 1 - Messages Traités`
2. **Cliquer sur "Send"`

**Réponse attendue (200 OK) :**
```json
{
    "total": 150,
    "page": 1,
    "page_size": 20,
    "results": [
        {
            "id": "fd0b0d9f-0857-4f9e-ba1b-9c51eea02970",
            "category": "RETRAIT",
            "type": "togocom",
            "title": "Retrait Togocom",
            "amount": 60000.0,
            "amount_total": 60900.0,
            "fee": 900.0
        }
    ]
}
```

### 2. Navigation entre Pages

**Page 2 avec 10 éléments :**
1. **Ouvrir** : `📊 Consultation des Messages Traités > Page 2 - 10 éléments`
2. **Cliquer sur "Send"`

### 3. Filtrage

**Filtrer par catégorie :**
1. **Ouvrir** : `📊 Consultation des Messages Traités > Filtrer par Catégorie - RETRAIT`
2. **Cliquer sur "Send"`

**Filtrer par type :**
1. **Ouvrir** : `📊 Consultation des Messages Traités > Filtrer par Type - togocom`
2. **Cliquer sur "Send"`

**Filtrer par utilisateur :**
1. **Ouvrir** : `📊 Consultation des Messages Traités > Filtrer par Utilisateur`
2. **Cliquer sur "Send"`

## ⚡ Traitement Manuel

### Lancer le Traitement

1. **Ouvrir** : `⚡ Traitement Manuel > Lancer Traitement Manuel`
2. **Cliquer sur "Send"`

**Réponse attendue (202 Accepted) :**
```json
{
    "message": "Traitement lancé en arrière-plan."
}
```

## 👤 Profil Utilisateur

### Récupérer le Profil

1. **Ouvrir** : `👤 Profil Utilisateur > Récupérer Profil`
2. **Cliquer sur "Send"`

**Réponse attendue (200 OK) :**
```json
{
    "user_id": "uuid-utilisateur",
    "nom": "Nom",
    "prenom": "Prénom",
    "phoneNumber": "+22899595766",
    "role": "admin"
}
```

## 🔍 Tests Automatisés

### Vérifier les Tests

Chaque requête contient des **tests automatisés** qui s'exécutent après l'envoi :

1. **Ouvrir l'onglet "Test Results"** (en bas de Postman)
2. **Vérifier que tous les tests passent** ✅

**Exemples de tests :**
- ✅ Status code is 200
- ✅ Response has tokens
- ✅ Processing was triggered
- ✅ Response has pagination info

## 🎯 Exemples de Messages Testés

### 💰 Retraits Togocom
```json
{
    "user_id": "d9e0f1a2-b3c4-43d5-e6f7-a8b9c0d1e2f3",
    "message": "Vous avez retire 60 000 FCFA auprès de l'agent LR ETS FIAT LUX-SERVICE (32765), le 15-11-24 14:54. Frais: 900 FCFA. Nouveau solde: 232 139 FCFA . Ref: 7213354475."
}
```

### 🏧 Retraits Flooz (Moov)
```json
{
    "user_id": "a6b7c8d9-e0f1-46a2-b3c4-d5e6f7a8b9c0",
    "message": "Retrait validé\r\nMontant: 100,000 FCFA \r\nFrais HT: 909 FCFA, TAF: 91 FCFA \r\nNom PDV: LINARCEL_ETS_MBC\r\nDate: 17-Mar-2025 12:52:20\r\nNouveau solde Flooz: 61,271 FCFA\r\nVeuillez retirer l'argent chez le Pdv. \r\nTrx id: 1250317169479"
}
```

### 📱 Transferts Mixx By Yas
```json
{
    "user_id": "e8f9a0b1-c2d3-47e4-f5a6-b7c8d9e0f1a2",
    "message": "TMoney devient Mixx By Yas. Vous avez envoyé 10 300 FCFA au 92939241, le 26-02-25 08:17. Frais: 30 FCFA. Nouveau solde: 45 670 FCFA. Ref: 1234567890."
}
```

### ⚡ Factures
```json
{
    "user_id": "4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a",
    "message": "Vous avez payé 14 574 FCFA a CEET (reference: 01001, string), le 24-05-24 06:14. Frais: 0 FCFA. Nouveau solde: 12 345 FCFA. Ref: 9876543210."
}
```

## 🚀 Workflow Complet

### 1. Authentification
```bash
POST /auth/login/
→ Récupérer le token JWT
```

### 2. Enregistrement
```bash
POST /messages/enregister/
→ Envoyer les messages à traiter
→ Traitement automatique déclenché
```

### 3. Consultation
```bash
GET /processed-messages/
→ Consulter les résultats traités
→ Navigation par pages
→ Filtrage par catégorie/type
```

## 🔧 Personnalisation

### Modifier les Variables

1. **Ouvrir l'environnement** (icône ⚙️)
2. **Modifier les valeurs** :
   - `base_url` : URL de votre API
   - `token` : Token JWT (rempli automatiquement)

### Ajouter de Nouveaux Messages

1. **Dupliquer** une requête d'enregistrement
2. **Modifier le body** avec vos messages
3. **Sauvegarder** la nouvelle requête

### Créer de Nouveaux Filtres

1. **Dupliquer** une requête de consultation
2. **Modifier les paramètres** dans l'URL
3. **Sauvegarder** la nouvelle requête

## 🛠️ Dépannage

### Token Expiré (401 Unauthorized)
1. **Se reconnecter** avec la requête Login
2. **Le token sera automatiquement mis à jour**

### API Non Accessible
1. **Vérifier** que Docker est démarré : `docker-compose ps`
2. **Vérifier** que XAMPP MySQL est démarré
3. **Redémarrer** si nécessaire : `docker-compose restart`

### Messages Non Traités
1. **Vérifier les logs** : `docker-compose logs api`
2. **Lancer le traitement manuel** si nécessaire
3. **Vérifier** que le worker Celery fonctionne

## 📊 Validation des Résultats

### Vérifier les Catégories
Les messages doivent être catégorisés comme :
- **RETRAIT** : Retraits d'espèces
- **TRANSFERT_ENVOYE** : Envois d'argent
- **FACTURE** : Paiements de factures
- **CREDIT** : Achats de crédit

### Vérifier les Montants
- **Extraction correcte** des montants en FCFA
- **Calcul des frais** (HT + TAF)
- **Montant total** = montant + frais

### Vérifier les Types
- **togocom** : Togocom/Mixx By Yas
- **moov** : Moov/Flooz
- **inconnu** : Opérateur non identifié

## 🎉 Félicitations !

Vous maîtrisez maintenant l'utilisation de l'API de catégorisation avec Postman ! 

**Prochaines étapes :**
- Tester avec vos propres messages
- Intégrer l'API dans votre application
- Personnaliser les filtres selon vos besoins

---

**📞 Support :** Consultez la documentation complète dans `/docs/API.md` 