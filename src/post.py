import os
import cv2
from dotenv import load_dotenv
from instagram.instagram import Instagram
import pickle

load_dotenv()

ins = Instagram(os.getenv('INSTAGRAM_APP_ID'), os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))


r = ins.post("hands/1683859360368.jpg")
print(r)

