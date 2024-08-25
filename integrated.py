import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pyttsx3
import speech_recognition as sr
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
import pywhatkit as kit
import googlesearch
from googlesearch import search
import geocoder


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu App")
        self.root.geometry("400x500")
        self.root.configure(bg="sky blue")

        tk.Label(self.root, text="Welcome to the Menu", font=("Playfair Display", 50, "bold"), bg="Sky Blue", fg="Dark Green").pack(pady=20)

        actions = [
            ("Send WhatsApp Message", self.sendWhatsapp),
            ("Send Bulk Email", self.sendBulkEmail),
            ("Get Top 5 Google Search Results", self.top5ResultGoogle),
            ("Find Location", self.findLocation),
            ("Convert Text to Audio", self.textToAudio),
            ("Convert Audio to Text", self.audioToText),
            ("Control System Volume", self.cntrlSystemVolume),
            ("Create Custom Image with NumPy", self.ownImgNumpy),
            ("Crop and Overlay Images", self.cutPhotoShowOnTop),
            ("Capture from Two Cameras", self.twoCameraOutputOneFrame),
            ("Open Notepad", self.openNotepad),
            ("Record Video", self.recordVideo),  # Added video recording button
        ]

        for text, command in actions:
            tk.Button(self.root, text=text, command=command, font=("Times New Roman", 15), bg= "#0FFCBE", fg="black", relief="flat", borderwidth=0).pack(pady=7)

        # Exit button
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Cursive", 12), bg="red", fg="white", relief="raised", borderwidth=4).pack(pady=20)

        # Canvas for custom button design
        

    def sendWhatsapp(self):
        phone_number = simpledialog.askstring("Phone Number", "Enter the target phone number (with country code):")
        message = simpledialog.askstring("Message", "Enter the message:")
        
        if phone_number and message:
            try:
                kit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True, close_time=2)
                messagebox.showinfo("Success", "Message sent successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter both phone number and message.")

    def sendBulkEmail(self):
        subject = simpledialog.askstring("Subject", "Enter email subject:")
        body = simpledialog.askstring("Body", "Enter email message:")
        if subject and body:
            try:
                ob = smtplib.SMTP('smtp.gmail.com', 587)
                ob.ehlo()
                ob.starttls()
                ob.login('kaminikaroliwal@gmail.com', 'nuxg jfgj zseb wchf')
                message = f'Subject: {subject}\n\n{body}'
                ob.sendmail('kaminikaroliwal@gmail.com', 'kaminikaroliwal@gmai', message)
                messagebox.showinfo("Success", "Email sent successfully")
            except smtplib.SMTPAuthenticationError as e:
                messagebox.showerror("Authentication Error", f"Failed to authenticate: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
            finally:
                ob.quit()
        else:
            messagebox.showwarning("Input Error", "Please enter both subject and body.")

    def top5ResultGoogle(self):
        query = simpledialog.askstring("Search Query", "Enter your search query:")
        if query:
           search_results = list(search(query))  # Convert the generator to a list
           results = "\n".join([f"{i+1}. {result}" for i, result in enumerate(search_results[:5])])
           messagebox.showinfo("Top 5 Google Search Results", results)
        else:
           messagebox.showwarning("Input Error", "Please enter a search query.")


    def findLocation(self):
        g = geocoder.ip('me')
        latlng = g.latlng
        city = g.city
        state = g.state
        country = g.country

        location_info = f"Coordinates: {latlng}\nCity: {city}\nState: {state}\nCountry: {country}"
        messagebox.showinfo("Location", location_info)

        engine = pyttsx3.init()
        speech_text = f"You are currently located in {city}, {state}, {country}. The coordinates are {latlng}."
        engine.say(speech_text)
        engine.runAndWait()

    def textToAudio(self):
        def string_to_audio(text):
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate - 50)
            volume = engine.getProperty('volume')
            engine.setProperty('volume', volume + 0.25)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(text)
            engine.runAndWait()

        text = simpledialog.askstring("Text to Speech", "Enter the text you want to convert to speech:")
        if text:
            string_to_audio(text)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def audioToText(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Info", "Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            messagebox.showinfo("Info", "Listening... Please speak into the microphone.")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            messagebox.showinfo("Recognized Text", f"You said: {text}")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results from Google Web Speech API; {e}")

    def cntrlSystemVolume(self):
        def get_volume():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = volume.GetMasterVolumeLevelScalar()
            return current_volume

        def set_volume(level):
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level, None)

        def change_volume(change):
            current_volume = get_volume()
            new_volume = current_volume + change
            new_volume = max(0.0, min(1.0, new_volume))
            set_volume(new_volume)
            messagebox.showinfo("Volume Changed", f"Volume changed to: {new_volume * 100:.2f}%")

        change = simpledialog.askfloat("Volume Change", "Enter volume change (-0.1 to decrease by 10%, 0.1 to increase by 10%):")
        if change is not None:
            change_volume(change)

    def ownImgNumpy(self):
        car_image = np.zeros((100, 100, 3), dtype=np.uint8)
        background_color = [135, 206, 235]
        car_body_color = [255, 0, 0]
        window_color = [12, 24, 232]
        wheel_color = [0, 0, 0]

        car_image[:, :] = background_color
        car_image[60:80, 20:80] = car_body_color
        car_image[50:60, 30:70] = car_body_color
        car_image[55:60, 35:45] = window_color
        car_image[55:60, 55:65] = window_color
        car_image[80:85, 30:40] = wheel_color
        car_image[80:85, 60:70] = wheel_color

        plt.imshow(car_image)
        plt.axis('off')
        plt.show()

    def cutPhotoShowOnTop(self):
        def capture_image():
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite('captured_image.jpg', frame)
            return ret, frame

        def crop_image(image_path, left, top, right, bottom):
            image = Image.open(image_path)
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save('cropped_image.png')
            return cropped_image

        def overlay_images(original_img_path, cropped_img_path, x_offset, y_offset):
            original_img = cv2.imread(original_img_path)
            cropped_img = Image.open(cropped_img_path).convert("RGBA")
            original_img_pil = Image.fromarray(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)).convert("RGBA")
            original_img_pil.paste(cropped_img, (x_offset, y_offset), cropped_img)
            combined = cv2.cvtColor(np.array(original_img_pil), cv2.COLOR_RGBA2BGRA)
            cv2.imwrite('overlayed_image.png', combined)
            return combined

        ret, frame = capture_image()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image")
            return

        height, width, _ = frame.shape
        left = width // 4
        top = height // 4
        right = left + 200
        bottom = top + 200

        crop_image('captured_image.jpg', left, top, right, bottom)
        x_offset = 50
        y_offset = 50
        result_image = overlay_images('captured_image.jpg', 'cropped_image.png', x_offset, y_offset)

        cv2.imshow('Overlayed Image', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def twoCameraOutputOneFrame(self):
        def main():
            cap1 = cv2.VideoCapture(0)
            cap2 = cv2.VideoCapture(1)

            if not cap1.isOpened() or not cap2.isOpened():
                messagebox.showerror("Error", "Could not open one or both cameras.")
                return

            while True:
                ret1, frame1 = cap1.read()
                ret2, frame2 = cap2.read()

                if not ret1 or not ret2:
                    messagebox.showerror("Error", "Could not read frame from one or both cameras.")
                    break

                frame1 = cv2.resize(frame1, (640, 480))
                frame2 = cv2.resize(frame2, (640, 480))
                combined_frame = cv2.hconcat([frame1, frame2])

                cv2.imshow('Combined Frame', combined_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap1.release()
            cap2.release()
            cv2.destroyAllWindows()

        main()

    def openNotepad(self):
        os.system("notepad.exe")

    def recordVideo(self):
        def start_recording():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open camera.")
                return

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                cv2.imshow('Recording', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Info", "Video recording completed and saved as 'output.avi'.")

        start_recording()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
