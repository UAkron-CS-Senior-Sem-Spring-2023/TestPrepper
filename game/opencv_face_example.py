import pygame
import cv2 as cv
import numpy as np

FACE_DETECTOR = cv.FaceDetectorYN.create(
        'face_detection_yunet_2022mar.onnx',
        "",
        (320, 320),
        0.9,
        0.3,
        5000
    )

# Screen settings
SCREEN = [1200, 800]

def cvimage_grayscale(cv_image):
    """Converts a cvimage into grayscale"""
    return cv.cvtColor(cv_image, cv.COLOR_RGB2GRAY)


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1],
                                   "BGR")


def detect_faces(cv_image):
    """Detects faces. Returns list of faces if any and their points"""
    return FACE_DETECTOR.detect(cv_image)


def draw_from_points(cv_image, points):
    """Takes the cv_image and points and draws a rectangle based on the points.
    Also draws points on where it thinks the eyes, nose, and mouth corners are.
    Returns a cv_image."""
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

if __name__ == '__main__':

    # Set game screen
    screen = pygame.display.set_mode(SCREEN)

    pygame.init()  # Initialize pygame

    # Load camera source then start
    cap = cv.VideoCapture(0)

    # Variable to control loop exit
    game_exit = False

    # Get the start time of the game
    start_time = pygame.time.get_ticks()
    now = start_time

    # Main Loop
    while not game_exit:
        # Exit the game if it was told to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        # Get current time and the elapsed time since start
        elapsed = now - start_time
        now = pygame.time.get_ticks()
        
        # If its been more than 16.7 ms, roughly 60 fps
        if elapsed >= 16.7:
            # Get current webcam image
            ret, image = cap.read()
            # Tell the face detector what size image to expect
            FACE_DETECTOR.setInputSize((image.shape[1], image.shape[0]))

            if ret:
                # Get all faces in image
                faces = detect_faces(image)
                # for debug, prints out the faces
                # print(faces)
                # Draws rectangles on the faces, returns the edited image
                image = draw_from_points(image, faces)
                # Blank fill the screen
                screen.fill([0, 0, 0])
                # Load new image on screen
                screen.blit(cvimage_to_pygame(image), (0, 0))
                # Update pygame display
                pygame.display.update()
    # Quit pygame
    pygame.quit()