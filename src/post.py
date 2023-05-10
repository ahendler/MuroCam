import os
import cv2
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
from instagram.instagram import Instagram
import pickle

load_dotenv()

cam = Camera(os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'), os.getenv('CAMERA_IP'))
det = Detection()

# Check if the instagram_instance.pickle file exists
if os.path.exists('instagram_instance.pickle'):
    print("Loading Instagram instance from file")
    with open('instagram_instance.pickle', 'rb') as f:
        ins = pickle.load(f)
else:
    # Create a new instance of the Instagram class
    print("Creating new Instagram instance")
    ins = Instagram(os.getenv('INSTAGRAM_APP_ID'), os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
    # Save the instance to a file
    with open('instagram_instance.pickle', 'wb') as f:
        pickle.dump(ins, f)

r = ins.post("hands/1683746618169.jpg")
print(r)

