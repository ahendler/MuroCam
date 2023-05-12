import os
import cv2
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
from instagram.instagram import Instagram
import shutil
import time
import datetime
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

last_picture = None
last_posted = int(time.time_ns() / 1000000)
times_tried = 0

while True:
    picture_name = cam.take_picture()
    image = cam.get_frame(picture_name)
    now = datetime.datetime.now()
    if det.detect_YOLOv5(image):
        print("Hand detected at " + now.strftime("%Y-%m-%d %H:%M:%S"))
        # save the image with a new name
        cv2.imwrite(picture_name, image)
        # move the file to a new folder (create if it doesn't exist)
        source_path = os.path.abspath(picture_name)
        destination_folder = 'hands'
        shutil.move(source_path, os.path.join(destination_folder, picture_name))
        last_picture = os.path.join(destination_folder, picture_name)
    else:
        times_tried += 1
        if times_tried > 20:
            print("No hand detected after 20 tries "+ now.strftime("%Y-%m-%d %H:%M:%S"))
            times_tried = 0
        #delete picture
        os.rename(picture_name, "image.jpg")
    
    if last_picture is not None:
        if last_posted == 0 or (int(time.time_ns() / 1000000) - last_posted) > 3600000:
            ins.post(last_picture)
            last_posted = int(time.time_ns() / 1000000)
            last_picture = None
            print("Posted at " + now.strftime("%Y-%m-%d %H:%M:%S"))