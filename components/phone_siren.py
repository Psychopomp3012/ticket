import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOPIC_ALERT = os.getenv("TOPIC_ALERT") # Laptop => cell phone
TOPIC_ACK = os.getenv("TOPIC_ACK") # Cell phone => Laptop'

def trigger_phone_siren():
    """Sends an ultra-urgent alert to your phone with siren sound + direct BookMyShow button."""
    
    # When sending JSON to ntfy, you post to the root URL, not the topic URL
    url = "https://ntfy.sh/"
    
    payload = {
        "topic": TOPIC_ALERT,
        "title": "🚨 TICKETS LIVE RIGHT NOW! 🚨",
        "message": "🚨 TICKETS ARE AVAILABLE!\nOPEN BOOKMYSHOW IMMEDIATELY OR MISS IT!",
        "priority": 5,                                 # MAX urgency
        "tags": ["siren", "rotating_light", "warning"], # big red icons
        "click": "https://in.bookmyshow.com/",          # tap anywhere opens it
        "actions": [
            {
                "action": "view",
                "label": "Open BookMyShow NOW!",
                "url": "https://in.bookmyshow.com/",
                "clear": True
            },
            {
                # THIS IS THE MAGIC KILL SWITCH BUTTON
                "action": "http",
                "label": "🛑 STOP ALARM",
                "url": f"https://ntfy.sh/{TOPIC_ACK}",
                "method": "POST",
                "body": "ACKNOWLEDGED",
                "clear": True
            }
        ]
    }
    
    try:
        # Use json=payload instead of data=message and headers=headers
        requests.post(url, json=payload, timeout=5)
        print("✅ Phone siren triggered!")
    except Exception as e:
        print(f"[Phone Alert Error] {e}")
        
        
def is_acknowledged():
    """Checks the secret ACK topic to see if you pressed the Stop button in the last 10 seconds."""
    try:
        # poll=1 means "don't wait, return immediately"
        # since=10s ensures we only look at button presses from the last 10 seconds
        url = f"https://ntfy.sh/{TOPIC_ACK}/json?poll=1&since=120s"
        response = requests.get(url, timeout=5)
        
        # If the word "ACKNOWLEDGED" is in the response, you pressed the button!
        if "ACKNOWLEDGED" in response.text:
            return True
    except Exception as e:
        pass
    
    return False


print(is_acknowledged())