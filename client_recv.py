import socket
import libs.reorderer as reorderer
import sys
import time

##defining default outputs, add them to CRYFrameWork.py as part of the class
o_debug="[IN-BUILDING DEBUG INFO LOG]"
o_std="[*]"
o_error="[ERROR]"
o_warning="[!]"


def log_outp(message,typelog=o_std):
    print(typelog+" "+message)

##Password for the encryptor
passw="6545766768503480"

##Connecting to server, max tries 5
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname() ##IP HAVE TO BE CHANGED TO STATICAL "192.168.1.79"
port=9009
x=0
while x < 5:
    try:
        log_outp("Try number "+str(x),o_warning)
        time.sleep(0.5)
        s.connect((host,port))
        x=6
    except:
        log_outp("Server may not be on, retrying...")
        for y in range(0,5):
            log_outp("Retrying in "+str(5-y)+" seconds...")
            time.sleep(1)
        x+=1
if x==5:
    exit()

##Initializing logging in Session
cmd=s.recv(1024).decode('utf-8')
if cmd=="id_type":
    log_outp(cmd,o_debug)
    s.sendall("id_recv".encode('utf-8'))
else:
    log_outp("Something unexpected gone wronk in server-side",o_error)
cmd=s.recv(1024).decode('utf-8')
if cmd=="wait":
    while s.recv(1024).decode('utf-8')!="free":
        pass
    cmd="free"
else:
    log_outp("Something unexpected gone wronk in server-side",o_error)

if cmd=="free":
        print("[!]User gained access to the chatroom!")
        input("Press enter to continue...")
        print("\n\n\n\n")
        print("--------------------------------------------------------")
        print("---------------- CHATROOM by CRY0g3n -------------------")
        print("--------------------------------------------------------")
        print("-----------------    ID: RECIVER    --------------------")
        print("--------------------------------------------------------")
        print("\n\n\n\n")
else:
    log_outp("Unexpected Error, closing connection",o_error)

while True:
    msg=s.recv(1024).decode("utf-8")
    log_outp(reorderer.dereorderer(msg,passw),o_std)
input("Press enter to close...")
s.close()
