#Client
import tkinter as tk
from socket import * 
from threading import *
from tkinter import *
from tkinter import filedialog


client = socket(AF_INET, SOCK_STREAM)
#ip adresinizi bulmak için cmd komut istemcisine ipconfig yazınız
ip = '10.100.5.139'
port = 55555

client.connect((ip, port))

pencere = Tk()
pencere.title('Bağlandı :' + ip + ":" + str(port))

messages = Text(pencere, width=80)
messages.grid(row=0, column=0, padx=10, pady=10)

yourMessage = Entry(pencere, width=50 )
yourMessage.insert(0, 'Isminizi giriniz')
yourMessage.grid(row=1, column=0, padx=10, pady=10) 
yourMessage.focus()
yourMessage.selection_range(0, END)



def sendMessage():
    clientMessage = yourMessage.get()
    messages.insert(END, '\n' + 'Sen: ' + clientMessage)
    client.send(clientMessage.encode('utf8'))
    yourMessage.delete(0, END)

bmessageGonder = Button(pencere, text='Gönder', width=16, command=sendMessage)
bmessageGonder.grid(row=1, column=1, padx=5, pady=8)

def receiveMessage():
    while True:
        data = client.recv(4096)
        if not data:
            break


def sendFile():
    file_path = filedialog.askopenfilename()  
    if file_path:  
        with open(file_path, "rb") as file:
            file_data = file.read()
            client.sendall(file_data) 
            messages.insert(END, '\nDosya gönderildi: ' + file_path)

bsendFile = Button(pencere, text="Dosya Seç", width=16, command=sendFile)
bsendFile.grid(row=1, column=2, padx=5, pady=8)


def receiveFile():
    while True:
        data = client.recv(4096)
        if not data:
            break
        
        
        

def sendImage():
    file_path = filedialog.askopenfilename()  
    if file_path:  
        with open(file_path, "rb") as file:
            file_data = file.read()
            client.sendall(file_data)  # Resmi gönder
            messages.insert("end", '\nResim gönderildi: ' + file_path)

bSendImage = Button(pencere, text="Resim Seç", width=16, command=sendImage)
bSendImage.grid(row=1, column=3, padx=5, pady=8)


def receiveImage():
    while True:
        data = client.recv(4096)
        if not data:
            break



def onEnter(event):
    sendMessage()

yourMessage.bind("<Return>",onEnter)



def recvMessage():
    while True:
        serverMessage = client.recv(1024).decode('utf8')
        messages.insert(END, '\n' + serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

pencere.mainloop()

