import picamera     #camera library
import pygame as pg #audio library
import os           #communicate with os/command line

from google.cloud import vision  #gcp vision library
from time import sleep
from adafruit_crickit import crickit
import time
import signal
import sys
import re           #regular expression lib for string searches!
import socket

#set up your GCP credentials - replace the " " in the following line with your .json file and path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/DET-2019-d3b82e6383ae.json"

# this line connects to Google Cloud Vision! 
client = vision.ImageAnnotatorClient()

# global variable for our image file - to be captured soon!
image = 'image.jpg'

def takephoto(camera):
    
    # this triggers an on-screen preview, so you know what you're photographing!
    camera.start_preview() 
    sleep(.5)                   #give it a pause so you can adjust if needed
    camera.capture('image.jpg') #save the image
    camera.stop_preview()       #stop the preview
        
def detect_hand(image):
    """Detects hand of cards in the image."""
    validCards = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    hand = []
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        print(text.description)
        if text.description in validCards:
            hand.append(text.description)
            
    return hand

def main():
    
    #generate a camera object for the takephoto function to
    #work with
    camera = picamera.PiCamera()
    host = '0.0.0.0'
    port = 9988
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
    
    while True:
        command = input("Enter command: ")
        if command == 'KILL':
            s.send(str.encode(command))
            break
        s.send(str.encode(command))
        reply = s.recv(1024)
        print(reply)
        
    s.close()
        
        
    #setup our pygame mixer to play audio in subsequent stages
#    pg.init()
#    pg.mixer.init()
"""   
    while True:
    #indicate that a new hand has been dealt with a cap touch
        if crickit.touch_1.value==0:
            hand = []
            
            # Keep taking pictures while a hand of 2 cards isn't detected
            while len(hand) != 2:
                takephoto(camera) # First take a picture

                with open('image.jpg', 'rb') as image_file:
                    #read the image file
                    content = image_file.read()
                    #convert the image file to a GCP Vision-friendly type
                    image = vision.types.Image(content=content)
                    hand = detect_hand(image)
                    print(hand)

                time.sleep(0.1)        
"""        
if __name__ == '__main__':
        main()    
