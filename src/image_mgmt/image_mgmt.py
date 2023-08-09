import os
import shutil
import time
from loguru import logger


class Image_mgmt:
    def __init__(self):
        self.images = {}
        self.hour_timer = int(time.time_ns() / 1000000)
        self.frames_per_hour = 0

    def handle_new_image(self, picture_file, score):
        if score > 0.5:
            self.images[picture_file] = score
            logger.info(f"Image {picture_file} detected with score {score}, highest score is {self.get_high_score()}")

            # move the file to a new folder (create if it doesn't exist)
            source_path = os.path.abspath(picture_file)
            destination_folder = os.getenv('DETECTED_IMAGE_PATH')
            shutil.move(source_path, os.path.join(destination_folder, picture_file))
        else:
            #delete picture
            os.rename(picture_file, "last_frame.jpg")

        self.frames_per_hour += 1
        if  (int(time.time_ns() / 1000000) - self.hour_timer) > 3600000:
            logger.info(f"{self.frames_per_hour} frames analised in the last hour")
            logger.info(f" {len(self.images)} images in the queue")
            self.frames_per_hour = 0
            self.hour_timer = int(time.time_ns() / 1000000)

        

    def get_high_score(self):
        if len(self.images) > 0:
            return max(self.images, key=self.images.get)
        return None
        
    def handle_posted_image(self, picture_file):
        self.images.pop(picture_file, None)
        shutil.copy(picture_file, os.path.join(os.getenv('POSTED_IMAGE_PATH'), os.path.basename(picture_file)))
        self.images = {}



