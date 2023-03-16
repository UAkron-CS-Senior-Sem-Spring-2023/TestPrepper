import os
import random

print("Do you want to review a chapter or create a new review?\n"
        "0:Create a new chapter.\n"
        "1:Review a chapter.")
choice = input()
endLoop = '1'

if choice == '0':
    print("What is the chapter?")
    chapterName = input()
    fileChange = open("Term/" + chapterName + "term.txt", "a")
    fileChange.close()
    fileChange = open("Definition/" + chapterName + "definition.txt", "a")
    fileChange.close()

    while endLoop == '1':

        fileChange = open("Term/" + chapterName + "Term.txt", "a")
        print("What's the term?")
        termInput = input()
        fileChange.write(termInput + '$')
        fileChange.close()

        fileChange = open("Definition/" + chapterName + "Definition.txt", "a")
        print("What's the definition?")
        termInput = input()
        fileChange.write(termInput + '$')
        fileChange.close()
        
        print("Done?\n1.Not yet\n2.Yes")

        endLoop = input()
    fileChange.close()

if choice == '1':
    path = "./Term"
    dir_list = os.listdir(path)
    cleanDir = [s.rstrip("Term.txt") for s in dir_list]
    print(cleanDir)
    chapterStudy = input()
    file = open("Term/" + chapterStudy + "Term.txt", "r")
    definitionList = []
    termList = []
    stringManipulate = ''
    while 1:
        char = file.read(1)
        if char != '$':
            stringManipulate += char
        if char == '$':
            termList.append(stringManipulate)
            stringManipulate = ''
        if not char:
            break
    file.close()

    file = open("Definition/" + chapterStudy + "Definition.txt", "r")
    while 1:
        char = file.read(1)
        if char != '$':
            stringManipulate += char
        if char == '$':
            definitionList.append(stringManipulate)
            stringManipulate = ''
        if not char:
            break
    file.close()
    questionChoice = random.randint(0,len(definitionList) - 1)
    print("What is " + definitionList[questionChoice] + "?")
    answer = input()
    if termList.count(answer) <= 0 and termList.count(answer) != questionChoice:
        print("Incorrect.")
    else:
        print("Correct!")
