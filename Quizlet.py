import os
import random
import sqlite3
# Guide to new guide or review
print("Do you want to review a chapter or create a new review?\n"
        "0:Create a new chapter.\n"
        "1:Review a chapter.")
choice = input()
endLoop = '1'

if choice == '0':

    # Build database for definitions and terms
    chapterName = input("What is the chapter?" )
    DBName = chapterName + ".db"
    definitionDB = sqlite3.connect(DBName)
    DBCursor = definitionDB.cursor()
    DBCursor.execute('CREATE TABLE ' + chapterName + '(Definition text, Term text)')
    # Loop the terms and definitions until everything is inserted
    while endLoop == '1':
        print("What's the term?")
        termInput = input()

        print("What's the definition?")
        definitionInput = input()
        
        DBCursor.execute("INSERT INTO " + chapterName + " VALUES ('" + definitionInput + "', '" + termInput + "')")

        print("Done?\n1.Not yet\n2.Yes")
        definitionDB.commit()
        endLoop = input()

if choice == '1':

    # Display list of guides available
    path = "./Term"
    dir_list = os.listdir(path)
    cleanDir = [s.rstrip("Term.txt") for s in dir_list]
    print(cleanDir)
    chapterStudy = input()

    # Insert guide into terms list and definitions list
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

    # Question section
    questionChoice = random.randint(0,len(definitionList) - 1)
    print("What is " + definitionList[questionChoice] + "?")
    answer = input()
    if termList.count(answer) <= 0 and termList.count(answer) != questionChoice:
        print("Incorrect.")
    else:
        print("Correct!")
