import pygame
import cv2
import numpy as np
import random

from .gesture_detection import GestureDetection, drawMarksOnImage, getXandYCoords

WIDTH = 600
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN = [WIDTH, HEIGHT]

clock = pygame.time.Clock()
pygame.init()  # Initialize pygame
screen = None
detecter = None

TITLE_OFFSET = 20
QUESTION_OFFSET = 45
CV_SCREEN_OFFSET = 60
FOOTER_OFFSET = 550
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
FONT = pygame.font.Font('freesansbold.ttf', 14)

ANSWER_WIDTH = 100
ANSWER_HEIGHT = 50
ANSWER_USABLE_SPACE = HEIGHT-CV_SCREEN_OFFSET

LEFT_ANSWER_START = (WIDTH/4)-(ANSWER_WIDTH/2)
LEFT_ANSWER_END = LEFT_ANSWER_START+ANSWER_WIDTH

RIGHT_ANSWER_START = (3*WIDTH/4)-(ANSWER_WIDTH/2)
RIGHT_ANSWER_END = RIGHT_ANSWER_START+ANSWER_WIDTH

TOP_ANSWER_START = CV_SCREEN_OFFSET+(ANSWER_USABLE_SPACE/4)-(ANSWER_HEIGHT/2)
TOP_ANSWER_END = TOP_ANSWER_START+ANSWER_HEIGHT

BOTTOM_ANSWER_START = CV_SCREEN_OFFSET+(3*ANSWER_USABLE_SPACE/4)-(ANSWER_HEIGHT/2)
BOTTOM_ANSWER_END = BOTTOM_ANSWER_START+ANSWER_HEIGHT

def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")

def setup(gesture_path):
    global detecter
    global screen
    detecter = GestureDetection(0, gesture_path)
    screen = pygame.display.set_mode(SCREEN)

def drawTitle(chapterName):
    text = TITLE_FONT.render(chapterName, True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH/2, TITLE_OFFSET))
    screen.blit(text, rect)

def drawScore(score, total_questions):
    text = TITLE_FONT.render("{}/{}".format(score, total_questions), True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH-100, TITLE_OFFSET))
    screen.blit(text, rect)

def drawQuestion(question):
    text = FONT.render(question, True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH/2, QUESTION_OFFSET))
    screen.blit(text, rect)

def drawAnswer(answer, answer_num):
    text = FONT.render(answer, True, BLACK, WHITE)
    if answer_num == 0:
        text_center = (LEFT_ANSWER_START+(ANSWER_WIDTH/2), TOP_ANSWER_START+(ANSWER_HEIGHT/2))
        border_start = (LEFT_ANSWER_START, TOP_ANSWER_START)
    elif answer_num == 1:
        text_center = (LEFT_ANSWER_START+(ANSWER_WIDTH/2), BOTTOM_ANSWER_START+(ANSWER_HEIGHT/2))
        border_start = (LEFT_ANSWER_START, BOTTOM_ANSWER_START)
    elif answer_num == 2:
        text_center = (RIGHT_ANSWER_START+(ANSWER_WIDTH/2), TOP_ANSWER_START+(ANSWER_HEIGHT/2))
        border_start = (RIGHT_ANSWER_START, TOP_ANSWER_START)
    else:
        text_center = (RIGHT_ANSWER_START+(ANSWER_WIDTH/2), BOTTOM_ANSWER_START+(ANSWER_HEIGHT/2))
        border_start = (RIGHT_ANSWER_START, BOTTOM_ANSWER_START)

    bordered_rect = pygame.draw.rect(
        screen,
        BLACK,
        (border_start[0], border_start[1], ANSWER_WIDTH, ANSWER_HEIGHT),
        5
        )
    rect = text.get_rect(center=text_center)
    screen.blit(text, rect)

def checkIfAnswerSelected(x, y):
    if x >= LEFT_ANSWER_START and x <= LEFT_ANSWER_END:
        if y >= TOP_ANSWER_START and y <= TOP_ANSWER_END:
            return 0
        if y >= BOTTOM_ANSWER_START and y <= BOTTOM_ANSWER_END:
            return 1
    if x >= RIGHT_ANSWER_START and x <= RIGHT_ANSWER_END:
        if y >= TOP_ANSWER_START and y <= TOP_ANSWER_END:
            return 2
        if y >= BOTTOM_ANSWER_START and y <= BOTTOM_ANSWER_END:
            return 3
    return -1

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

        pygame.draw.rect(screen, WHITE, (0,CV_SCREEN_OFFSET,WIDTH,HEIGHT))
        
        drawAnswer(answer0, 0)
        drawAnswer(answer1, 1)
        drawAnswer(answer2, 2)
        drawAnswer(answer3, 3)

        if result != False:
            x, y = getXandYCoords(image.shape[1], image.shape[0], result[1])
            pygame.draw.circle(screen, BLACK, (image.shape[1]-x,y+CV_SCREEN_OFFSET), radius=10)
            answer = checkIfAnswerSelected(image.shape[1]-x, y+CV_SCREEN_OFFSET)
            if answer >= 0:
                return answer

        pygame.display.update()
        clock.tick(5)

def resultsScreen(title, definition, correct_answer, user_answer):
    screen.fill(WHITE)
    drawTitle(title)
    drawQuestion(definition)

    if correct_answer == user_answer:
        text = TITLE_FONT.render("Correct!", True, GREEN, WHITE)
        rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, rect)
    else:
        text = TITLE_FONT.render("Incorrect!", True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)))
        screen.blit(text, rect)
        text = TITLE_FONT.render("You answered: " + user_answer, True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+50))
        screen.blit(text, rect)
        text = TITLE_FONT.render("Correct answer: " + correct_answer, True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+100))
        screen.blit(text, rect)

    pygame.display.update()

def finalResultsScreen(title, score, total_questions):
    drawTitle(title)
    text = TITLE_FONT.render("{}/{}".format(score, total_questions), True, BLACK, WHITE)
    rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)))
    screen.blit(text, rect)

    if score/total_questions < 0.3:
        text = TITLE_FONT.render("You might want to", True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+50))
        screen.blit(text, rect)
        text = TITLE_FONT.render("practice some more", True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+100))
        screen.blit(text, rect)
    elif score/total_questions < 0.6:
        text = TITLE_FONT.render("You're alright but could", True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+50))
        screen.blit(text, rect)
        text = TITLE_FONT.render("use some more practice", True, RED, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+100))
        screen.blit(text, rect)
    elif score/total_questions < 0.8:
        text = TITLE_FONT.render("You've done well!", True, BLACK, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+50))
        screen.blit(text, rect)
    else:
        text = TITLE_FONT.render("Good job!", True, GREEN, WHITE)
        rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+50))
        screen.blit(text, rect)
    pygame.display.update()
    pygame.time.delay(4000)

def game(chapterName, termList, definitionList, dbcursor=None):
    screen.fill(WHITE)
    drawTitle(chapterName)

    array=list(range(0,len(termList) + 0))
    random.shuffle(array)
    num_questions = len(termList)
    score = 0
    for x in array:
        choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
        while len(set(choicePicker)) != len(choicePicker):
                choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
        random.shuffle(choicePicker)

        answer = quiz(
            definitionList[x],
            choicePicker[0],
            choicePicker[1],
            choicePicker[2],
            choicePicker[3],
        )
        # Process the answer
        if termList[x] == choicePicker[answer]:
            if dbcursor is not None:
                dbcursor.execute("UPDATE score SET correct = correct + 1 WHERE Term = '" + choicePicker[answer] + "';")
            score += 1
        pygame.time.delay(500)
        # Tell the user if it was right
        resultsScreen(chapterName, definitionList[x], termList[x], choicePicker[answer])
        screen.fill(WHITE)
        pygame.time.delay(2000)
        drawTitle(chapterName)
        drawScore(score, num_questions)

    finalResultsScreen(chapterName, score, num_questions)
    pygame.quit()
    return score
        
if __name__ == "__main__":
    # If calling from the repo root dir
    setup("./game/gesture_recognizer.task")
    # If calling from the game dir
    # setup("gesture_recognizer.task")
    results = game(
        'ComputerParts',
        ['CPU', 'RAM', 'SSD', 'Motherboard', 'Case', 'GPU'],
        ['Processes all the instructions fed in by RAM', 'Volatile storage for quick access fed in by SSD', 'Large, slow storage to hold information', 'Electronic housing for all the components', 'Physical housing for all the components', 'Powers what you see on the display']
        )
    print(results)
    exit(0)
    