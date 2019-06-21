import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555
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
    global clientList, matchOn
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
            elif (arr[1]=="wait"):
                reply = waitlistManagement(arr[0],arr[2])
                if reply != "nada":
                    matchOn[arr[2]] = addr
            else:
                addr = matchOn[arr[0]]
                reply = arr[2]
       
        print("Sending: " + reply)
        conn.sendto(reply.encode(), addr)
    

    print("Connection Closed")
    for client in clientList:
        if(client[0] == addr[0]):
            clientList.remove(client)
            break
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