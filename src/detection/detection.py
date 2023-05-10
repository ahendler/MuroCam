import mediapipe as mp
import cv2

class Detection:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.05)

    def detect(self, image):
        # Convert the image from BGR to RGB and process it with MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        # Check if a hand was detected in the image
        if (results.multi_hand_landmarks and results.multi_handedness and results.multi_handedness[0].classification[0].score > 0.1):
            return True
        else:
            return False
        
    def detect_split(self, image):
        height, width, _ = image.shape
        # Define number of regions
        n_regions = 6

        # Calculate width and height of each region
        region_width = width // 2
        region_height = height // 2 + height // 4
        height_start = height // 2 - height // 4

        # Split image into regions
        regions = []
        region = image[0:region_height, 0:region_width, :]
        regions.append(region)
        region = image[0:region_height, width//4:width//4 + region_width, :]
        regions.append(region)
        region = image[0:region_height, width//2: -1, :]
        regions.append(region)
        region = image[height_start:-1, 0:region_width, :]
        regions.append(region)
        region = image[height_start:-1, width//4:width//4 + region_width, :]
        regions.append(region)
        region = image[height_start:-1, width//2:-1, :]
        regions.append(region)
        for i in range(n_regions):
            if self.detect(regions[i]):
                return True

