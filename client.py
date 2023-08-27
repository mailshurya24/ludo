from tkinter import *
from threading import Thread
import socket
from PIL import ImageTk
import random

server = None
port = None
ip = None
canvas1 = None
canvas2 = None
player1Name = 'joining'
player2Name = 'joining'
player1Score = 0
player2Score = 0
winFunctionCall = 0
winningMessage = None
screenWidth = None
screenHeight = None
playerName = None
nameEntry = None
nameWindow = None
dice = None
rollButton = None
playerType = None
finishingbox = None
playerTurn = None
resetButton = None
player1Label = None
player2Label = None
player1ScoreLabel = None
player2ScoreLabel = None
leftboxes = []
rightboxes = []

def checkColourPosition(boxes, colour):
    for box in boxes:
        boxColour = box.cget("bg")
        if boxColour == colour:
            return boxes.index(box)
    return False

def movePlayer1(steps):
    global leftboxes

    boxPosition = checkColourPosition(leftboxes[1:], "red")

    if boxPosition:
        diceValue = steps
        colouredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - colouredBoxIndex

        if steps == remainingSteps:
            for box in leftboxes[1:]:
                box.configure(bg = "white")
            global finishingbox
            finishingbox.configure(bg = "red")
            
            global server
            msg = "Red Wins the Game"
            server.send(msg.encode())

        elif steps < remainingSteps:
            for box in leftboxes[1:]:
                box.configure(bg = "white")
            nextStep = colouredBoxIndex + 1 + diceValue
            leftboxes[nextStep].configure(bg = "red")

        else:
            print("Move False")
    else:
        leftboxes[steps].configure(bg = "red")

def movePlayer2(steps):
    global rightboxes

    boxPosition = checkColourPosition(rightboxes[-2::-1], "yellow")

    if boxPosition:
        diceValue = steps
        colouredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - colouredBoxIndex

        if diceValue == remainingSteps:
            for box in rightboxes[-2::-1]:
                box.configure(bg = "white")
            global finishingbox
            finishingbox.configure(bg = "yellow")
            
            global server
            msg = "Yellow Wins the Game"
            server.send(msg.encode())

        elif diceValue < remainingSteps:
            for box in rightboxes[-2::-1]:
                box.configure(bg = "white")
            nextStep = colouredBoxIndex + 1 + diceValue
            rightboxes[::-1][nextStep].configure(bg = "yellow")

        else:
            print("Move False")
    else:
        rightboxes[len(rightboxes) - (steps + 1)].configure(bg = "yellow")

def handleResetGame():
    global canvas2, playerType, rollButton, dice, resetButton, rightboxes, leftboxes, gamewindow, screenWidth, screenHeight, winningMessage

    if playerType == "Player1":
        rollButton = Button(gamewindow, text = "Roll Dice", fg = 'black', font = ("Chalkboard SE", 15), bg = 'gray', width = 20, height = 5, command = rollDice)
        rollButton.place(x = screenWidth/2 - 80, y = screenHeight/2 + 250)
        playerTurn = True
    
    if playerType == "Player2":
        playerTurn = False

    for i in rightboxes[-2::-1]:
        i.configure(bg = 'white')

    for i in leftboxes[1:]:
        i.configure(bg = 'white')

    finishingbox.configure(bg = 'green')
    canvas2.itemconfigure(winningMessage, text = '')
    resetButton.destroy()
    resetButton = Button(gamewindow, text = "Reset Game", fg = 'black', font = ('Chalkboard SE', 15), bg = 'gray', width = 20, height = 5, command = resetGame)
    winFunctionCall = 0

def resetGame():
    global server
    server.send("Reset Game".encode())

def leftboard():
    global gamewindow, leftboxes, screenHeight

    x1 = 30

    for box in range(0, 11):
        if box == 0:
            boxLabel = Label(gamewindow, font = ("Helvetica", 30), width = 1, height = 1, bg = 'red')
            boxLabel.place(x = x1, y = screenHeight/2 - 88)
            leftboxes.append(boxLabel)
            x1 += 50
        else:
            boxLabel = Label(gamewindow, font = ("Helvetica", 40), width = 1, height = 1, bg = 'white')
            boxLabel.place(x = x1, y = screenHeight/2 - 88)
            leftboxes.append(boxLabel)
            x1 += 65

def rightboard():
    global gamewindow, rightboxes, screenHeight

    x2 = 988

    for box in range(0, 11):
        if box == 10:
            boxLabel = Label(gamewindow, font = ("Helvetica", 30), width = 1, height = 1, bg = 'yellow')
            boxLabel.place(x = x2, y = screenHeight/2 - 88)
            rightboxes.append(boxLabel)
            x2 += 50
        else:
            boxLabel = Label(gamewindow, font = ("Helvetica", 40), width = 1, height = 1, bg = 'white')
            boxLabel.place(x = x2, y = screenHeight/2 - 88)
            rightboxes.append(boxLabel)
            x2 += 65

def finishingBox():
    global gamewindow, finishingbox, screenHeight, screenWidth

    finishingbox = Label(gamewindow, text = 'Home', font = ("Chalkboard SE", 32), width = 8, height = 4, bg = 'green', fg = 'white')
    finishingbox.place(x = screenWidth/2 - 210, y = screenHeight/2 - 160)

def rollDice():
    global server, gamewindow, dice, screenHeight, screenWidth, playerType, playerTurn, rollButton

    dicechoices = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
    value = random.choice(dicechoices)

    rollButton.destroy()
    playerTurn = False

    if playerType == 'Player1':
        server.send(f'{value}player2turn'.encode())

    if playerType == 'Player2':
        server.send(f'{value}player1turn'.encode())

def gameWindow():
    global gamewindow, canvas2, screenWidth, screenHeight, dice, rollButton, playerTurn, playerType, playerName, player1Label, player1ScoreLabel, player1Score, player2Label, player2Score, player2ScoreLabel

    gamewindow = Tk()
    gamewindow.title("Ludo")
    screenHeight = gamewindow.winfo_screenheight()
    screenWidth = gamewindow.winfo_screenwidth()
    

    bg = ImageTk.PhotoImage(file = "./bg1.png")
    canvas2 = Canvas(gamewindow, width = 500, height = 500)
    canvas2.pack(fill = 'both', expand = True)
    canvas2.create_image(0,0, image = bg, anchor = 'nw')
    canvas2.create_text(screenWidth/2, screenHeight/5, text = 'Ludo Ladder', font = ("Chalkboard SE", 100), fill = 'white')
    winningMessage = canvas2.create_text(screenWidth/2 + 10, screenHeight/2 + 250, text = "", font = ("Chalkboard SE", 100), fill = '#FFF176')
    resetButton = Button(gamewindow, text = "Reset Game", fg = "black", font = ("Chalkboard SE", 15), bg = "gray", width = 20, height = 5, command = resetGame)

    leftboard()
    rightboard()
    finishingBox()

    rollButton = Button(gamewindow, text = "Roll Dice", fg = 'black', font = ("Chalkboard SE", 15), bg = 'gray', width = 20, height = 5, command = rollDice)
    
    if playerType == 'Player1' & playerTurn:
        rollButton.place(x = screenWidth/2 - 80, y = screenHeight/2 + 250)
    else:
        rollButton.pack_forget()

    dice = canvas2.create_text(screenWidth/2 + 10, screenHeight/2 + 100, text = "\u2680", font = ("Chalkboard SE", 250), fill = 'white')
    player1Label = canvas2.create_text(400, screenHeight/2 + 65, text = player1Name, font = ("Chalkboard SE", 60), fill = '#FFF176')
    player2Label = canvas2.create_text(400, screenHeight/2 + 65, text = player2Name, font = ("Chalkboard SE", 60), fill = '#FFF176')
    player1ScoreLabel = canvas2.create_text(400, screenHeight/2 + 65, text = player1Score, font = ("Chalkboard SE", 60), fill = '#FFF176')
    player2ScoreLabel = canvas2.create_text(400, screenHeight/2 + 65, text = player2Score, font = ("Chalkboard SE", 60), fill = '#FFF176')

    gamewindow.mainloop()

def updateScore(msg):
    global player1Score, player2Score, player1ScoreLabel, player2ScoreLabel

    if "Red" in msg:
        player1Score += 1
    elif "Yellow" in msg:
        player2Score += 1

    canvas2.itemconfigure(player1ScoreLabel, text = player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text = player2Score)

def handleWin(msg):
    global playerType, rollButton, canvas2, screenHeight, screenWidth, resetButton, winningMessage

    if "Red" in msg:
        if playerType == "Player2":
            rollButton.destroy()
    elif "Yellow" in msg:
        if playerType == "Player1":
            rollButton.destroy()
    
    message = msg.split('.')[0] + '.'
    canvas2.itemconfigure(winningMessage, text = message)
    resetButton.place(x = screenWidth/2 - 80, y = screenHeight - 220)

def saveName():
    global server
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()
    server.send(playerName.encode())

    gameWindow()

def askPlayerName():
    global canvas1, screenWidth, screenHeight, playerName, nameEntry, nameWindow

    nameWindow = Tk()
    nameWindow.title("Ludo-Game")
    screenWidth = nameWindow.winfo_screenwidth()
    screenHeight = nameWindow.winfo_screenheight()
    nameWindow.configure(width = screenWidth, height = screenHeight)

    bg = ImageTk.PhotoImage(file = "./bg1.png")
    canvas1 = Canvas(nameWindow, width = 500, height = 500)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image(0,0, image = bg, anchor = "nw")
    nameLabel = Label(nameWindow, text = "Enter Name: ", font = ("Chalkboard SE", 15))
    nameLabel.place(x = (screenWidth/2) - 500, y = screenHeight/5 - 50)
    nameEntry = Entry(nameWindow, width = 15, justify = 'center', font = ("Chalkboard SE", 15), bd = 2)
    nameEntry.place(x = (screenWidth/2) - 350, y = screenHeight/5 - 50)
    loginButton = Button(nameWindow, text = "Login", font = ("Chalkboard SE", 15), width = 10, command = saveName)
    loginButton.place(x = (screenWidth/2) - 350, y = screenHeight/5)

    nameWindow.mainloop()

def receiveMessage():
    global canvas1, screenWidth, screenHeight, playerName, nameEntry, nameWindow, playerTurn, playerType, rollButton, canvas2, gamewindow, player1Name, player2Name, winFunctionCall, dice, resetButton, player1Label, player2Label

    while True:
        message = server.recv(2048).decode()
        
        if 'playertype' in message:
            message1 = eval(message)
            playerType = message1['playertype']
            playerTurn = message1['turn']
        elif 'playerName' in message:
            message2 = eval(message)
            message2 = message2['playerName']

            for i in message2:
                if i['type'] == 'Player1':
                    player1Name = i['name']
                elif i['type'] == "Player2":
                    player2Name = i['name']
        elif '⚀' in message:
            canvas2.itemconfigure(dice, text = '\u2680')
        elif '⚁' in message:
            canvas2.itemconfigure(dice, text = '\u2681')
        elif '⚂' in message:
            canvas2.itemconfigure(dice, text = '\u2682')
        elif '⚃' in message:
            canvas2.itemconfigure(dice, text = "\u2683")
        elif '⚄' in message:
            canvas2.itemconfigure(dice, text = '\u2684')
        elif '⚅' in message:
            canvas2.itemconfigure(dice, text = '\u2685')
        elif 'Wins the Game' in message and winFunctionCall == 0:
            winFunctionCall += 1
            handleWin(message)
            updateScore(message)
        elif message == 'Reset Game':
            handleResetGame()
        
        if 'player1turn' in message and playerType == 'Player1':
            playerTurn = True
            rollButton = Button(gamewindow, text = "Roll Dice", fg = 'black', font = ("Chalkboard SE", 15), bg = 'gray', width = 20, height = 5, command = rollDice)
            rollButton.place(x = screenWidth/2 - 80, y = screenHeight/2 + 250)
        elif 'player2turn' in message and playerType == "Player2":
            playerTurn = True
            rollButton = Button(gamewindow, text = "Roll Dice", fg = 'black', font = ("Chalkboard SE", 15), bg = 'gray', width = 20, height = 5, command = rollDice)
            rollButton.place(x = screenWidth/2 - 80, y = screenHeight/2 + 250)

        if 'player1turn' in message or 'player2turn' in message:
            diceChoices = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
            diceValue = diceChoices.index(message[0]) + 1

            if 'player1turn' in message:
                movePlayer2(diceValue)
            elif 'player2turn' in message:
                movePlayer1(diceValue)

        if player1Name != 'joining' and canvas2:
            canvas2.itemconfigure(player1Label, text = player1Name)
        elif player2Name != 'joining' and canvas2:
            canvas2.itemconfigure(player2Label, text = player2Name)
        

def setup():
    global server, port, ip
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "127.0.0.1"
    port = 8000
    server.connect((ip, port))
    thread1 = Thread(target = receiveMessage)
    thread1.start()

    askPlayerName()

setup()