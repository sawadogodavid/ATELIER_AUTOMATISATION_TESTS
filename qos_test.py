import requests
import time
import statistics

def measure_qos():
    url = "https://api.agify.io/?name=michael"
    num_requests = 15  # Nombre de requêtes pour l'échantillon
    latencies = []
    success_count = 0
    error_count = 0

    print(f"🚀 Début de la mesure de QoS ({num_requests} requêtes en cours)...")

    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5.0)
            end_time = time.time()
            
            latency_ms = (end_time - start_time) * 1000  # Convertir en millisecondes
            
            if response.status_code == 200:
                latencies.append(latency_ms)
                success_count += 1
            else:
                error_count += 1
        except requests.exceptions.RequestException:
            error_count += 1
            
        time.sleep(0.5) # Petite pause entre chaque requête

    # Calcul des métriques si on a des succès
    if latencies:
        avg_latency = statistics.mean(latencies)
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]
    else:
        avg_latency = 0
        p95_latency = 0

    availability = (success_count / num_requests) * 100

    print("\n📊 --- RAPPORT DE QoS ---")
    print(f"✅ Requêtes réussies : {success_count}/{num_requests}")
    print(f"❌ Erreurs : {error_count}/{num_requests}")
    print(f"📈 Disponibilité : {availability:.2f}%")
    print(f"⏱️ Latence moyenne : {avg_latency:.2f} ms")
    print(f"⚡ Latence P95 : {p95_latency:.2f} ms")

if __name__ == "__main__":
    measure_qos()
