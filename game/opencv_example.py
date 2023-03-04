from pygame import camera
import pygame
import time
import cv2 as cv
import os
import numpy as np

# from yunet import YuNet

# Recognition
# HAAR_PATH = "/usr/share/opencv/haarcascades/"

FACE_CASCADE = cv.CascadeClassifier('haarcascade_frontalcatface.xml')
FACE_DETECTOR = cv.FaceDetectorYN.create(
        'face_detection_yunet_2022mar.onnx',
        "",
        (320, 320),
        0.9,
        0.3,
        5000
    )

# # Face
# # FACE_HAAR = os.path.join(HAAR_PATH, "haarcascade_frontalface_default.xml")
# FACE_HAAR = cv.Load(FACE_HAAR)

# # Eye
# EYE_HAAR = os.path.join(HAAR_PATH, "haarcascade_mcs_righteye.xml")
# EYE_HAAR = cv.Load(EYE_HAAR)

# # Nose
# NOSE_HAAR = os.path.join(HAAR_PATH, "haarcascade_mcs_nose.xml")
# NOSE_HAAR = cv.Load(NOSE_HAAR)

# # Mouth
# MOUTH_HAAR = os.path.join(HAAR_PATH, "haarcascade_mcs_mouth.xml")
# MOUTH_HAAR = cv.Load(MOUTH_HAAR)

# Screen settings
SCREEN = [640, 360]


# def surface_to_string(surface):
#     """Convert a pygame surface into string"""
#     return pygame.image.tostring(surface, 'RGB')


# def pygame_to_cvimage(surface):
#     """Convert a pygame surface into a cv image"""
#     cv_image = cv.CreateImageHeader(surface.get_size(), cv.IPL_DEPTH_8U, 3)
#     image_string = surface_to_string(surface)
#     cv.SetData(cv_image, image_string)
#     return pygame.image.frombuffer(image.tostring(), image.shape[:2],
#                                    "RGB")


def cvimage_grayscale(cv_image):
    """Converts a cvimage into grayscale"""
    return cv.cvtColor(cv_image, cv.COLOR_RGB2GRAY)


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1],
                                   "RGB")


def detect_faces(cv_image):
    """Detects faces based on haar. Returns points"""
    # return FACE_CASCADE.detectMultiScale(cvimage_grayscale(cv_image))
    return FACE_DETECTOR.detect(cv_image)
    # return cv.HaarDetectObjects(cvimage_grayscale(cv_image), FACE_HAAR,
    #                             storage)


# def detect_eyes(cv_image, storage):
#     """Detects eyes based on haar. Returns points"""
#     return cv.HaarDetectObjects(cvimage_grayscale(cv_image), EYE_HAAR,
#                                 storage)


# def detect_nose(cv_image, storage):
#     """Detects nose based on haar. Returns ponts"""
#     return cv.HaarDetectObjects(cvimage_grayscale(cv_image), NOSE_HAAR,
#                                 storage)


# def detect_mouth(cv_image, storage):
#     """Detects mouth based on haar. Returns points"""
#     return cv.HaarDetectObjects(cvimage_grayscale(cv_image), MOUTH_HAAR,
#                                 storage)


def draw_from_points(cv_image, points):
    """Takes the cv_image and points and draws a rectangle based on the points.
    Returns a cv_image."""
    # for (x, y, w, h) in points:
    #     cv.rectangle(cv_image, (x, y), (x + w, y + h), 255)
    # return cv_image
    if points[1] is not None:
        for idx, face in enumerate(points[1]):
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))

            coords = face[:-1].astype(np.int32)
            cv.rectangle(cv_image, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), 2)
            cv.circle(cv_image, (coords[4], coords[5]), 2, (255, 0, 0), 2)
            cv.circle(cv_image, (coords[6], coords[7]), 2, (0, 0, 255), 2)
            cv.circle(cv_image, (coords[8], coords[9]), 2, (0, 255, 0), 2)
            cv.circle(cv_image, (coords[10], coords[11]), 2, (255, 0, 255), 2)
            cv.circle(cv_image, (coords[12], coords[13]), 2, (0, 255, 255), 2)
    
    return cv_image


# if __name__ == '__main__':

#     # Set game screen
#     screen = pygame.display.set_mode(SCREEN)

#     pygame.init()  # Initialize pygame
#     camera.init()  # Initialize camera

#     # Load camera source then start
#     cam = camera.Camera('/dev/video0', SCREEN)
#     cam.start()

#     while 1:  # Ze loop

#         time.sleep(1 / 120)  # 60 frames per second

#         image = cam.get_image()  # Get current webcam image

#         cv_image = pygame_to_cvimage(image)  # Create cv image from pygame image

#         # Detect faces then draw points on image
#         # FIXME: Current bottleneck. Image has to be Grayscale to make it faster.
#         #        One solution would be to use opencv instead of pygame for
#         #        capturing images.
#         # storage = cv.CreateMemStorage(-1)  # Create storage
#         #points = detect_eyes(cv_image, storage) + \
#         #        detect_nose(cv_image, storage) + \
#         #        detect_mouth(cv_image, storage)
#         points = detect_faces(cv_image)  # Get points of faces.
#         cv_image = draw_from_points(cv_image, points)  # Draw points

#         screen.fill([0, 0, 0])  # Blank fill the screen

#         screen.blit(cvimage_to_pygame(cv_image), (0, 0))  # Load new image on screen

#         pygame.display.update()  # Update pygame display

if __name__ == '__main__':

    # Set game screen
    screen = pygame.display.set_mode(SCREEN)

    pygame.init()  # Initialize pygame
    # camera.init()  # Initialize camera

    # Load camera source then start
    cap = cv.VideoCapture(0)
    # cam = camera.Camera('/dev/video0', SCREEN)
    # cam.start()

    game_exit = False

    start_time = pygame.time.get_ticks()

    while not game_exit:  # Ze loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        # time.sleep(1 / 120)  # 60 frames per second
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        if elapsed > 16.7:
            ret, image = cap.read()  # Get current webcam image

            FACE_DETECTOR.setInputSize((image.shape[1], image.shape[0]))

            if ret:
                # cv_image = pygame_to_cvimage(image)  # Create cv image from pygame image

                # Detect faces then draw points on image
                # FIXME: Current bottleneck. Image has to be Grayscale to make it faster.
                #        One solution would be to use opencv instead of pygame for
                #        capturing images.
                # storage = cv.CreateMemStorage(-1)  # Create storage
                #points = detect_eyes(cv_image, storage) + \
                #        detect_nose(cv_image, storage) + \
                #        detect_mouth(cv_image, storage)
                faces = detect_faces(image)  # Get points of faces.
                print(faces)
                image = draw_from_points(image, faces)  # Draw points

                screen.fill([0, 0, 0])  # Blank fill the screen

                screen.blit(cvimage_to_pygame(image), (0, 0))  # Load new image on screen

                pygame.display.update()  # Update pygame display

    pygame.quit()