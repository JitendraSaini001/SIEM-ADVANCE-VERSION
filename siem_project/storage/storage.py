from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["siem_db"]

events_col = db["events"]
alerts_col = db["alerts"]

def store_event(event: dict):
    """Save a parsed log event to MongoDB."""
    event["stored_at"] = datetime.utcnow()
    events_col.insert_one(event)

def store_alert(alert: dict):
    """Save a triggered alert to MongoDB."""
    alert["created_at"] = datetime.utcnow()
    alerts_col.insert_one(alert)

def get_recent_alerts(limit=50):
    """Fetch recent alerts for the dashboard."""
    return list(alerts_col.find({}, {"_id": 0})
                          .sort("created_at", -1)
                          .limit(limit))

def get_event_count_by_ip():
    """Aggregate event counts per IP address."""
    pipeline = [
        {"$group": {"_id": "$source_ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    return list(events_col.aggregate(pipeline))

def get_alert_stats():
    """Count alerts by severity."""
    pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}}
    ]
    return list(alerts_col.aggregate(pipeline))