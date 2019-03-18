import socket , threading
from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('148.70.120.145', 2101)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)
window = Tk()
window.title("聊天室")
window.geometry('600x600')
titleImage = PhotoImage(file="./image/client.gif")
frame1 = Frame(window)
frame1.pack()
Label(frame1, image=titleImage).pack(side='top')
frame2 = Frame(window)
frame2.pack()
label2 = Label(frame2, text="请输入要发送的文字", font=('Arial', 16), width=20)
val3 = StringVar()
entryVal_text = Entry(frame2, bd=5, width=40, textvariable=val3)
label2.pack(side=LEFT)
entryVal_text.pack(side=LEFT)
frame3 = Frame(window)
frame3.pack()
text = ScrolledText(window)
text.pack(padx=5,pady=5)
   



def sendMsg():
    global sock
    global val3
    message  = str(val3.get())
    sock.send(message.encode('utf-8'))
frame2 = Frame(window)
frame2.pack()
sendBtn = Button(frame2, text="Send",font=('Arial', 16), width=16, bg='MintCream', command = sendMsg)
sendBtn.pack()


def receiveMsg():
    while True:
        try:
                data = sock.recv(1024)
                #print(sys.stderr, 'client received "%s"\n' % data)
                data_end = '\n'+str(data)
                text.insert(END,data_end)
        except:
            pass
receiveThread = threading.Thread(name='waitForMSG', target=receiveMsg)
receiveThread.start()
sendThread = threading.Thread(name='send', target=sendMsg)
sendThread.start()
window.mainloop()
