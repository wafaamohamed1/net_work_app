# importing
from socket import *
import threading

def receive_thread(s):
    while True:
        x=s.recv(500)
        print(x.encode('utf_8'))

#creating
s=socket(AF_INET,SOCK_STREAM)
host='127.0.0.1'
port=8000

s.connect(host,port)

receive=threading.Thread(target=receive_thread,args=(s,))
receive.start()
#send and resiveing

while True:
    s.send(input("enter").encode('utf_8'))

