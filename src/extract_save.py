import os
import cv2
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
import shutil

load_dotenv()

cam = Camera(os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'), os.getenv('CAMERA_IP'))
det = Detection()

while True:
    picture_name = cam.take_picture()
    image = cam.get_frame(picture_name)
    if det.detect_split(image):
        print("Hand detected")
        # save the image with a new name
        cv2.imwrite(picture_name, image)
        # move the file to a new folder (create if it doesn't exist)
        source_path = os.path.abspath(picture_name)
        destination_folder = 'hands'
        shutil.move(source_path, os.path.join(destination_folder, picture_name))
    else:
        print("No hand detected")
        #delete picture
        os.rename(picture_name, "image.jpg")
