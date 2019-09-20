import picamera     #camera library
import pygame as pg #audio library
import os           #communicate with os/command line

from google.cloud import vision  #gcp vision library
from time import sleep
from adafruit_crickit import crickit
from PIL import Image
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
    crop('image.jpg', (0,0,1920,540), 'dealer_image.jpg')
    crop('image.jpg', (0,540,1920,1080), 'player_image.jpg')
    camera.stop_preview()       #stop the preview

def crop(image, coords, new_image):
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(new_image)
    cropped_image.show()
    
def detect_hand(image):
    """Detects hand of cards in the image."""
    validCards = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    hand = []
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        if text.description in validCards:
            hand.append(text.description)
            
    return hand

def capture_initial_hands(camera):
    player_hand = []
    dealer_hand = []
            
    # Keep taking pictures if the correct number of cards isn't detected
    while len(player_hand) is not 2 or len(dealer_hand) is not 1:
        takephoto(camera) # Capture a picture

        with open('player_image.jpg', 'rb') as image_file:
            #read the image file
            content = image_file.read()
            #convert the image file to a GCP Vision-friendly type
            image = vision.types.Image(content=content)
            player_hand = detect_hand(image)
            print("Player hand: ")
            for card in player_hand:
                print(card)
                print("Number of player cards: " + str(len(player_hand)))
                    
        with open('dealer_image.jpg', 'rb') as image_file:
            #read the image file
            content = image_file.read()
            #convert the image file to a GCP Vision-friendly type
            image = vision.types.Image(content=content)
            dealer_hand = detect_hand(image)
            print("Dealer hand: ")
            for card in dealer_hand:
                print(card)
                print("Number of dealer cards: " + str(len(dealer_hand)))
        
        time.sleep(0.1)
        
    return [player_hand, dealer_hand]
    
def main():
    
    #generate a camera object for the takephoto function to
    #work with
    camera = picamera.PiCamera()      
        
    #setup our pygame mixer to play audio in subsequent stages
#    pg.init()
#    pg.mixer.init()  
    while True:
    #indicate that a new hand has been dealt with a cap touch
        if crickit.touch_1.value==1:
            [player_hand, dealer_hand ] = capture_initial_hands(camera)
            for card in player_hand:
                print(card)
            for card in dealer_hand:
                print(card)
            # Keep taking pictures if the correct number of cards isn't detected
'''            while len(player_hand) is not 2 or len(dealer_hand) is not 1:
                takephoto(camera) # Capture a picture

                with open('player_image.jpg', 'rb') as image_file:
                    #read the image file
                    content = image_file.read()
                    #convert the image file to a GCP Vision-friendly type
                    image = vision.types.Image(content=content)
                    player_hand = detect_hand(image)
                    print("Player hand: ")
                    for card in player_hand:
                        print(card)
                    print("Number of player cards: " + str(len(player_hand)))
                    
                with open('dealer_image.jpg', 'rb') as image_file:
                    #read the image file
                    content = image_file.read()
                    #convert the image file to a GCP Vision-friendly type
                    image = vision.types.Image(content=content)
                    dealer_hand = detect_hand(image)
                    print("Dealer hand: ")
                    for card in dealer_hand:
                        print(card)
                    print("Number of dealer cards: " + str(len(dealer_hand)))
 '''           
      
if __name__ == '__main__':
        main()    
