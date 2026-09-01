import os
import re
import time
import subprocess
import markdown2
from bs4 import BeautifulSoup

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string



# key events like receive call, stop call, go back
def keyEvent(key_code):
    try:
        command =  f'adb shell input keyevent {key_code}'
        subprocess.run(command, shell=True, check=True)
        time.sleep(1)
    except subprocess.CalledProcessError:
        print("ADB not available or device not connected")

# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    try:
        command =  f'adb shell input tap {x} {y}'
        subprocess.run(command, shell=True, check=True)
        time.sleep(1)
    except subprocess.CalledProcessError:
        print("ADB not available or device not connected")

# Input Event is used to insert text in mobile
def adbInput(message):
    try:
        command =  f'adb shell input text "{message}"'
        subprocess.run(command, shell=True, check=True)
        time.sleep(1)
    except subprocess.CalledProcessError:
        print("ADB not available or device not connected")

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')

def markdown_to_text(md):
    html = markdown2.markdown(md)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()