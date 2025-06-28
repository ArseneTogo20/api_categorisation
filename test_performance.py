import requests
import uuid
import time
import random

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{API_BASE_URL}/auth/login/"
TRANSACTIONS_URL = f"{API_BASE_URL}/transactions/"

# Remplacez par les identifiants de votre super-utilisateur créé via createsuperuser
ADMIN_USERNAME = "98454209"  # Votre numéro de téléphone
ADMIN_PASSWORD = "le_mot_de_passe_que_vous_avez_défini"

# --- Paramètres du Test ---
NUM_TRANSACTIONS = 10000
DUPLICATE_RATIO = 0.3  # 30% des transactions seront des doublons

def get_auth_token():
    """Se connecte à l'API et retourne un token d'authentification."""
    print("1. Connexion pour obtenir le token d'authentification...")
    payload = {
        "phoneNumber": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        token = response.json().get("tokens", {}).get("access")
        if not token:
            print("Erreur: Token non trouvé dans la réponse de login.")
            print(response.json())
            return None
        print("   Connexion réussie.")
        return token
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion: {e}")
        if e.response:
            print(f"Réponse du serveur: {e.response.text}")
        return None

def generate_transactions(num, duplicate_ratio):
    """Génère une liste de transactions avec des doublons."""
    print(f"2. Génération de {num} transactions avec ~{int(duplicate_ratio*100)}% de doublons...")
    
    transactions = []
    num_duplicates = int(num * duplicate_ratio)
    num_uniques = num - num_duplicates

    # Générer les transactions uniques
    for _ in range(num_uniques):
        transactions.append({
            "user_id": str(uuid.uuid4()),
            "message": f"Transaction unique N°{random.randint(1, 1000000)}"
        })
    
    # Générer les doublons en se basant sur les uniques
    duplicates_source = random.choices(transactions, k=num_duplicates)
    transactions.extend(duplicates_source)
    
    random.shuffle(transactions) # Mélanger le tout
    print(f"   {len(transactions)} transactions générées.")
    return transactions

def run_test(token, transactions):
    """Envoie les transactions à l'API et mesure la performance."""
    print("3. Envoi des transactions à l'API...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "transactions": transactions
    }
    
    start_time = time.time()
    try:
        response = requests.post(TRANSACTIONS_URL, headers=headers, json=payload)
        end_time = time.time()
        
        duration = end_time - start_time
        print("\n--- RÉSULTATS DU TEST ---")
        print(f"Temps de réponse de l'API: {duration:.4f} secondes")
        
        if response.status_code == 201:
            print("Statut de la réponse: 201 CREATED (Succès)")
            print("Statistiques retournées par l'API:")
            print(response.json())
        else:
            print(f"Erreur: L'API a retourné un statut {response.status_code}")
            print("Réponse de l'API:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête: {e}")

if __name__ == "__main__":
    print("--- Début du Script de Test de Performance ---")
    
    # Étape 1: Obtenir le token
    auth_token = get_auth_token()
    
    if auth_token:
        # Étape 2: Générer les données de test
        transactions_list = generate_transactions(NUM_TRANSACTIONS, DUPLICATE_RATIO)
        
        # Étape 3: Lancer le test
        run_test(auth_token, transactions_list)
        
    print("\n--- Fin du Script ---") 