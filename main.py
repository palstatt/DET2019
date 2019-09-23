import os

from google.cloud import vision_v1p4beta1 as vision
from time import sleep
import time
import signal
import sys
import re
import socket
from process_image import process_image


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./det_google_cloud.json"

client = vision.ImageAnnotatorClient()

image = 'test_image_hi.jpg'


def detect_hand(image):
    """Takes an image and uses GCV to detect valid cards in the image

    Arguments:
        image {Image} -- a GCV friendly image type

    Returns:
        [str] -- array of cards in hand
    """

    validCards = ['A', 'K', 'Q', 'J', '10',
                  '9', '8', '7', '6', '5', '4', '3', '2']
    hand = []

    context = vision.types.ImageContext(language_hints="en-t-i0-plain")

    response = client.text_detection(
        image=image, image_context=context)
    texts = response.text_annotations

    for text in texts:
        print(text)
        letter = text.description.upper()
        if letter in validCards:
            hand.append(letter)

    return hand


def main():
    global image

    dealer_image, player_image, processed_image = process_image(image)
    with open(player_image, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    dealer_hand = detect_hand(image)
    print("Dealer hand: ")
    for card in dealer_hand:
        print(card)
        print("Number of player cards: " + str(len(dealer_hand)))


if __name__ == '__main__':
    main()
