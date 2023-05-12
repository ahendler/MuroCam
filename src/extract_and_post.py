import os
import sys
import cv2
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
from instagram.instagram import Instagram
import shutil
import time
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

load_dotenv()

cam = Camera(os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'), os.getenv('CAMERA_IP'))
det = Detection()
ins = Instagram(os.getenv('INSTAGRAM_APP_ID'), os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))

last_picture = None
last_posted = int(time.time_ns() / 1000000)
frames_since_last_detection = 0
last_detection = int(time.time_ns() / 1000000)
frames_per_hour = 0
hour_timer = int(time.time_ns() / 1000000)

logger.info("Starting image capture")
while True:
    picture_name = cam.take_picture()
    image = cam.get_frame(picture_name)
    frames_per_hour += 1
    if det.detect_YOLOv5(image):
        logger.info(f"{frames_since_last_detection} frames analised and {(int(time.time_ns() / 1000000) - int(last_detection))/60000} minutes elapsed since last detection/program start")
        logger.info("Person detected")
        last_detection = int(time.time_ns() / 1000000)
        frames_since_last_detection = 0

        # move the file to a new folder (create if it doesn't exist)
        source_path = os.path.abspath(picture_name)
        destination_folder = os.getenv('DETECTED_IMAGE_PATH')
        shutil.move(source_path, os.path.join(destination_folder, picture_name))
        last_picture = os.path.join(destination_folder, picture_name)
    else:
        frames_since_last_detection += 1
        if  (int(time.time_ns() / 1000000) - hour_timer) > 3600000:
            logger.info(f"{frames_per_hour} frames analised in the last hour")
            frames_per_hour = 0
            hour_timer = int(time.time_ns() / 1000000)
        #delete picture
        os.rename(picture_name, "last_frame.jpg")
    
    if last_picture is not None:
        if last_posted == 0 or (int(time.time_ns() / 1000000) - last_posted) > 3600000:
            ins.post(last_picture)
            last_posted = int(time.time_ns() / 1000000)
            logger.info(f"Image {last_picture} posted")
            shutil.copy(last_picture, os.path.join(os.getenv('POSTED_IMAGE_PATH'), os.path.basename(last_picture)))
            last_picture = None