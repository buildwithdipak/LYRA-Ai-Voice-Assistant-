import pyttsx3
import speech_recognition as sr
import eel
import time
# Import everything needed from features here
from lyra.modules.features import (
    speak, openCommand, PlayYoutube, findContact, 
    whatsApp, makeCall, sendMessage, geminai, 
    take_screenshot, capture_image, detect_faces, 
    set_volume, set_brightness, get_news
)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 6)
        except:
            return ""

    try:
        print('Recognizing...')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1) # Reduced sleep
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    
    # Determine input source (Voice vs Text)
    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = str(message).lower()
        eel.senderText(query)

    if not query:
        return

    try:
        if "open" in query:
            openCommand(query)
            
        elif "on youtube" in query:
            PlayYoutube(query)
            
        elif "screenshot" in query:
            take_screenshot()
            
        elif "camera" in query or "capture" in query:
            capture_image()
            
        elif "face detection" in query:
            # We run this in a thread so it doesn't block the UI, 
            # but note that the CV2 window must be handled carefully.
            import threading
            threading.Thread(target=detect_faces, daemon=True).start()
            
        elif "volume" in query:
            if "mute" in query: set_volume(0)
            elif "increase" in query: set_volume(100)
            elif "decrease" in query: set_volume(50)
            
        elif "brightness" in query:
            if "increase" in query: set_brightness(100)
            elif "decrease" in query: set_brightness(50)
            
        elif "news" in query:
            get_news()

        elif "send message" in query or "phone call" in query or "video call" in query:
            contact_no, name = findContact(query)
            
            if contact_no != 0:
                speak("Do you want to use WhatsApp or Mobile?")
                preference = takecommand() 
                
                if "mobile" in preference:
                    if "send message" in query:
                        speak("What is the message?")
                        msg = takecommand()
                        sendMessage(msg, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                        
                elif "whatsapp" in preference:
                    msg = ""
                    if "send message" in query:
                        speak("What is the message?")
                        msg = takecommand()
                    
                    flag = 'message' if "send message" in query else 'call'
                    if "video" in query: flag = 'video_call'
                    
                    whatsApp(contact_no, query, flag, name)
            else:
                speak("Contact not found")

        else:
            # Default to AI
            geminai(query)

    except Exception as e:
        print(f"Command Error: {e}")
    
    eel.ShowHood()