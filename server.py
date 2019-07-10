import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 1999
clientList = []
waitlist = []
matchOn = {}

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

def threaded_client(conn, addr):
    global clientList, matchOn, waitList
    currentId = addr[0]
    conn.send(str.encode(currentId))
    reply = ''
    while True:
        data = conn.recv(2048)
        reply = data.decode('utf-8')
        if not data:
            conn.send(str.encode("Goodbye"))
            break
        else:
            print("Received: " + reply)
            arr = reply.split(":")
            if (arr[1]=="name" or arr[1]=="refresh"):
                if (arr[1]=="name"):
                    foo=0
                    for client in clientList:
                        if client[0]==addr[0]:
                            foo=1
                            break
                    if foo==0:
                        clientList.append((addr[0],arr[2]))
                reply = addr[0]
                for client in clientList:
                    reply += ";"+client[0]+": "+client[1]
                for client in waitlist:
                    if client[0] == addr[0]:
                        waitlist.remove(client)
                        break
            elif (arr[1]=="wait"):
                reply = waitlistManagement(arr[0],arr[2])
                if reply != "nada":
                    matchOn[arr[2]] = [addr, 0]
            elif (arr[1]=="acabou"):
                if arr[0] in matchOn:
                    matchOn[arr[0]][1] = arr[0] + ":acabou:" + arr[2]
            elif (arr[1]=="selfdelete"):
                p2 = matchOn[arr[0]][0][0]
                if p2 in matchOn:
                    del matchOn[p2]
                for client in clientList:
                    if(client[0] == p2):
                        clientList.remove(client)
                        break
                reply = "nada"
            else:
                # matchOn é um dict onde o IP arr[0] (do jogador atual) retorna uma tupla com endereço e uma string com posições
                if matchOn[arr[0]][0][0] in matchOn:
                    matchOn[arr[0]][1] = arr[2]
                    reply = str(matchOn[matchOn[arr[0]][0][0]][1]) # reply é posição do inimigo
                else:
                    reply = str(arr[0])+":acabou:0"
                    if arr[0] in matchOn:
                        del matchOn[arr[0]]

       
        print("Sending: " + reply)
        conn.sendto(reply.encode(), addr)
    

    print("Connection Closed")
    for client in clientList:
        if(client[0] == addr[0]):
            clientList.remove(client)
            break

    if addr[0] in matchOn:
        del matchOn[addr[0]]
    conn.close()

def waitlistManagement (p1, p2):
    global waitlist, clientList, matchOn
    pos = 0
    foundme = 0
    foundthem = 0
    for client in waitlist:
        if client[0]==p1:
            foundme = 1
            pos = client[2]
        if client[1]==p1:
            foundthem = 1
            pos = (client[2]%2)+1
    if foundme == 0:
        if pos == 0:
            waitlist.append((p1,p2,1))
        else:
            waitlist.append((p1,p2,pos))
        return "nada"
    elif foundthem == 0:
        return "nada"
    else:
        killboth = 0
        for client in clientList:
            if client[0] == p2:
                p2 += ":"+client[1]
                break

        for client in waitlist:
            if client[0] == p2 and client[2] == 3:
                killboth = 1
                waitlist.remove(client)
                break

        for client in waitlist:
            if client[0] == p1:
                client[2] == 3
                if killboth == 1:
                    waitlist.remove(client)
                break
        return p1+";"+p2+";"+str(pos)

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, addr))