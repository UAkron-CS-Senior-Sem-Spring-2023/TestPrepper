import pygame
import cv2
import numpy as np

from gesture_detection import GestureDetection, drawMarksOnImage, getXandYCoords

clock = pygame.time.Clock()
pygame.init()  # Initialize pygame

WIDTH = 600
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
SCREEN = [WIDTH, HEIGHT]

def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")

if __name__ == "__main__":
    # Set game screen
    screen = pygame.display.set_mode(SCREEN)

    detecter = GestureDetection(0)

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        image = detecter.getImage()

        result = detecter.doesImageContainGesture('Open_Palm', image)

        image = np.zeros([image.shape[0],image.shape[1],3],dtype=np.uint8)
        image.fill(255)

        screen.fill([0,0,0])
        screen.blit(cvimage_to_pygame(image), (0,0))
        
        if result != False:
            x, y = getXandYCoords(image.shape[1], image.shape[0], result[1])
            image = drawMarksOnImage(image, x, y, result[1], "You're pointing up At: y=")

        pygame.display.update()
        clock.tick(15)
    
    pygame.quit()
    quit()

