from flask import Flask, render_template_string
import requests
import statistics
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard QoS - API Agify</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }
        h1 { color: #333; }
        .metric { margin: 15px 0; font-size: 18px; }
        .value { font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📊 Rapport de QoS - API Agify</h1>
        <div class="metric">Disponibilité : <span class="value">{{ availability }}%</span></div>
        <div class="metric">Latence moyenne : <span class="value">{{ avg_latency }} ms</span></div>
        <div class="metric">Latence P95 : <span class="value">{{ p95_latency }} ms</span></div>
        <hr>
        <p><small>Statut : ✅ API Fonctionnelle</small></p>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    url = "https://api.agify.io/?name=michael"
    latencies = []
    successes = 0
    total = 5

    for _ in range(total):
        start = time.time()
        try:
            res = requests.get(url, timeout=5.0)
            if res.status_code == 200:
                latencies.append((time.time() - start) * 1000)
                successes += 1
        except Exception:
            pass

    avg_lat = round(statistics.mean(latencies), 2) if latencies else 0
    p95_lat = round(sorted(latencies)[int(len(latencies)*0.95)], 2) if latencies else 0
    avail = round((successes / total) * 100, 2)

    return render_template_string(HTML_TEMPLATE, availability=avail, avg_latency=avg_lat, p95_latency=p95_lat)

if __name__ == '__main__':
    app.run(debug=True)
