import os

def trigger_laptop_siren():
    """Takes over the Linux desktop to alert you immediately."""
    print("🚨 TRIGGERING LOCAL SIREN! 🚨")
    
    try:
        # 1. Force the system volume to 100% (so you hear it even if muted)
        os.system("pactl set-sink-volume @DEFAULT_SINK@ 100%")
        
        # 2. Throw a massive popup window in the center of the screen
        # The '&' at the end makes it run in the background so it doesn't freeze the script
        os.system('zenity --warning --title="🚨 TICKETS LIVE! 🚨" --text="OPEN BOOKMYSHOW NOW!" --width=1080 --height=720 &')
        
        # 3. Use Linux Text-to-Speech to scream at you
        for _ in range(3):
            # 3. Play the audio file!
            # ---> OPTION A: If you are using a .wav or .ogg file (Built into most Linux distros)
            os.system(f'paplay "assets/alert.wav"')
            
    except Exception as e:
        print(f"[Local Alarm Error] Failed to trigger alarm: {e}")
        