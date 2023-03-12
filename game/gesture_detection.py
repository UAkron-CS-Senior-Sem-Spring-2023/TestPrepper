import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.python.solutions.drawing_styles import HandLandmark

import numpy as np
import cv2 as cv

import time

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL = 'gesture_recognizer.task'
MODEL_CONTENTS = open(MODEL, 'rb').read()

def main():
    pass

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    # Create a gesture recognizer instance with the video mode:
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=MODEL_CONTENTS),
        running_mode=VisionRunningMode.VIDEO
    )
    mp_drawing = mp.solutions.drawing_utils
    with GestureRecognizer.create_from_options(options) as recognizer:
        while True:
            ret, image = cap.read()
            if not ret:
                exit(-1)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(image))
            gesture_recognition_result = recognizer.recognize_for_video(mp_image, mp.Timestamp.from_seconds(time.time()).microseconds())
            if len(gesture_recognition_result.gestures) > 0:
                for i in range(len(gesture_recognition_result.gestures)):
                    if gesture_recognition_result.gestures[i][0].category_name == 'Pointing_Up':
                        print("You're pointing up!")
                        for mark in gesture_recognition_result.hand_landmarks[0]:
                            x = int(mark.x * image.shape[1])
                            y = int(mark.y * image.shape[0])
                            # Annotate landmarks
                            cv.circle(image, (x, y), 5, (0, 255, 0), -1)

            cv.imshow('img', image)
            key = cv.waitKey(1)
            if key == ord('q'):
                exit(1)
                        
