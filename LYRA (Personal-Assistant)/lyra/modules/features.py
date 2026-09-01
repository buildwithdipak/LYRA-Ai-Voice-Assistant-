import csv
import json
import os
from shlex import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import pygame
import eel
import pyaudio
import pyautogui
from lyra.core.config import ASSISTANT_NAME, LLM_KEY
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
import cv2
from lyra.utils.helper import extract_yt_term, markdown_to_text, remove_words
from hugchat import hugchat

from google import genai
import cv2
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import requests
import platform
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import screen_brightness_control as sbc
import tkinter as tk
from PIL import Image, ImageTk
import PyDictionary as dictionary
import threading

con = sqlite3.connect("LYRA.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "ui\\assets\\audio\\start_sound.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE LOWER(name) = LOWER(?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Understood. Opening " + query + " now.")
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name) = LOWER(?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Got it. Launching " + query + " in your browser.")
                    webbrowser.open(results[0][0])

                else:
                    speak("One moment. Executing " + query + ".")
                    try:
                        os.system('start '+query)
                    except:
                        speak("I'm sorry, I couldn't find that. Let me know if you need help with something else.")
        except:
            speak("some thing went wrong")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 6)
        except:
            return ""

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        return ""

def process_command(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "screenshot" in command:
        take_screenshot()
    elif "camera" in command or "capture image" in command:
        capture_image()
    elif "face detection" in command:
        threading.Thread(target=detect_faces, daemon=True).start()
    elif "who am i" in command or "about me" in command:
        speak(f"You are {user_profile['name']}, a {user_profile['age']} year old {user_profile['profession']} from {user_profile['location']}.")
    elif "volume" in command:
        if "mute" in command:
            set_volume(0)
        elif "increase" in command:
            set_volume(100)
        elif "decrease" in command:
            set_volume(50)
        elif "set volume to" in command:
            try:
                level = int(''.join(filter(str.isdigit, command)))
                set_volume(level)
            except:
                speak("Invalid volume level")
    elif "brightness" in command:
        if "set brightness to" in command:
            try:
                level = int(''.join(filter(str.isdigit, command)))
                set_brightness(level)
            except:
                speak("Invalid brightness level")
        elif "increase" in command:
            set_brightness(100)
        elif "decrease" in command:
            set_brightness(50)
    else:
        response = ai_process(command)
        speak(response)

def listen_after_wake():
    recognizer = sr.Recognizer()
    wake_word_heard = False

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)

                if not wake_word_heard:
                    print("🎧 Waiting for wake word: 'lyra'")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    try:
                        wake_word = recognizer.recognize_google(audio).lower()
                        print(f"🔊 Heard: {wake_word}")
                        if "lyra" in wake_word or "Lyra" in wake_word or "LYRA" in wake_word or "Layra" in wake_word:
                            speak("Yes sir")
                            wake_word_heard = True
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        speak(f"Speech service error: {e}")
                else:
                    print("🎧 Lyra is now listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                    try:
                        command = recognizer.recognize_google(audio).lower()
                        print(f"📢 You said: {command}")
                        process_command(command)
                    except sr.UnknownValueError:
                        print("🤔 Didn't catch that.")
                    except sr.RequestError as e:
                        speak(f"API error: {e}")
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            speak(f"⚠️ Error occurred: {e}")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["LYRA","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")
                speak("Hello sir, how can I help you?")
        start_continuous_listening()
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video', 'whatsapp']
    query = remove_words(query, words_to_remove)
    query = query.strip().lower()

    try:
        # First try exact match (case insensitive)
        cursor.execute("SELECT mobile_no, name FROM contacts WHERE LOWER(name) = ?", (query,))
        results = cursor.fetchall()
        
        if not results:
            # If no exact match, try partial matches
            cursor.execute("SELECT mobile_no, name FROM contacts WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
            results = cursor.fetchall()
            
            if not results:
                # Try if query matches start of any name
                cursor.execute("SELECT mobile_no, name FROM contacts WHERE LOWER(name) LIKE ?", (query + '%',))
                results = cursor.fetchall()
                
                if not results:
                    # Try reverse - if name contains query at start
                    cursor.execute("SELECT mobile_no, name FROM contacts WHERE LOWER(name) LIKE ?", ('%' + query,))
                    results = cursor.fetchall()

        if results:
            # Return the first match with the actual name from database
            mobile_number_str = str(results[0][0])
            actual_name = results[0][1]
            
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            print(f"Found contact: {actual_name} - {mobile_number_str}")
            return mobile_number_str, actual_name
        else:
            print('Contact not found in database')
            return 0, 0
            
    except Exception as e:
        print(f"Error finding contact: {e}")
        return 0, 0
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        LYRA_message = "message send successfully to "+name

    elif flag == 'call':
        message = ''
        LYRA_message = "calling to "+name

    else:
        message = ''
        LYRA_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(f"Encoded message: {encoded_message}")
    
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    print(f"WhatsApp URL: {whatsapp_url}")

    # Open WhatsApp with the constructed URL
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.run(full_command, shell=True)
    
    # Wait for WhatsApp to open and load
    time.sleep(8)
    
    # For message sending, just press Enter (message should already be typed)
    if flag == 'message':
        pyautogui.press('enter')
        time.sleep(2)
    
    speak(LYRA_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    try:
        import requests
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}  # Replace with your token or use free if available
        payload = {"inputs": user_input, "parameters": {"max_length": 100}}
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                response_text = result[0].get("generated_text", "No response")
            else:
                response_text = "AI response generated."
        else:
            response_text = "AI service is currently unavailable."
        print(response_text)
        speak(response_text)
        return response_text
    except Exception as e:
        error_msg = "AI service is currently unavailable due to setup issues."
        speak(error_msg)
        return error_msg

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from lyra.utils.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

def geminai(query):
    # Using Hugging Face chat instead of Gemini due to quota issues
    chatBot(query)

# Settings Modal 

WEATHER_API_KEY = "ENTER YOUR OPEN WETHER API KEY"
API_KEY = "ENTER YOUR GEMINI AI API KEY"
NEWS_API_KEY = "ENTER YOUR NEWS API KEY"
FACE_CASCADE_PATH = "data/auth/haarcascade_frontalface_default.xml"

recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()
TEMP_AUDIO_FILE = "temp.mp3"

def speak(text):
    print(f"🗣️ LYRA: {text}")
    try:
        eel.receiverText(text)  # GUI me dikhane ke liye
    except:
        pass

    try:
        tts = gTTS(text=text, lang='en')
        tts.save(TEMP_AUDIO_FILE)

        pygame.mixer.music.load(TEMP_AUDIO_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except:
            pass

        for _ in range(3):
            try:
                os.remove(TEMP_AUDIO_FILE)
                break
            except PermissionError:
                time.sleep(0.1)
    except Exception as e:
        print(f"gTTS failed: {e} — falling back to pyttsx3")
        engine.say(text)
        engine.runAndWait()



def get_user_city():
    try:
        ip_info = requests.get('https://ipapi.co/json').json()
        return ip_info.get("city", "Delhi")
    except:
        return "Delhi"

def get_weather():
    city = get_user_city()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=hi"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"{city} के मौसम की जानकारी नहीं मिल पाई।"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f" तापमान {temp} डिग्री सेल्सियस है और मौसम {desc} है।"
    except:
        return "मौसम सर्वर से संपर्क नहीं हो पाया।"


def update_user_location():
    try:
        ip_info = requests.get('https://ipapi.co/json').json()
        city = ip_info.get("city", "Unknown")
        region = ip_info.get("region", "")
        country = ip_info.get("country_name", "")
        location = f"{city}, {region}, {country}"
        user_profile["location"] = location
        return location
    except:
        user_profile["location"] = "India"
        return "India"
    
def number_to_hindi(num):
    hindi_numbers = {
        0: "शून्य", 1: "एक", 2: "दो", 3: "तीन", 4: "चार", 5: "पांच",
        6: "छह", 7: "सात", 8: "आठ", 9: "नौ", 10: "दस", 11: "ग्यारह",
        12: "बारह", 13: "तेरह", 14: "चौदह", 15: "पंद्रह", 16: "सोलह",
        17: "सत्रह", 18: "अठारह", 19: "उन्नीस", 20: "बीस", 21: "इक्कीस",
        22: "बाईस", 23: "तेईस", 24: "चौबीस", 25: "पच्चीस", 26: "छब्बीस",
        27: "सत्ताईस", 28: "अट्ठाईस", 29: "उनतीस", 30: "तीस", 31: "इकतीस",
        32: "बत्तीस", 33: "तैंतीस", 34: "चौंतीस", 35: "पैंतीस", 36: "छत्तीस",
        37: "सैंतीस", 38: "अड़तीस", 39: "उनतालीस", 40: "चालीस", 41: "इकतालीस",
        42: "बयालीस", 43: "तैंतालीस", 44: "चवालीस", 45: "पैंतालीस", 46: "छयालिस",
        47: "सैंतालीस", 48: "अड़तालीस", 49: "उनचास", 50: "पचास", 51: "इक्यावन",
        52: "बावन", 53: "तिरेपन", 54: "चौवन", 55: "पचपन", 56: "छप्पन",
        57: "सत्तावन", 58: "अट्ठावन", 59: "उनसठ"
    }
    return hindi_numbers.get(num, str(num))


def get_time_in_hindi():
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min

    # Convert 24-hour to 12-hour
    if hour == 0:
        hour = 12
        ampm = "रात"
    elif hour < 12:
        ampm = "सुबह"
    elif hour == 12:
        ampm = "दोपहर"
    else:
        hour -= 12
        ampm = "शाम"

    hour_text = number_to_hindi(hour)
    minute_text = number_to_hindi(minute)

    if minute == 0:
        return f"{ampm} के {hour_text} बजे हैं"
    else:
        return f"{ampm} के {hour_text} बजकर {minute_text} मिनट हुए हैं"




user_profile = {
    "name": "Deepak Maurya",
    "age": 21,
    "profession": "Computer Science Student",
    "skills": ["Python", "AI", "Web Development"],
    "hobbies": ["Gaming", "Coding", "Listening Music"],
   "location": ["Varanasi , India"]

}

#IMAGE FOLER ME SAVE HOE
def ensure_snap_folder():
    folder_path = "snap"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def ai_process(command):
    try:
        import requests
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}  # Replace with your token or use free if available
        payload = {"inputs": command, "parameters": {"max_length": 100}}
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get("generated_text", "No response").strip()
            return "AI response generated."
        else:
            return "AI service is currently unavailable."
    except Exception as e:
        print(f"AI error: {e}")
        return "AI service is currently unavailable."

def open_application(app):
    speak(f"Opening {app}")
    os_name = platform.system()
    app = app.lower()
    try:
        if "chrome" in app:
            os.system("start chrome" if os_name == "Windows" else "google-chrome")
        elif "notepad" in app:
            os.system("notepad" if os_name == "Windows" else "gedit")
        elif "code" in app:
            os.system("code")
        else:
            speak("Application not configured.")
    except Exception as e:
        speak(f"Error opening app: {e}")

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        speak(f"Volume set to {level} percent")
    except Exception as e:
        speak(f"Volume adjustment failed: {e}")

def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent")
    except Exception as e:
        speak(f"Brightness adjustment failed: {e}")

def take_screenshot():
    folder = ensure_snap_folder()
    filename = os.path.join(folder, f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")


def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        speak("Webcam not available")
        return
    ret, frame = cam.read()
    if ret:
        folder = ensure_snap_folder()
        filename = os.path.join(folder, f"webcam_{int(time.time())}.png")
        cv2.imwrite(filename, frame)
        speak(f"Image saved as {filename}")
    cam.release()


def detect_faces():
    speak("Face detection started")
    root = tk.Tk()
    root.title("Face Detection")
    label = tk.Label(root)
    label.pack()

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    def update():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            label.imgtk = img
            label.configure(image=img)
        label.after(10, update)

    root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy(), speak("Face detection stopped")))
    update()
    root.mainloop()

def get_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        articles = r.json().get('articles', [])[:5]
        speak("Here are the top headlines.")
        for article in articles:
            speak(article.get('title', ''))
    except:
        speak("Unable to fetch news")

def get_meaning(command):
    words = command.lower().replace("meaning of", "").replace("what is", "").strip()
    if not words:
        speak("Please provide the word or phrase you'd like the meaning of.")
        return
    meaning = dictionary.meaning(words)
    if meaning:
        first_def = next(iter(meaning.values()))[0]
        speak(f"The meaning of {words} is: {first_def}")
    else:
        speak(f"Sorry, I couldn't find the meaning of {words}.")


#------PROCESS COMMAND------------
    words = command.lower().replace("meaning of", "").replace("what is", "").strip()
    if not words:
        speak("Please provide the word or phrase you'd like the meaning of.")
        return
    meaning = dictionary.meaning(words)
    if meaning:
        first_def = next(iter(meaning.values()))[0]
        speak(f"The meaning of {words} is: {first_def}")
    else:
        speak(f"Sorry, I couldn't find the meaning of {words}.")



# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    con.commit()
    personalInfo()
    return 1



@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, MobileNo, Email, City))
    con.commit()


@eel.expose
def InsertMultipleContacts(contacts_list):
    """Insert multiple contacts at once. contacts_list should be a list of tuples: [(name, mobile, email, city), ...]"""
    try:
        cursor.executemany(
            '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', 
            [(None, name, mobile, email or None, city or None) for name, mobile, email, city in contacts_list]
        )
        con.commit()
        return f"Successfully added {len(contacts_list)} contacts"
    except Exception as e:
        con.rollback()
        return f"Error adding contacts: {str(e)}"


def importContactsFromCSV(csv_file_path):
    """Import contacts from CSV file. Expected format: name,mobile,email,city"""
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # Skip header row if exists
            
            contacts_data = []
            for row in csvreader:
                if len(row) >= 2:  # At least name and mobile required
                    name = row[0].strip()
                    mobile = row[1].strip()
                    email = row[2].strip() if len(row) > 2 else None
                    city = row[3].strip() if len(row) > 3 else None
                    
                    if name and mobile:  # Only add if name and mobile are not empty
                        contacts_data.append((None, name, mobile, email, city))
            
            if contacts_data:
                cursor.executemany('''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', contacts_data)
                con.commit()
                return f"Successfully imported {len(contacts_data)} contacts from CSV"
            else:
                return "No valid contacts found in CSV file"
                
    except FileNotFoundError:
        return f"CSV file not found: {csv_file_path}"
    except Exception as e:
        con.rollback()
        return f"Error importing CSV: {str(e)}"
