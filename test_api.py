import requests
import time

def test_agify_with_robustness():
    url = "https://api.agify.io/?name=michael"
    max_retries = 3
    timeout_limit = 5.0
    
    response = None
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Tentative {attempt} de requête vers l'API...")
            response = requests.get(url, timeout=timeout_limit)
            
            if response.status_code == 429:
                print("⚠️ Trop de requêtes (429). Pause avant réessai...")
                time.sleep(2)
                continue
            elif response.status_code >= 500:
                print(f"⚠️ Erreur serveur ({response.status_code}). Nouvelle tentative...")
                time.sleep(2)
                continue
                
            break
            
        except requests.exceptions.Timeout:
            print(f"⏱️ La requête a dépassé le délai d'attente ({timeout_limit}s).")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            
        if attempt < max_retries:
            time.sleep(1)
            
    if response is None:
        raise Exception("❌ Échec critique : impossible de joindre l'API après plusieurs essais.")
        
    assert response.status_code == 200, f"Attendu 200, reçu {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "La réponse n'est pas un JSON valide"
    assert "name" in data and "age" in data, "Champs manquants dans la réponse"
    
    print("✅ Test de robustesse réussi : l'API a répondu proprement !")

if __name__ == "__main__":
    test_agify_with_robustness()
