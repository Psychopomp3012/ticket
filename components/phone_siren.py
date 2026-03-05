import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOPIC_ALERT = os.getenv("TOPIC_ALERT") # Laptop => cell phone
TOPIC_ACK = os.getenv("TOPIC_ACK") # Cell phone => Laptop'

def trigger_phone_siren(run_id: str):
    """Sends the alert with a unique kill-switch ID."""
    url = "https://ntfy.sh/"
    
    payload = {
        "topic": TOPIC_ALERT,
        "title": "🚨 TICKETS LIVE RIGHT NOW! 🚨",
        "message": "Tickets are live! Press the STOP button below to kill this alarm loop.",
        "priority": 5,
        "tags": ["siren", "warning"],
        "actions": [
            {
                "action": "view",
                "label": "🎟️ Open BookMyShow",
                "url": "https://in.bookmyshow.com/",
                "clear": True
            },
            {
                "action": "http",
                "label": "🛑 STOP ALARM",
                "url": f"https://ntfy.sh/{TOPIC_ACK}",
                "method": "POST",
                # WE NOW SEND THE UNIQUE RUN ID
                "body": f"ACK_{run_id}", 
                "clear": True
            }
        ]
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[Phone Alert Error] {e}")
        
def is_acknowledged(run_id: str) -> bool:
    """Checks if the phone sent back this specific run_id."""
    try:
        url = f"https://ntfy.sh/{TOPIC_ACK}/json?poll=1&since=50s"
        response = requests.get(url, timeout=5)
        
        # WE NOW LOOK FOR THE EXACT UNIQUE ID
        if f"ACK_{run_id}" in response.text:
            return True
    except Exception as e:
        pass
    
    return False