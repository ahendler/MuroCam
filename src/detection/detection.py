from loguru import logger
import torch
import sys
import os

class Detection:
    def __init__(self):
        # Supressing yolov5 presentation
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def detect_YOLOv5(self, image):
        # Inference
        results = self.model(image)

        # Results
        #results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

        df = results.pandas().xyxy[0]
        # Filter rows with name 'person' and confidence > 0.65
        person_df = df[(df['name'] == 'person') & (df['confidence'] > 0.65)].copy()
        if not person_df.empty:
            person_df.loc[:, 'area'] = (person_df['xmax'] - person_df['xmin']) * (person_df['ymax'] - person_df['ymin'])
            person_df.loc[:, 'score'] = person_df['area'] * person_df['confidence']
            total_score = person_df['score'].sum()
            return int(total_score/100)
        return 0
