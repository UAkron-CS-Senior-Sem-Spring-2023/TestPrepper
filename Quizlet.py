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
    definitionDB = sqlite3.connect("Databases/" + DBName)
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
    path = "./Databases"
    dir_list = os.listdir(path)
    cleanDir = [subtract[:-3] for subtract in dir_list]
    print(cleanDir)
    chapterStudy = input()
    DBName = chapterStudy + ".db"
    definitionDB = sqlite3.connect("Databases/" + DBName)
    DBCursor = definitionDB.cursor()

    # Insert guide into terms list and definitions list
    DBCursor.execute("SELECT Definition FROM " + chapterStudy)
    definitionList = DBCursor.fetchall()
    DBCursor.execute("SELECT Term FROM " + chapterStudy)
    termList = DBCursor.fetchall()

    # Question section
    questionChoice = random.randint(0,len(definitionList) - 1)
    print("What is {}".format(definitionList[questionChoice]) + "?")
    answer = input()
    if termList.count(answer) <= 0 and termList.count(answer) != questionChoice:
        print("Incorrect.")
    else:
        print("Correct!")
