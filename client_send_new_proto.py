import socket
import libs.reorderer as reorderer
passw="6545766768503480"
wait_count=0
class iotserver:
        conversion_type="ascii"
        available_conversions=("utf-8","ascii")
        def conv_send(socket,text):
                try:
                        socket.sendall(text.encode(iotserver.conversion_type))
                        return 1
                except:
                        return -1
        def conv_recv(socket,maxbuffer=1024):
                try:
                        recv_str=socket.recv(maxbuffer).decode(iotserver.conversion_type)
                        return recv_str
                except:
                        print('Connection error to the server')
        def setConversionType(text):
                if text in iotserver.available_conversions:
                        iotserver.conversion_type=text
                else:
                        print('conversion type not allowed!')
                
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()##"192.168.1.79"
port=9009
iotserver.setConversionType("utf-8")
connected=0
while connected!=1:
        try:
                s.connect((host,port))
                connected=1
        except:
                print("Server may not be on...")
                connected=0
usr = input("[-]Inserisci nome utente:")
u_pass= input("[-]Inserisci password:")
command=iotserver.conv_recv(s)
if command=="id_type":
        iotserver.conv_send(s,"id_sender")
command=iotserver.conv_recv(s)
if command=="ask_username":
        iotserver.conv_send(s,usr)
command=iotserver.conv_recv(s)
if command == "close_conn_unex_error":
        s.close()
        raise "[!!!]Unexpected server error, closed connection."
elif command=="done":
        command=iotserver.conv_recv(s)

        if command!="ask_password":
                print("[!]Waiting for server to give chat access...")
                while command=="wait":
                        wait_count+=0.00001
                        command=iotserver.conv_recv(s)
                        print("[!]Server has responded!")
        else:
                iotserver.conv_send(s,u_pass)
                command=iotserver.conv_recv(s)
                if command=="error_code_0x001000C":
                        print("[!]Username or password wasn't correct, closing connection to the server...")
                        s.close()
                        input("[#]Press enter to exit the program...")
                        exit()
                elif command=="successfull_connection":
                        iotserver.conv_send(s,"handshake")
                else:
                        print("[!]Unexpected error, closing connection!")
                        s.close()
                        exit()
print("[!]Waiting for server giving access to the chat room...")
command=iotserver.conv_recv(s)
if command=="wait":
        iotserver.conv_send(s,"waiting")
command=iotserver.conv_recv(s)
if command=="free":
        print("[!]User gained access to the chatroom!")
        input("Press enter to continue...")
        print("\n\n\n\n")
        print("--------------------------------------------------------")
        print("---------------- CHATROOM by CRY0g3n -------------------")
        print("--------------------------------------------------------")              
        print("\n\n\n\n")
else:
        print("[!]Unexpected error, closing connection...")
        s.close()
while True:
        text=input("Inserisci il messaggio:")
        mex= "[" + usr + "]" + text
        texte=reorderer.reorderer(mex, passw)
        s.send(texte.encode('utf-8'))
input("Press enter to close...")
s.close()
