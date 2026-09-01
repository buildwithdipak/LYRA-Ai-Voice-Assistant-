import os
import eel
import subprocess
import sys
import threading
import cv2
from lyra.modules.features import *
from lyra.modules.command import *
from lyra.modules.recoganize import AuthenticateFace as recoganize
def start():
    
    eel.init("ui")

    playAssistantSound()
    @eel.expose
    def init():
        try:
            subprocess.run(['cmd', '/c', 'lyra\\utils\\device.bat'], check=True)
        except subprocess.CalledProcessError:
            print("ADB setup failed - continuing without Android device connection")
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Deepak Sir. How can I help you today?")
            eel.hideStart()
            playAssistantSound()
            eel.hideMicBtn()
            # Start wake word listening
            from lyra.modules.features import listen_after_wake
            threading.Thread(target=listen_after_wake, daemon=True).start()
        else:
            speak("Face Authentication Fail")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)