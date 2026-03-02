from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime

# URL = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-2/ET00474271"
URL = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-1-kolkata/ET00483392"
CHECK_INTERVAL_MINUTES = 1  # Start with 5 min to avoid rate limits

AVAILABLE_KEYWORDS = [
    "book tickets", "book now", "buy tickets", "proceed", "select seats",
    "tickets available", "buy now", "proceed to book", "add to cart",
    "Book Now", "₹", "onwards"
]
COMING_SOON_KEYWORDS = ["coming soon", "comingsoon", "tickets soon", "more tickets soon"]

def check_tickets():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] Checking ticket status...")

    options = Options()
    options.add_argument("--headless=new")  # Modern headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = None
    try:
        # webdriver-manager handles chromedriver download/match
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(URL)
        time.sleep(12)  # Give time for Cloudflare/JS

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_text = soup.get_text(separator=' ', strip=True).lower()

        print("DEBUG - Page text snippet (first 600 chars):")
        print(page_text[:600])
        print("-" * 80)

        status_found = "unknown"

        if any(kw in page_text for kw in COMING_SOON_KEYWORDS):
            status_found = "Coming Soon"
        elif any(kw in page_text for kw in AVAILABLE_KEYWORDS):
            status_found = "TICKETS AVAILABLE!"
        elif "sold out" in page_text or "unavailable" in page_text:
            status_found = "Sold Out"
        elif "₹" in page_text and "onwards" in page_text:
            status_found = "TICKETS LIKELY AVAILABLE!"

        print(f"Status: {status_found}")

        if "AVAILABLE" in status_found.upper():
            alert_msg = f"ALERT! Tickets appear available!\nURL: {URL}\nStatus: {status_found}"
            print(alert_msg)
            # Add email here later if needed

        return "AVAILABLE" in status_found.upper()

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        if driver:
            driver.quit()

print("Starting ticket monitor for India vs England Semi-Final 2...")
print(f"Checks every {CHECK_INTERVAL_MINUTES} min.")

while True:
    found = check_tickets()
    if found:
        print("Alert triggered! Check Render logs or add notifications.")
    time.sleep(CHECK_INTERVAL_MINUTES * 60)
    
    
    
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def health():
    return "OK - Ticket monitor running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# Start Flask in background thread
threading.Thread(target=run_flask, daemon=True).start()