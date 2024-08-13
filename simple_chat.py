#servier
#importing
from _thread import *

import threading
from socket import *
def client_thread(coon):
    receive = threading.Thread(target= receive_thread,args=(coon,))
    receive.start()
     
    while True:
        coon.send(input("Enter").encode('utf-8'))
        
def receive_thread(coon):
    while True:
        x=coon.recv(500)
        print(x.decode('utf-8'))

       


#creat a socket 
s = socket(AF_INET,SOCK_STREAM)
# bind
host='127.0.0.1'
port=8000
s.bind(host,port)
#listen
s.listen(5)
# accepting
while True:
    coon ,add = s.accept()
    print("connect fron" , add[0])
    start_new_thread(client_thread,(coon,))