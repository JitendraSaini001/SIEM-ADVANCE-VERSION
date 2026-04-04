# 🛡️ SentinelIQ — Open-Source SIEM System

> A lightweight, real-time Security Information & Event Management system built with Python, Flask, MongoDB, and ML-based anomaly detection.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.x-47A248?style=flat&logo=mongodb&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Academic](https://img.shields.io/badge/Project-Academic-blue?style=flat)

---

## 📌 What is SentinelIQ?

SentinelIQ is a fully functional, open-source SIEM system built as an academic project for BCA Cybersecurity at Poornima University. It collects logs from multiple sources, detects real-world attack patterns using both rule-based logic and machine learning, stores everything in MongoDB, and displays live alerts on a dark-themed web dashboard.

Commercial SIEMs (Splunk, IBM QRadar, Microsoft Sentinel) cost ₹10L–₹1Cr/year. SentinelIQ demonstrates the same core concepts with zero cost, running on a single laptop.

---

## 🖥️ Live Dashboard Preview

```
🛡 SentinelIQ — Security Dashboard    ● LIVE (auto-refresh 5s)

  Critical    High      Medium    Total
  ───────     ────      ──────    ─────
    12          37        58       107

  Time       Type               Source IP         Severity   Message
  14:32:01   brute_force        45.33.32.156      HIGH       10 failed logins in 30s
  14:32:08   sql_injection      185.220.101.45    CRITICAL   UNION SELECT in path
  14:32:14   xss_attempt        192.241.186.56    HIGH       <script> detected in URL
  14:32:20   anomaly_detected   45.33.32.156      MEDIUM     Score: -0.342 (unusual rate)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **Real-time log collection** | Tails log files live using Python threading — no polling delay |
| **Multi-format parsing** | Regex-based parsing for SSH auth logs and Apache/Nginx HTTP logs |
| **Brute-force detection** | Triggers HIGH alert after 5+ failed SSH logins in 60 seconds per IP |
| **SQL Injection detection** | Matches UNION SELECT, DROP TABLE, `' OR '1'='1` in HTTP paths |
| **XSS detection** | Flags `<script>`, `javascript:`, `onerror=` patterns in URLs |
| **ML anomaly detection** | Isolation Forest model trains on live traffic, no labeled data needed |
| **MongoDB storage** | Stores all events and alerts with timestamps, severity, and source IP |
| **Live dashboard** | Flask + Chart.js dashboard with severity donut chart and top-IPs bar chart |
| **Attack simulator** | Generates realistic brute-force, SQLi, and XSS attack logs for testing |
| **Color-coded alerts** | Console output with CRITICAL (red) / HIGH (yellow) / MEDIUM (cyan) |

---

## 🏗️ Architecture

```
LOG SOURCES (System · Web · SSH · App)
         ↓
  [collector.py]  — Python threads tail log files in real time
         ↓
  [parser.py]     — Regex extracts IP, user, status code → JSON
         ↓
  ┌─────────────────────┬──────────────────────────┐
  │   [rules.py]        │   [ml_engine.py]          │
  │   Rule-based engine │   Isolation Forest (ML)   │
  │   Brute force       │   Feature extraction      │
  │   SQLi, XSS         │   Auto-trains on 50+ evts │
  └─────────┬───────────┴──────────┬───────────────┘
            ↓                      ↓
       [alerts.py]  ←─── Triggered alerts
            ↓
       [MongoDB]    ←─── Stores events + alerts
            ↓
    [Flask app.py]  ←─── REST API (/api/alerts, /api/stats)
            ↓
    [index.html]    ←─── Live dashboard at localhost:5000
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.10+ | Core logic, threading, log processing |
| Web Framework | Flask 3.x | REST API + dashboard serving |
| Database | MongoDB 7.x | Event and alert storage |
| ML | scikit-learn | Isolation Forest anomaly detection |
| Frontend | HTML5 + Chart.js | Real-time dashboard, no build step needed |
| File Watching | Python threading | Real-time log file tailing |
| Attack Simulation | Python | Generates test attack logs |

---

## 📁 Project Structure

```
sentineliq/
│
├── collector/
│   └── collector.py          # Real-time log file reader
│
├── parser/
│   └── parser.py             # SSH + HTTP log parsers (regex)
│
├── detection/
│   ├── rules.py              # Brute force, SQLi, XSS rules
│   └── ml_engine.py          # Isolation Forest anomaly detection
│
├── alerts/
│   └── alerts.py             # Alert dispatcher (console + MongoDB)
│
├── storage/
│   └── storage.py            # MongoDB read/write interface
│
├── simulator/
│   └── attack_simulator.py   # Generates fake attack logs
│
├── dashboard/
│   ├── app.py                # Flask server + REST API
│   └── templates/
│       └── index.html        # Live dashboard UI
│
├── logs/                     # Log files monitored by collector
│   ├── auth.log              # SSH auth log
│   └── access.log            # HTTP access log
│
├── requirements.txt
├── main.py                   # Entry point — starts everything
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MongoDB (running on localhost:27017)
- Node.js (optional, for development only)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sentineliq.git
cd sentineliq
```

### 2. Install Python dependencies

```bash
pip install flask pymongo scikit-learn watchdog requests numpy
```

### 3. Start MongoDB

```bash
# Linux/macOS
mongod --dbpath /data/db

# Windows
mongod --dbpath C:\data\db
```

### 4. Start the SIEM system

```bash
python main.py
```

### 5. Run the attack simulator (separate terminal)

```bash
python -m simulator.attack_simulator
```

### 6. Open the dashboard

Navigate to **http://localhost:5000** in your browser.

---

## 🔴 Simulated Attacks

The `attack_simulator.py` generates three attack types:

### SSH Brute Force
```
Apr 04 14:32:01 server sshd[1234]: Failed password for root from 45.33.32.156 port 22 ssh2
Apr 04 14:32:01 server sshd[1234]: Failed password for admin from 45.33.32.156 port 22 ssh2
... (10 attempts in 30 seconds)
→ Triggers: [HIGH] brute_force alert
```

### SQL Injection
```
GET /' OR '1'='1 HTTP/1.1  →  CRITICAL
GET /search?UNION SELECT * FROM users--  →  CRITICAL
```

### XSS Attempt
```
GET /search?q=<script>alert(1)</script>  →  HIGH
GET /page?onerror=fetch('evil.com')  →  HIGH
```

---

## 🤖 ML Anomaly Detection

The Isolation Forest model detects attacks without any labeled training data.

**Features extracted per event:**
| Feature | Normal | Attack |
|---|---|---|
| Requests per 60s | 3–10 | 80+ |
| Hour of day | 9–17 | 2–4 AM |
| HTTP status code | 200–304 | 400, 403, 500 |
| URL path length | 10–30 chars | 200+ chars |

**How it works:**
1. Collects features from every web log event
2. After 50+ events, trains `IsolationForest(contamination=0.05)`
3. Scores each new event — anomalous events need fewer random splits to isolate
4. Events scoring below the threshold trigger a `MEDIUM` anomaly alert

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Dashboard UI |
| `/api/alerts` | GET | Last 50 alerts (JSON) |
| `/api/stats` | GET | Alert counts by severity + top IPs |

**Example response — `/api/alerts`:**
```json
[
  {
    "alert_type": "brute_force",
    "source_ip": "45.33.32.156",
    "severity": "HIGH",
    "message": "10 failed logins in 60s from 45.33.32.156",
    "created_at": "2026-04-04T14:32:01.000Z"
  }
]
```

---

## 👥 Team Roles

| Role | Files | Responsibilities |
|---|---|---|
| **Backend Developer** | `collector.py`, `parser.py`, `storage.py`, `main.py` | Log tailing, regex parsing, MongoDB integration |
| **Security Analyst** | `rules.py`, `attack_simulator.py` | Detection rules (OWASP Top 10), attack simulation |
| **ML Engineer** | `ml_engine.py` | Feature engineering, Isolation Forest, auto-training |
| **Frontend Developer** | `app.py`, `index.html` | Flask API, Chart.js dashboard, severity badges |

---

## 📈 Results

| Test | Result |
|---|---|
| Brute force detection rate | 100% (all simulated attacks detected) |
| SQLi/XSS pattern accuracy | 100% (all 8 test payloads caught) |
| ML anomaly F-score | ~0.87 on mixed simulated traffic |
| End-to-end alert latency | < 1 second |
| Dashboard refresh rate | Every 5 seconds |

---

## 🔮 Future Scope

- **Wazuh integration** — Replace file tailing with production-grade Wazuh agent
- **Elasticsearch backend** — Scale to billions of events with ELK Stack
- **Email + Slack alerts** — Push CRITICAL alerts via SMTP / webhook
- **GeoIP mapping** — Visualize attacker origins on a world map
- **MITRE ATT&CK tagging** — Tag each alert with T-number (T1110 = Brute Force)
- **User Behavior Analytics** — Per-user baselines, impossible travel detection

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Attack classification
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) — Authentication guidelines
- [Isolation Forest Paper](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf) — Liu et al., 2008
- [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

---

## 📜 License

MIT License — free to use, modify, and distribute for academic and personal projects.

---

## 👤 Author

**Jitendra**  
BCA Cybersecurity (2024–2027)  
Poornima University, Jaipur, Rajasthan  
TryHackMe: Top 4% globally · 130+ rooms completed

---

> *"Security is not a product, it's a process."* — Bruce Schneier
