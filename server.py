import socket 
from threading import Thread
import time

server = None
port = None
ip = None

clients = {}
playerNames = []

def handleClient(socket, name):
    global clients
    global playerNames
    playerType = clients[name]['playertype']

    if playerType == 'Player1':
        clients[name]['turn'] = True
        socket.send(str({
            'playertype': clients[name]['playertype'],
            'turn': clients[name]['turn'],
            'playerName': name
            }).encode())
    else:
        clients[name]['turn'] = False
        socket.send(str({
            'playertype': clients[name]['playertype'],
            'turn': clients[name]['turn'],
            'playerName': name
            }).encode())
    playerNames.append({"name": name, "type": clients[name]['playertype']})
    time.sleep(2)

    if len(playerNames) > 0 and len(playerNames) <= 2:
        for i in clients:
            socket1 = clients[i]['playerSocket']
            socket1.send(str({
                "playerName": playerNames
            }).encode())

    
    while True:
        try:
            message = socket.recv(1024)
            if message:
                for i in clients:
                    s1 = clients[i]['playerSocket']
                    s1.send(message)
        except:
            pass

def acceptConnections():
    global clients, server
    while True:
        playerSocket, addr = server.accept()
        playerName = playerSocket.recv(1024).decode().strip()

        if len(clients.keys()) == 0:
            clients[playerName] = {'playertype': 'Player1'}
        else:
            clients[playerName] = {'playertype': "Player2"}
        
        clients[playerName]["playerSocket"] = playerSocket
        clients[playerName]['address'] = addr
        clients[playerName]['playerName'] = playerName
        clients[playerName]['turn'] = False

        print(f"Connection established with {playerName}:{addr}")

        thread1 = Thread(target = handleClient, args = (playerSocket, playerName))
        thread1.start()

def setup():
    print("Ludo Game")
    global server, port, ip
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "127.0.0.1"
    port = 8000
    server.bind((ip, port))
    server.listen()
    print("Server is waiting for connections")
    acceptConnections()

setup()