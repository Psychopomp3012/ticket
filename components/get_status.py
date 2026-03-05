from curl_cffi import requests
from datetime import datetime
import re
from typing import Literal

# def check_ticket(url: str, count: int) -> Literal["coming_soon", "sold_out"]:

from components.telegram import send_telegram
from components.phone_siren import trigger_phone_siren
from components.phone_siren import is_acknowledged
from components.laptop_warning import trigger_laptop_siren

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # You MUST include your valid cf_clearance cookie here!
    # "Cookie": "cf_clearance=YOUR_VALID_COOKIE_HERE; rgn=%7B%22regionCode%22%3A%22KOLK%22%7D;" 
}

def get_status(url:str) -> Literal["coming_soon", "available", "sold_out", "unknown"]:
    """Return the status
    coming_soon | available | sold_out | unknown
    
    condition 1: event_status
    """
    try:
        response = requests.get(url, headers=headers, impersonate="chrome124")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if response.status_code == 200:
            print(f"[{now}] Request success - 125")

            text = response.text

            # --------------------------
            # 1st
            # match1 = re.search(r'"offers"\s*:\s*(\[[\s\S]*?\])', text)
            # offers_list = json.loads(match1.group(1))
            # print(offers_list)
            #----------------------------
            
            match_obj = re.search(r'"event_status"\s*:\s*"([^"]+)"', text)
            
            if not match_obj:
                print("Could not find 'event_status' in the page source.")
                return "unknown"
                
            match1 = match_obj.group(1)
            
            if match1 == "registration":
                print("🎉 Tickets available!")
                return "available"
            
            elif match1 == "sold_out":
                print("No tickets yet")
                return "sold_out"
            
            elif match1 == "coming_soon":
                return "coming_soon"
            
            else:
                print(f"Unknown case in check_ticket() | match1: {match1}")
                return "unknown"
                

        elif response.status_code == 403:
            print(f"[{now}] Blocked — cookie expired")
            send_telegram(f"Something Went wrong(403)")
            return "unknown" 

        else:
            print(f"[{now}] Status: {response.status_code}")
            # send_telegram(f"Something Went wrong")
            return "unknown"

    except Exception as e:
        print(f"[ERROR] {e}")
        return "unknown"

