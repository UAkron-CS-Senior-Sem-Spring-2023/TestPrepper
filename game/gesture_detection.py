import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.python.solutions.drawing_styles import HandLandmark

import numpy as np
import cv2 as cv
import os

import time

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

FONT_COLOR = (0,0,0)
FONT = cv.FONT_HERSHEY_COMPLEX
FONT_SCALE = 0.5
THICKNESS = 1

class GestureDetection():
    def __init__(
            self,
            camera_num:int,
            gesture_path:str
        ):
        
        self.cam = cv.VideoCapture(int(camera_num))
        model_contents = open(gesture_path, 'rb').read()
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_buffer=model_contents),
            running_mode=VisionRunningMode.VIDEO
        )
        self.recognizer = GestureRecognizer.create_from_options(options)
        self.drawing = mp.solutions.drawing_utils

    def __del__(self):
        del self.recognizer

    def getImage(self):
        ret, image = self.cam.read()
        assert(ret)
        return image

    def doesImageContainGesture(
        self,
        gesture: str,
        image
    ):
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(image))
        gesture_recognition_result = self.recognizer.recognize_for_video(mp_image, mp.Timestamp.from_seconds(time.time()).microseconds())

        if len(gesture_recognition_result.gestures) > 0:
            for i in range(len(gesture_recognition_result.gestures)):
                if gesture_recognition_result.gestures[i][0].category_name == gesture:
                    landmarks = gesture_recognition_result.hand_landmarks[0]
                    return (image, landmarks)
        return False
    
def drawMarksOnImage(image, top_finger_x, top_finger_y, landmarks, text):
    for mark in landmarks:
        x = int(mark.x * image.shape[1])
        y = int(mark.y * image.shape[0])
        # Annotate landmarks
        cv.circle(image, (x, y), 5, (0, 255, 0), -1)

    pointing_len = cv.getTextSize(text, FONT, FONT_SCALE, 1)
    cv.putText(image, text, (top_finger_x, top_finger_y), FONT, FONT_SCALE, FONT_COLOR, THICKNESS, cv.LINE_AA)
    cv.putText(image, str(top_finger_y), (top_finger_x+pointing_len[0][0], top_finger_y), FONT, FONT_SCALE, FONT_COLOR, THICKNESS, cv.LINE_AA)

    return image

def getXandYCoords(width, height, landmarks):
    top_finger_y = 10000
    top_finger_x = -1

    for mark in landmarks:
        x = int(mark.x * width)
        y = int(mark.y * height)

        if top_finger_y > y:
            top_finger_y = y
            top_finger_x = x

    return (top_finger_x, top_finger_y)


# if __name__ == "__main__":
#     cap = cv.VideoCapture(0)
#     # Create a gesture recognizer instance with the video mode:
#     options = GestureRecognizerOptions(
#         base_options=BaseOptions(model_asset_buffer=MODEL_CONTENTS),
#         running_mode=VisionRunningMode.VIDEO
#     )
#     mp_drawing = mp.solutions.drawing_utils
#     with GestureRecognizer.create_from_options(options) as recognizer:
#         while True:
#             ret, image = cap.read()
#             if not ret:
#                 exit(-1)

#             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(image))
#             gesture_recognition_result = recognizer.recognize_for_video(mp_image, mp.Timestamp.from_seconds(time.time()).microseconds())

#             top_finger_x = -1
#             top_finger_y = 10000
#             if len(gesture_recognition_result.gestures) > 0:
#                 for i in range(len(gesture_recognition_result.gestures)):
#                     if gesture_recognition_result.gestures[i][0].category_name == 'Pointing_Up':
#                         # print("You're pointing up!")
#                         for mark in gesture_recognition_result.hand_landmarks[0]:
#                             x = int(mark.x * image.shape[1])
#                             y = int(mark.y * image.shape[0])
#                             # Annotate landmarks
#                             cv.circle(image, (x, y), 5, (0, 255, 0), -1)

#                             if top_finger_y > y:
#                                 top_finger_y = y
#                                 top_finger_x = x

#                         pointing_len = cv.getTextSize(POINTING_UP_QUOTE, FONT, FONT_SCALE, 1)
#                         cv.putText(image, POINTING_UP_QUOTE, (top_finger_x, top_finger_y), FONT, FONT_SCALE, FONT_COLOR, THICKNESS, cv.LINE_AA)
#                         cv.putText(image, str(top_finger_y), (top_finger_x+pointing_len[0][0], top_finger_y), FONT, FONT_SCALE, FONT_COLOR, THICKNESS, cv.LINE_AA)

#             cv.imshow('img', image)
#             key = cv.waitKey(1)
#             if key == ord('q'):
#                 exit(1)
                        
