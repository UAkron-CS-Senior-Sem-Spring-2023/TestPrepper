import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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

            cv.imshow('img', image)
            cv.waitKey(1)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(image))
            gesture_recognition_result = recognizer.recognize_for_video(mp_image, mp.Timestamp.from_seconds(time.time()).microseconds())
            # print(gesture_recognition_result)
            # print(gesture_recognition_result.gestures)
            if len(gesture_recognition_result.gestures) > 0:
                for gesture in gesture_recognition_result.gestures:
                    # print(gesture[0])
                    # print(gesture[0].category_name)
                    if gesture[0].category_name == 'Pointing_Up':
                        print("You're pointing up! at ")
                        # annotated_image = mp_drawing.draw_landmarks(mp_image.numpy_view(), gesture_recognition_result)
                        
