import mediapipe as mp
import cv2

class Detection:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.01)

    def detect(self, image):
        # Convert the image from BGR to RGB and process it with MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        # Check if a hand was detected in the image
        if (results.multi_hand_landmarks and results.multi_handedness and results.multi_handedness[0].classification[0].score > 0.1):
            print("Hand detected")
            return True
        else:
            return False