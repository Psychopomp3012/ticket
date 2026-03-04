from curl_cffi import requests
from datetime import datetime
import json
import re
import time

from components.telegram import send_telegram
from components.phone_siren import trigger_phone_siren
from components.phone_siren import is_acknowledged
from components.laptop_warning import trigger_laptop_siren

url = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-2/ET00474271"
# url = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-1-kolkata/ET00483392"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # You MUST include your valid cf_clearance cookie here!
    # "Cookie": "cf_clearance=YOUR_VALID_COOKIE_HERE; rgn=%7B%22regionCode%22%3A%22KOLK%22%7D;" 
}

AVAILABLE_KEYWORDS = [
    "Book Now", "Login to Book"
]

def check_ticket(count):
    try:
        response = requests.get(url, headers=headers, impersonate="chrome124")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if response.status_code == 200:
            print(f"[{now}] Request success")

            text = response.text

            match = re.search(r'"offers"\s*:\s*(\[[\s\S]*?\])', text)
            # 2nd
            keyword_pattern = r'(' + '|'.join(AVAILABLE_KEYWORDS) + r')'
            # match2 = re.search(keyword_pattern, text, re.IGNORECASE)
            
            match2 = True
            
            if not match:
                print("Offers block not found")
                return False

            offers_list = json.loads(match.group(1))
            # print(offers_list)

            if len(offers_list) > 0 and match2:
                print("🎉 Tickets available!")
                # send_telegram(f"🚨 TICKET AVAILABLE! Book NOW!: {count}")
                current_run_id = str(int(time.time()))
                
                while True:
                    # 1. Trigger the loud laptop audio
                    trigger_laptop_siren()
                    
                    # 2. Send the phone alert with the Kill Switch button
                    trigger_phone_siren(current_run_id)
                    
                    send_telegram(f"🚨 TICKET AVAILABLE! Book NOW!: {count}")
                    
                    # 3. Wait 30 seconds to give you time to grab your phone
                    print("Waiting 30 seconds for acknowledgment...")
                    time.sleep(30)
                    
                    # 4. Check if you pressed the Stop button on your phone
                    if is_acknowledged(current_run_id):
                        print("✅ Alarm acknowledged from phone! Shutting down permanently.")
                        return True
                    else:
                        print("❌ Not acknowledged yet. Ringing again!")
                
                return True
            else:
                print("No tickets yet")

        elif response.status_code == 403:
            print(f"[{now}] Blocked — cookie expired")
            send_telegram(f"Something Went wrong(403)")

        else:
            print(f"[{now}] Status: {response.status_code}")
            send_telegram(f"Something Went wrong")

    except Exception as e:
        print(f"[ERROR] {e}")

    return False