import pygame
import cv2
import numpy as np
import random

from gesture_detection import GestureDetection, drawMarksOnImage, getXandYCoords

WIDTH = 600
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
SCREEN = [WIDTH, HEIGHT]

clock = pygame.time.Clock()
pygame.init()  # Initialize pygame
screen = pygame.display.set_mode(SCREEN)
detecter = GestureDetection(0)

TITLE_OFFSET = 20
QUESTION_OFFSET = 45
CV_SCREEN_OFFSET = 60
FOOTER_OFFSET = 550
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
FONT = pygame.font.Font('freesansbold.ttf', 14)

ANSWER_WIDTH = 100
ANSWER_HEIGHT = 50

def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")

def drawMainScreen():
    pass

def drawTitle(chapterName):
    text = TITLE_FONT.render(chapterName, True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH/2, TITLE_OFFSET))
    screen.blit(text, rect)

def drawFooter():
    pass

def drawQuestion(question):
    text = FONT.render(question, True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH/2, QUESTION_OFFSET))
    screen.blit(text, rect)

def drawAnswer(answer, answer_num):
    usable_height = HEIGHT-CV_SCREEN_OFFSET
    text = FONT.render(answer, True, BLACK, WHITE)
    if answer_num == 0 or answer_num == 2:
        if answer_num == 0:
            center = (WIDTH/4, CV_SCREEN_OFFSET+(usable_height/4))
        else:
            center = (WIDTH/4, CV_SCREEN_OFFSET+(3*usable_height/4))
    elif answer_num == 1 or answer_num == 3:
        if answer_num == 1:
            center = (3*WIDTH/4, CV_SCREEN_OFFSET+(usable_height/4))
        else:
            center = (3*WIDTH/4, CV_SCREEN_OFFSET+(3*usable_height/4))

    bordered_rect = pygame.draw.rect(
        screen,
        BLACK,
        (center[0]-(ANSWER_WIDTH/2), center[1]-(ANSWER_HEIGHT/2), ANSWER_WIDTH, ANSWER_HEIGHT),
        5
        )
    rect = text.get_rect(center=center)
    screen.blit(text, rect)

def quiz(question, answer0, answer1, answer2, answer3):
    drawQuestion(question)
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                exit(-1)

        image = detecter.getImage()

        result = detecter.doesImageContainGesture('Open_Palm', image)

        # image = np.zeros([image.shape[0],image.shape[1],3],dtype=np.uint8)
        # image.fill(255)

        # screen.fill([0,0,0])
        # screen.blit(cvimage_to_pygame(image), (0,50))
        pygame.draw.rect(screen, WHITE, (0,CV_SCREEN_OFFSET,WIDTH,HEIGHT))
        
        drawAnswer(answer0, 0)
        drawAnswer(answer1, 1)
        drawAnswer(answer2, 2)
        drawAnswer(answer3, 3)

        if result != False:
            x, y = getXandYCoords(image.shape[1], image.shape[0], result[1])
            pygame.draw.circle(screen, BLACK, (image.shape[1]-x,y+CV_SCREEN_OFFSET), radius=10)

        pygame.display.update()
        clock.tick(5)

def game(chapterName, termList, definitionList):
    screen.fill(WHITE)
    drawTitle(chapterName)

    array=list(range(0,len(termList) + 0))
    random.shuffle(array)
    for x in array:
        choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
        while len(set(choicePicker)) != len(choicePicker):
                choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
        random.shuffle(choicePicker)

        questionChoice = termList[x]
        print("{}".format(definitionList[x]) + "?")
        print("A.{}".format(choicePicker[0]))
        print("B.{}".format(choicePicker[1]))
        print("C.{}".format(choicePicker[2]))
        print("D.{}".format(choicePicker[3]))
        quiz(
            definitionList[x],
            choicePicker[0],
            choicePicker[1],
            choicePicker[2],
            choicePicker[3],
        )

if __name__ == "__main__":
    game(
        'ComputerParts',
        ['CPU', 'RAM', 'SSD', 'Motherboard', 'Case', 'GPU'],
        ['Processes all the instructions fed in by RAM', 'Volatile storage for quick access fed in by SSD', 'Large, slow storage to hold', 'Electronic housing for all the components', 'Physical housing for all the components', 'Powers what you see on the display']
        )
    input()
    exit(0)
    

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        image = detecter.getImage()

        result = detecter.doesImageContainGesture('Open_Palm', image)

        # image = np.zeros([image.shape[0],image.shape[1],3],dtype=np.uint8)
        # image.fill(255)

        # screen.fill([0,0,0])
        # screen.blit(cvimage_to_pygame(image), (0,50))
        pygame.draw.rect(screen, (255,255,255), (0,0,WIDTH,HEIGHT))
        
        if result != False:
            x, y = getXandYCoords(image.shape[1], image.shape[0], result[1])
            pygame.draw.circle(screen, (0,0,0), (image.shape[1]-x,y+CV_SCREEN_OFFSET), radius=10)

        pygame.display.update()
        clock.tick(5)
    
    pygame.quit()
    quit()

