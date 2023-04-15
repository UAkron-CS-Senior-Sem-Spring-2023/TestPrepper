import os
import random
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# Guide to new guide, review, or score graph
print("Do you want to review a chapter or create a new review?\n"
        "0:Create a new chapter.\n"
        "1:Review a chapter.\n"
        "2:Export graph of scores.")
choice = input()
endLoop = '1'

if choice == '0':

    # Build database for definitions and terms
    chapterName = input("What is the chapter?" )
    DBName = chapterName + ".db"
    definitionDB = sqlite3.connect("Databases/" + DBName)
    DBCursor = definitionDB.cursor()
    DBCursor.execute('CREATE TABLE ' + chapterName + '(Definition text, Term text)')
    DBCursor.execute('CREATE TABLE score (Term text, correct int)')
    DBCursor.execute('INSERT INTO score VALUES ("Total", 0)')

    # Loop the terms and definitions until everything is inserted
    while endLoop == '1':
        print("What's the term?")
        termInput = input()

        print("What's the definition?")
        definitionInput = input()
        
        DBCursor.execute("INSERT INTO " + chapterName + " VALUES ('" + definitionInput + "', '" + termInput + "')")
        DBCursor.execute('INSERT INTO score VALUES ("'+ termInput + '", 0)')

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

    testChoice = input("What kind of test do you want?\nMultiple choice:1\nQuestion/Answer:2\n")
    if testChoice == '1':
        # Develop Multiple choice quiz
        array=list(range(0,len(termList) + 0))
        random.shuffle(array)
        DBCursor.execute("UPDATE score SET correct = correct + 1 WHERE Term = 'Total'")
        definitionDB.commit()
        # Question section
        for x in array:
            choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
            while len(set(choicePicker)) != len(choicePicker):
                 choicePicker = [termList[x],termList[random.choice(array)],termList[random.choice(array)],termList[random.choice(array)]]
            random.shuffle(choicePicker)

            questionChoice = termList[x]
            print("What is {}".format(definitionList[x]) + "?")
            print("A.{}".format(choicePicker[0]))
            print("B.{}".format(choicePicker[1]))
            print("C.{}".format(choicePicker[2]))
            print("D.{}".format(choicePicker[3]))
            answer = input()
            if(answer == 'a' or answer == 'A' and choicePicker[0] == termList[x]):
                answer = choicePicker[0]
            if(answer == 'b' or answer == 'B' and choicePicker[1] == termList[x]):
                answer = choicePicker[1]
            if(answer == 'c' or answer == 'C' and choicePicker[2] == termList[x]):
                answer = choicePicker[2]
            if(answer == 'd' or answer == 'D' and choicePicker[3] == termList[x]):
                answer = choicePicker[3]
            try:
                if termList.index(answer) == termList.index(questionChoice):
                    DBCursor.execute("UPDATE score SET correct = correct + 1 WHERE Term = '" + answer + "';")
                    definitionDB.commit()
                    print("Correct!")
                else:
                    print("Incorrect.")
            except ValueError as ve:
                print("Incorrect input.")
    if testChoice == '2':
        # Develop Q/A quiz
        array=list(range(0,len(termList) + 0))
        random.shuffle(array)
        DBCursor.execute("UPDATE score SET correct = correct + 1 WHERE Term = 'Total'")
        definitionDB.commit()
        # Question section
        for x in array:
            questionChoice = termList[x]
            print("What is {}".format(definitionList[x]) + "?")
            answer = input()
            try:
                if termList.index(answer) == termList.index(questionChoice):
                    DBCursor.execute("UPDATE score SET correct = correct + 1 WHERE Term = '" + answer + "';")
                    definitionDB.commit()
                    print("Correct!")
                else:
                    print("Incorrect.")
            except ValueError as ve:
                print("Incorrect input.")

if choice == '2':

    # Display list of guides available
    path = "./Databases"
    dir_list = os.listdir(path)
    cleanDir = [subtract[:-3] for subtract in dir_list]
    print(cleanDir)
    chapterStudy = input()
    DBName = chapterStudy + ".db"
    definitionDB = sqlite3.connect("Databases/" + DBName)
    DBCursor = definitionDB.cursor()

    # Build y-plot
    DBCursor.execute("SELECT Term FROM score")
    DBList = DBCursor.fetchall()
    testStringList = [''.join(i) for i in DBList]
    testStringList.pop(0)

    # Build x-plot
    DBCursor.execute("SELECT correct FROM score")
    DBList = DBCursor.fetchall()
    testIntList = [int(i[0]) for i in DBList]
    totalTestsTaken = testIntList[0]
    testIntList.pop(0)

    # Display
    plt.bar(testStringList, testIntList)
    plt.show()
    