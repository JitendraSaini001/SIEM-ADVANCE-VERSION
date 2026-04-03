from flask import Flask, render_template, jsonify
from storage.storage import (get_recent_alerts, 
                              get_event_count_by_ip, 
                              get_alert_stats)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/alerts")
def api_alerts():
    alerts = get_recent_alerts(50)
    return jsonify(alerts)

@app.route("/api/stats")
def api_stats():
    ip_counts   = get_event_count_by_ip()
    alert_stats = get_alert_stats()
    return jsonify({
        "top_ips":     ip_counts,
        "alert_stats": alert_stats
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)