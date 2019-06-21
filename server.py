import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555
clientList = []
waitlist = []

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

pos = ["0:0,300", "1:500,300"]
def threaded_client(conn, addr):
    global pos, clientList, waitlist
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
                    clientList.append((addr[0],arr[2]))
                reply = addr[0]
                for client in clientList:
                    reply += ";"+client[0]+": "+client[1]
            elif (arr[1]=="wait"):
                reply = waitlistManagement(arr[0],arr[2])
            else:
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = str.encode(pos[addr[0]][:])
       
        print("Sending: " + reply)
        conn.sendto(reply.encode(), addr)
    

    print("Connection Closed")
    for client in clientList:
        if(client[0] == addr[0]):
            clientList.remove(client)
            break
    conn.close()

def waitlistManagement (p1, p2):
    global waitlist, clientList
    pos = 0
    found = 0
    for client in waitlist:
        if client[0]==p1:
            found = 1
            pos = client[2]
        if client[1]==p1:
            pos = (client[2]%2)+1
    if found == 0:
        if pos == 0:
            waitlist.append((p1,p2,1))
        else:
            waitlist.append((p1,p2,found))
        return "nada"
    else:
        for client in waitlist:
            if client[0] == p1:
                waitlist.remove(client)
                break
        for client in clientList:
            if client[0] == p2:
                p2 += ":" client[1]
                break
        return p1+";"+p2+";"+pos

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, addr))