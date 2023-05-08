import os
import cv2
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
import shutil

load_dotenv()

cam = Camera(os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'), os.getenv('CAMERA_IP'))
detection = Detection()

i = 0
while True:
    cam.take_picture()
    image = cam.get_frame()
    if detection.detect(image):
        print("Hand detected")
        # save the image with a new name
        new_filename = f'hand_{i}.jpg'
        cv2.imwrite(new_filename, image)
        i += 1       

        # move the file to a new folder
        source_path = os.path.abspath(new_filename)
        destination_folder = 'hands'
        shutil.move(source_path, os.path.join(destination_folder, new_filename))
    else:
        print("No hand detected")