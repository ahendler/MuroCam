import os
import sys
from dotenv import load_dotenv
from camera.camera import Camera
from detection.detection import Detection
from instagram.instagram import Instagram
from image_mgmt.image_mgmt import Image_mgmt
from loguru import logger
import time

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

load_dotenv()

cam = Camera(os.getenv('CAMERA_USERNAME'), os.getenv('CAMERA_PASSWORD'), os.getenv('CAMERA_IP'))
ins = Instagram(os.getenv('INSTAGRAM_APP_ID'), os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
det = Detection()
img_mgmt = Image_mgmt()

last_posted = int(time.time_ns() / 1000000)

logger.info("Starting image capture")
while True:
    picture_file = cam.take_picture()
    image = cam.get_frame(picture_file)
    score = det.detect_YOLOv5(image)
    img_mgmt.handle_new_image(picture_file, score)
    if (int(time.time_ns() / 1000000) - last_posted) > 3600000:
        best_image = img_mgmt.get_highest_score_image()
        if best_image is not None:
            ins.post(best_image)
            img_mgmt.handle_posted_image(best_image)
            last_posted = int(time.time_ns() / 1000000)