from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def make_phone_call():
    """Makes a real cellular phone call using Twilio."""
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
    TWILIO_PHONE = os.getenv("TWILIO_PHONE")
    MY_PHONE = os.getenv("MY_PHONE")

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        call = client.calls.create(
            # TwiML is the XML-like language Twilio uses for voice instructions
            twiml='<Response><Say loop="3">Emergency Alert! Book My Show tickets are live. Go to your laptop right now!</Say></Response>',
            to=MY_PHONE,
            from_=TWILIO_PHONE
        )
        print(f"[Call Success] Phone ringing! Call SID: {call.sid}")
    except Exception as e:
        print(f"[Call Error] Failed to make phone call: {e}")