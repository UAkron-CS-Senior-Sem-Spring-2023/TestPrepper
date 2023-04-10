import pygame
import cv2

from gesture_detection import GestureDetection

clock = pygame.time.Clock()

SCREEN = [640, 360]

def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "BGR")

if __name__ == "__main__":
    # Set game screen
    screen = pygame.display.set_mode(SCREEN)

    pygame.init()  # Initialize pygame
    detecter = GestureDetection(0)

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        image = detecter.getImage()

        result = detecter.doesImageContainGesture('Pointing_Up', image)
        if result != False:
            print(result[1][1])

        screen.fill([0,0,0])
        screen.blit(cvimage_to_pygame(image), (0,0))
        pygame.display.update()
        clock.tick(15)
    
    pygame.quit()
    quit()

