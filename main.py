# main.py

from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import datetime
import random
import os
import getpass
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import click_login_button
from location import enter_location_details
from options import read_ride_options
from confirm_and_request import confirm_and_request_ride


# === Speak Function ===
def nova_speak(text):
    print(f"\n🔊 Nova: {text}")
    tts = gTTS(text=text, lang='en')
    filename = f"nova_{random.randint(1000,9999)}.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# === Listen Function ===
def nova_listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(mic)
        try:
            audio = recognizer.listen(mic, timeout=8, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-IN')
            print(f"🗣️ You said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("⏱️ No response detected.")
            return ""
        except:
            nova_speak("Sorry, I didn't understand.")
            return ""

# === Greeting ===
def get_time_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# === Introduce Nova ===
def nova_intro():
    messages = [
        "Hello, I'm NovaCab. Your voice is my command.",
        "I'm Nova, designed by Sahil to assist you with cabs and conversation.",
        "Nova here! Ready to make your travels smooth and easy."
    ]
    nova_speak(random.choice(messages))

# === Sleep Mode ===
def sleep_mode():
    nova_speak("Entering sleep mode. Say 'wake up Nova' when you're ready.")
    while True:
        cmd = nova_listen()
        if "wake up nova" in cmd or ("wake" in cmd and "nova" in cmd):
            nova_speak("Nova is awake and ready.")
            break

# === Open Uber Mobile Website with Persistence ===
def open_uber_with_persistence():
    nova_speak("Opening Uber mobile website. Please wait...")

    try:
        username = getpass.getuser()
        custom_profile = f"C:\\Users\\{username}\\clova-mobile-profile"

        options = uc.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
            "Mobile/15E148 Safari/604.1"
        )
        options.add_argument(f"--user-data-dir={custom_profile}")
        options.add_argument("--profile-directory=Profile1")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # ✅ Don't add 'detach' for undetected_chromedriver
        driver = uc.Chrome(version_main=138, options=options)
        driver.set_window_size(420, 900)

        # Open Uber mobile site
        driver.get("https://m.uber.com/go/home")

        click_login_button(driver, nova_speak)
        enter_location_details(driver, nova_speak, nova_listen)
        read_ride_options(driver)
        confirm_and_request_ride(driver)



    except Exception as e:
        print(f"⚠️ Error: {e}")
        nova_speak("Failed to open Uber mobile website.")


# === Command Handler ===
def handle_command(cmd):
    if "introduce" in cmd or "who are you" in cmd:
        nova_intro()
    elif "sleep" in cmd:
        sleep_mode()
    elif "exit" in cmd or "quit" in cmd:
        nova_speak("Goodbye. Nova signing off.")
        return False
    elif "book a cab" in cmd or "open uber" in cmd:
        open_uber_with_persistence()
    else:
        nova_speak("I didn't catch that.")
    return True

# === Assistant Loop ===
def nova_loop():
    nova_speak("Nova is standing by. Say 'wake up Nova' to begin.")
    awake = False

    while True:
        command = nova_listen()
        if not awake:
            if "wake up nova" in command or ("wake" in command and "nova" in command):
                awake = True
                nova_speak(get_time_greeting())
                continue
            else:
                continue

        if not handle_command(command):
            break

# === Start Nova ===
if __name__ == "__main__":
    nova_loop()
