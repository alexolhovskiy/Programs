import threading
import tkinter
from tkinter import * #Listbox, Variable, 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import socket

nickname=""
port=0
ip=""


with open("regData.txt","r") as file:
    nickname,ip,temp=file.read().split(' ')
    port=int(temp)




window=tkinter.Tk()
window.title("Local Comunicator")
window.geometry("600x300+100+100")


##def parseIP():
##    out = os.popen("ipconfig").read()
##    arr=out.split('\n')
##    arrr=arr[len(arr)-9].split(" ")
##    print(arrr[len(arrr)-1])
##    return arrr[len(arrr)-1]


window.columnconfigure(index=0,weight=4)
window.columnconfigure(index=1,weight=4)
window.columnconfigure(index=2,weight=4)
window.columnconfigure(index=3,weight=4)
window.columnconfigure(index=4,weight=1)
window.columnconfigure(index=5,weight=4)
window.columnconfigure(index=6,weight=4)
window.columnconfigure(index=7,weight=1)
window.rowconfigure(index=0,weight=1)
window.rowconfigure(index=1,weight=1)
window.rowconfigure(index=2,weight=1)
window.rowconfigure(index=3,weight=1)
window.rowconfigure(index=4,weight=1)




#label=ttk.Label(text=f'IP: {parseIP()}')
label=ttk.Label(text=f'{nickname},ip:{ip},port:{port}')
label.grid(column=0,columnspan=2,row=0,padx=6,pady=6,sticky="NSEW")
entry = ttk.Entry()
entry.grid(column=0,columnspan=2,row=1,padx=6,pady=6,sticky="NSEW")

my_messages=[]
messages_var = Variable(value=my_messages)

my_contacts=[]
contacts_var = Variable(value=my_contacts)






#########################client###############################33
servers=[]

def write(message,server):
    server.send(message.encode('ascii'))
    
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
    pass

def handleConnection(ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    
    message = client.recv(1024).decode('ascii')
    if message == 'NICK':
        client.send(nickname.encode('ascii'))
        
    message = client.recv(1024).decode('ascii')
    if message=='Connected to server!':
        print(message)
        return {"connection":True,"ip":ip,"port":port,"server":client}
        
    return {"connection":False,"ip":ip,"port":port,"server":client}
#####################server#########################################
clients = []
nicknames = []
key=False

# Handling Messages From Clients
def handle(client):
    print("Handle start!")
    while True:
        print("Handle work!")
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode('ascii')
            print(message)
            if message.split(' ')[0]=="FILE":
                answer = messagebox.askyesno(title="File Saving",message=f"{nicknames[clients.index(client)]} send you file:{message.split(' ')[1]}.Save it?")
                if answer:
                    filepath=filedialog.askopenfilename()
                    print(filepath)
                    client.send("FILE_OK".encode('ascii'))
                    with open(filepath,"wb") as file:
                        print("receiving data from client")
                        while True:
                            data = client.recv(1024)
##                            print(f"{data},{len(data)}")
                            file.write(data)
                            print("receive")
                            if len(data)<1024:break
                        print("Done!") 
            else:
                my_messages.append(f"{nicknames[clients.index(client)]}:{message}")
                messages_var.set(my_messages)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
    print("Handle stop!")

# Receiving / Listening Function
def receive(port,host):
    # Connection Data
    # Starting Server
    global key
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"{ip} {port}")
    server.bind((host, port))
    server.listen()
    print("Receive start!")
    while key:
        print("Receive work!")
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        client.send('Connected to server!'.encode('ascii'))


        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

    print("Receive stop!")

def ServerReceive():
    global key
    global nickname
    global ip
    global port
    print("Server is listening...")
    
    if key==True:
        key=False
        buttons[5]["text"]="Receive"
        
    else:
        key=True
        buttons[5]["text"]="Stop Receive"
        thread = threading.Thread(target=receive, args=(port,ip))
        thread.start()  
        
    print(key)

###################################################################################

with open("contacts.txt","r") as file:
    for line in file:
        c_name,c_ip,c_port=line.split(' ')
        print(c_name)
        print(c_ip)
        print(c_port)
        
        my_contacts.append(f"{c_name},{c_ip},{c_port}")
        contacts_var.set(my_contacts)
        
##        
##        servers.append(handleConnection(ip,int(port)))




def Open():
    filepath = filedialog.askopenfilename()
    print(filepath)
    for num in lb.curselection():
        n,ip,port=lb.get(num).split(',')
        for server in servers:
            print(f"{port},{ip}")
            if (server["ip"]==ip)&(server["port"]==int(port)):
                sendFile(filepath,server["server"])
                my_messages.append(f"{ip},{port}:{filepath}")
                messages_var.set(my_messages)
    pass

def Connect():
    for num in lb.curselection():
        n,ip,port=lb.get(num).split(',')
        servers.append(handleConnection(ip,int(port)))
        my_contacts[num]=f"Connect:{my_contacts[num]}"
        contacts_var.set(my_contacts)
    pass

def Message():
    global servers
    global lb
    my_message=entry.get()
    #messages_var.set(my_messages)
    
    for num in lb.curselection():
        n,ip,port=lb.get(num).split(',')
        for server in servers:
            print(f"{port},{ip}")
            if (server["ip"]==ip)&(server["port"]==int(port)):
                write(my_message,server["server"])
                my_messages.append(f"{ip},{port}:{my_message}")
                messages_var.set(my_messages)
    
    
    pass

def IP():
    global servers
    contactName=entry.get()
    ip,port=contactName.split(',')
    print(ip)
    print(port)
    
    my_contacts.append(contactName)
    contacts_var.set(my_contacts)
    
    servers.append(handleConnection(ip,int(port)))

    pass

def Registration():
    global nickname
    global ip
    global port
    nickname,ip,temp=entry.get().split(',')
    port=int(temp)
    print(nickname)
    print(ip)
    print(port)
    with open("regData.txt","w") as file:
        file.write(f"{nickname} {ip} {port}")


buttons=[]
buttons.append(ttk.Button(text="Send File",command=Open))
buttons.append(ttk.Button(text="Connect",command=Connect))
buttons.append(ttk.Button(text="Add Connection",command=IP))
buttons.append(ttk.Button(text="Send Message",command=Message))
buttons.append(ttk.Button(text="Registration",command=Registration))
buttons.append(ttk.Button(text="Receive",command=ServerReceive))

buttons[0].grid(column=0,row=2,padx=6,pady=6,sticky="NSEW")
buttons[1].grid(column=1,row=2,padx=6,pady=6,sticky="NSEW")
buttons[2].grid(column=0,row=3,padx=6,pady=6,sticky="NSEW")
buttons[3].grid(column=1,row=3,padx=6,pady=6,sticky="NSEW")
buttons[4].grid(column=0,row=4,padx=6,pady=6,sticky="NSEW")
buttons[5].grid(column=1,row=4,padx=6,pady=6,sticky="NSEW")



lb=Listbox(listvariable=contacts_var,selectmode=MULTIPLE,selectbackground="red")

lb.grid(column=2,columnspan=2,row=0,rowspan=5,sticky="NSEW",padx=6,pady=6)


scroll=ttk.Scrollbar(orient="vertical",command=lb.yview)
scroll.grid(column=4,row=0,rowspan=5,sticky="NS")
lb["yscrollcommand"]=scroll.set



lb2=Listbox(listvariable=messages_var)

lb2.grid(column=5,columnspan=2,row=0,rowspan=5,sticky="NSEW",padx=6,pady=6)


scroll2=ttk.Scrollbar(orient="vertical",command=lb2.yview)
scroll2.grid(column=7,row=0,rowspan=5,sticky="NS")
lb2["yscrollcommand"]=scroll2.set



##filepath = filedialog.askopenfilename()
##print(filepath)

window.mainloop()








