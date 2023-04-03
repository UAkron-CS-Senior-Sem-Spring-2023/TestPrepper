import os
import random
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# Guide to new guide or review
print("Do you want to review a chapter or create a new review?\n"
        "0:Create a new chapter.\n"
        "1:Review a chapter.\n"
        "2:Export score.")
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
    DBList = DBCursor.fetchall()
    definitionList = [''.join(i) for i in DBList]

    DBCursor.execute("SELECT Term FROM " + chapterStudy)
    DBList = DBCursor.fetchall()
    termList = [''.join(i) for i in DBList]

    array=list(range(0,len(termList) + 0))
    print(array)
    random.shuffle(array)

    # Question section
    for x in array:
        questionChoice = termList[x]
        print("What is {}".format(definitionList[x]) + "?")
        answer = input()
        try:
            if termList.index(answer) == termList.index(questionChoice):
                print("Correct!")
            else:
                print("Incorrect.")
        except ValueError as ve:
            print("Incorrect input.")

if choice == '2':
    x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
    plt.plot(x, np.sin(x))       # Plot the sine of each x point
    plt.show()                   # Display the plot