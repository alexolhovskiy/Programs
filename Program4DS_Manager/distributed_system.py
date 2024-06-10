import threading 
from tkinter import filedialog
from tkinter import messagebox
import os
import socket


integrity=False
contacts=[]
servers=[]
clients = []

def init():
    with open("ds_resourses.txt","r") as file:
        for line in file:
            contacts.append(line)



#########################client###############################33

    
def sendFile(filepath,server):
    arr=filepath.split('/')
    filename=arr[len(arr)-1]
    print(filename)
    server.send(f"FILE {filename}".encode('ascii'))
    message = server.recv(1024).decode('ascii')
    print(message)
    
    if message=="FILE_OK":
        with open(filepath,"rb") as file:
            print("sending data to client")
            data = file.read(1024)
            while data:
                server.send(data)
                print("send")
                data = file.read(1024) 
            #server.send("OVER".encode('ascii'))   
            print("Done!")
            
def sendFile2(filepath,server):
    arr=filepath.split('/')
    filename=arr[len(arr)-1]
    print(filename)
    server.send(f"FILER {filename}".encode('ascii'))
    message = server.recv(1024).decode('ascii')
    print(message)
    
    if message=="FILE_OK":
        with open(filepath,"rb") as file:
            print("sending data to client")
            data = file.read(1024)
            while data:
                server.send(data)
                print("send")
                data = file.read(1024) 
            #server.send("OVER".encode('ascii'))   
            print("Done!")
    
def sendRequest(message,server):
    server.send(message.encode('ascii'))
    

def handleConnection(name,ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    
    message = client.recv(1024).decode('ascii')
    if message == 'NICK':
        client.send(name.encode('ascii'))
        
    message = client.recv(1024).decode('ascii')
    if message=='Connected to server!':
        print(message)
        return {"connection":True,"name":name,"ip":ip,"port":port,"server":client}
        
    return {"connection":False,"name":name,"ip":ip,"port":port,"server":client}



def clientWork():
    arr=contacts[0].split(' ')  
    servers.append(handleConnection(arr[0],arr[1],int(arr[2])))

#####################server#########################################


# Handling Messages From Clients
def handle(client,nickname):
    print("Handle start!")
    while True:
        print("Handle work!")
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
            arr=message.split(' ')
            if arr[0]=="FILE":
                client.send("FILE_OK".encode('ascii'))
                with open(arr[1],"wb") as file:
                    print("receiving data from client")
                    data = client.recv(1024)
                    while len(data)==1024:
                        file.write(data)
                        print(data)
                        data = client.recv(1024)
                    file.write(data)
                    print("Done!") 
                    
            elif arr[0]=="REQUEST":
                for dic in clients:
                    if dic["name"]==nickname:
                        index = clients.index(dic)
                
                for server in servers:
                    if (server["ip"]==clients[index]["ip"])&(server["port"]==clients[index]["port"]):
                        sendFile(arr[1],server)
                        
            elif arr[0]=="FILER":
                answer = messagebox.askyesno(title="File from request! Save it?")
                if answer:
                    dirpath=filedialog.askdirectory()
                    print(f"{dirpath}/{arr[1]}")
                    client.send("FILE_OK".encode('ascii'))
                    with open(f"{dirpath}/{arr[1]}","wb") as file:
                        print("receiving data from client")
                        while True:
                            data = client.recv(1024)
##                            print(f"{data},{len(data)}")
                            file.write(data)
                            print("receive")
                            if len(data)<1024:break
                        print("Done!") 
                
        except:
            # Removing And Closing Clients
            for dic in clients:
                if dic["name"]==nickname:
                    print(f"Client {dic["name"]} disconnect")
                    dic["client"].close()
                    index = clients.index(dic)
            clients.remove(index)
            break
    print("Handle stop!")

# Receiving / Listening Function
def receive(name,host,port):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"{name} {host} {port}")
    server.bind((host, port))
    server.listen()
    print("Receive start!")
    while True:
        print("Receive work!")
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        print("Nickname is {}".format(nickname))
        client.send('Connected to server!'.encode('ascii'))
        
        clients.append({"connection":True,"name":nickname,"ip":host,"port":port,"client":client})

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,nickname))
        thread.start()


def serverReceive():
    arr=contacts[0].split(' ')
    thread = threading.Thread(target=receive, args=(arr[0],arr[1],int(arr[2])))
    thread.start()  
       

###################################################################################


def copyFile1(filepath):
    arr=filepath.slit('/')
    filename=arr[len(arr)-1]
    with open(filename,"wb") as file:
        with open(filepath,"rb") as file2:
            for line in file2:
                file.write(line)    
            print("Done!") 


def copyFile2(filename):
    filepath=filedialog.askopenfile()
    with open(filepath,"wb") as file:
        with open(filename,"rb") as file2:
            for line in file2:
                file.write(line)    
            print("Done!") 


def sendFiles(progect_name,file_names):
    print(file_names)
    name=contacts[0].split(' ')[0]
    temp=[]
    for file in file_names:
        arr=file.split('.')
        extention=arr[len(arr)-1]
        arr=file.split('/')
        fileName=arr[len(arr)-1]
        
        if extention==name:
            copyFile1(file)
            temp.append(f"{fileName},{contacts[0].split(' ')[1]},{contacts[0].split(' ')[2]}")
        for server in servers:
            if extention==server["name"]:
                sendFile(file,server["server"])
                temp.append(f"{fileName},{server["ip"]},{server["port"]}")
    
                
    with open(f"prog_{progect_name}.txt","a") as f:
        for item in temp:
            f.write(item)
    
    for server in servers:
        sendFile("ds_registration.txt",server["server"])


def getFiles(progect_name):
    print(progect_name)
    
    with open(f"prog_{progect_name}.txt","r") as f:
        for line in f:
            arr=line.split(',')
            if (arr[1]==contacts[0].split(' ')[1])&(arr[2]==contacts[0].split(' ')[2]):
                copyFile2(arr[0])
            for server in servers:
                if (arr[1]==server["ip"]) & (int(arr[2])==server["port"]):
                    sendRequest(f"REQUEST {arr[0]}",server)



def checkIntegrity():
    cnt=0
    for contact in contacts[1:]:
        arr=contact.split(' ')
        for server in servers:
            if (arr[0]==server["name"]) & (arr[1]==server["ip"]) & (int(arr[2])==server["port"]):
                cnt+=1

    if cnt==2:
        integrity=True
    else:
        integrity=False







