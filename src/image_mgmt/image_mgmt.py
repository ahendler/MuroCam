import os
import shutil
import time
from loguru import logger


class Image_mgmt:
    def __init__(self):
        self.images = {}
        self.hour_timer = int(time.time_ns() / 1000000)
        self.frames_per_hour = 0

        # create image folders if they don't exist
        if not os.path.exists(os.getenv('DETECTED_IMAGE_PATH')):
            os.makedirs(os.getenv('DETECTED_IMAGE_PATH'))
            logger.info(f"Created folder {os.getenv('DETECTED_IMAGE_PATH')}")
        if not os.path.exists(os.getenv('POSTED_IMAGE_PATH')):
            os.makedirs(os.getenv('POSTED_IMAGE_PATH'))
            logger.info(f"Created folder {os.getenv('POSTED_IMAGE_PATH')}")

    def handle_new_image(self, picture_file, score):
        if score > 1:
            if score > self.get_highest_score():
                logger.info(f"New highest score {score}, image {picture_file}")
            self.images[picture_file] = score
            source_path = os.path.abspath(picture_file)
            destination_folder = os.getenv('DETECTED_IMAGE_PATH')
            shutil.move(source_path, os.path.join(destination_folder, picture_file))
        else:
            #delete picture
            os.rename(picture_file, "last_frame.jpg")

        self.frames_per_hour += 1
        if  (int(time.time_ns() / 1000000) - self.hour_timer) > 3600000:
            logger.info(f"{self.frames_per_hour} frames analised in the last hour")
            self.frames_per_hour = 0
            self.hour_timer = int(time.time_ns() / 1000000)

        

    def get_highest_score_image(self):
        if len(self.images) > 0:
            return max(self.images, key=self.images.get)
        return None
    
    def get_highest_score(self):
        if len(self.images) > 0:
            return self.images[self.get_highest_score_image()]
        return 0
        
    def handle_posted_image(self, picture_file):
        self.images.pop(picture_file, None)
        
        picture_path = os.path.join(os.getenv('DETECTED_IMAGE_PATH'), picture_file)
        shutil.copy(picture_path, os.path.join(os.getenv('POSTED_IMAGE_PATH'), os.path.basename(picture_file)))
        self.images = {}



