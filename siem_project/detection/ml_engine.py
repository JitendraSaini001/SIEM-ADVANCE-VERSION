import numpy as np
from sklearn.ensemble import IsolationForest
from collections import defaultdict
from datetime import datetime

# Per-IP request rate tracker
ip_request_counts = defaultdict(list)

class AnomalyDetector:
    def __init__(self):
        # Isolation Forest: contamination = expected anomaly fraction
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,   # 5% of traffic expected to be anomalous
            random_state=42
        )
        self.training_data = []
        self.is_trained = False
        self.min_samples  = 50    # need at least 50 events before ML kicks in

    def extract_features(self, event: dict) -> list:
        """
        Convert an event dict into a numeric feature vector.
        Features: [requests_last_60s, hour_of_day, status_code, path_length]
        """
        ip  = event.get("source_ip", "0.0.0.0")
        now = datetime.utcnow()

        # Count requests from this IP in last 60 seconds
        ip_request_counts[ip] = [
            t for t in ip_request_counts[ip]
            if (now - t).seconds < 60
        ]
        ip_request_counts[ip].append(now)
        req_rate = len(ip_request_counts[ip])

        hour        = now.hour
        status_code = int(event.get("status_code", 200))
        path_len    = len(event.get("path", ""))

        return [req_rate, hour, status_code, path_len]

    def add_training_sample(self, event: dict):
        features = self.extract_features(event)
        self.training_data.append(features)

        # Auto-train once enough data is collected
        if len(self.training_data) >= self.min_samples and not self.is_trained:
            self.train()

    def train(self):
        X = np.array(self.training_data)
        self.model.fit(X)
        self.is_trained = True
        print(f"[ML] Isolation Forest trained on {len(X)} samples.")

    def predict(self, event: dict) -> dict | None:
        """
        Returns an alert dict if the event is anomalous, else None.
        -1 from Isolation Forest = anomaly
        """
        if not self.is_trained:
            return None

        features = self.extract_features(event)
        X        = np.array([features])
        score    = self.model.decision_function(X)[0]  # negative = more anomalous
        pred     = self.model.predict(X)[0]            # -1 = anomaly, 1 = normal

        if pred == -1:
            return {
                "alert_type": "anomaly_detected",
                "source_ip":  event.get("source_ip", "unknown"),
                "severity":   "MEDIUM",
                "message":    f"ML anomaly detected from "
                              f"{event.get('source_ip','?')} "
                              f"(score: {score:.3f})",
                "features":   features,
                "event":      event
            }
        return None

# Global singleton
detector = AnomalyDetector()