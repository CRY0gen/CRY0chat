import socket
import threading

errors={
    0x0010000 : 0,
    0x001000A : 0,  ##Wrong Username
    0x001000B : 0,  ##Wrong Password
    0x001000C : 0   ##Username or password wrong, just for logs, better use for client
    }
usernames=("admin","shadow","test")
passwords={
    "admin":"password",##Those are just for testing
    "shadow":"darkshadow",
    "test":"testpassword"
    }

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        
    def listen(self):

        print("[!]Listener opened on socket!")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print("[*]Got a connection from ["+str(address[0])+"]")
            threading.Thread(target = self.askForUsername,args = (client,address)).start()
    def askForUsername(self, client, address):
        try:
            client.sendall("id_type".encode("utf-8"))
            if client.recv(1024).decode("utf-8")=="id_recive":
                print("[!]Recive client is connecting...")
                threading.Thread(target = self.askForPassword, args = (client, str(address[0]),"recv_id")).start()
            else:
                print("[*]User whith ip: ["+str(address[0])+"] is connecting, asking for the username...")
                try:
                    client.sendall("ask_username".encode("utf-8"))
                    username=client.recv(1024).decode("utf-8")
                    for x in usernames:
                        if x == username:
                            print("["+str(address[0])+"]User successfully logged in as ["+ username+"]")
                            client.sendall("done".encode("utf-8"))
                            print("[*]Asking for password...")
                            threading.Thread(target = self.askForPassword, args = (client, str(address[0]), username)).start()
                            return "successfully-logged"
                    errors[0x001000A]+=1
                    username="0x001000A"
                    print("[!]No username has found, keep asking for password...")##in developing
                    print(errors)
                    client.sendall("done".encode("utf-8"))
                    threading.Thread(target = self.askForPassword, args = (client, str(address[0]), username)).start()
                except:
                    print("[ ERROR ]\n[!!!]Unexpected error, closing client connection...")
                    client.sendall("close_conn_unex_error".encode("utf-8"))
    
                    client.close()
        except:
            print("[!!!]ERROR: unexpected error, closing client connection...")
            client.sendall("close_conn_unex_error".encode("utf-8"))
            client.close()

    def askForPassword(self, client, address, username):
        clients_lock = threading.Lock()
        clients = set()
        try:
            print(username)
            if username=="id_recv":
                print("[!]'Recive' client is connecting: bypassing password necessity!")
                client.sendall("wait".encode("utf-8"))
                with clients_lock:
                    clients.add(client)
                threading.Thread(target=self.listenToClient, args=(client, address, clients, clients_lock)).start()
            elif username=="0x001000A":
                print("[*]Sending error info...")
                client.sendall("ask_password".encode("utf-8"))
                client.recv(1024).decode("utf-8")##just needed to wait for the response of the client
                errors[0x001000B]+=1
                client.sendall("error_code_0x001000C".encode("utf-8"))
            else:
                client.sendall("ask_password".encode("utf-8"))
                password = client.recv(1024).decode("utf-8") ##will be encrypted by my algorithm
                if passwords[username]==password:
                    print("[-]User (ip="+address+") has successfully connected to the server!")
                    print("[-]User's public username: "+username)
                    client.sendall("successfull_connection".encode("utf-8"))
                    if client.recv(1024).decode("utf-8")=="handshake":
                        client.sendall("wait".encode("utf-8"))
                        
                        if client.recv(1024).decode("utf-8")=="waiting":
                            with clients_lock:
                                clients.add(client)
                            threading.Thread(target=self.listenToClient, args=(client, address, clients, clients_lock)).start()
                    else:
                        print("[!]ALERT: client hasn't accepted the handshake, closing connection!")
                        client.close()
                else:
                    print("[!]Wrong password!\n[#]Closing connection...",end="")
                    errors[0x001000B]+=1
                    client.sendall("error_code_0x001000C".encode("utf-8"))
                    client.close()
                    print("[ DONE ]")
        except:
            print("[!!!]Unexpected error!")
            client.close()
            

    def listenToClient(self, client, address, clients, clients_lock):
        size = 1024
        client.sendall("free".encode("utf-8"))
        while True:
            try:
                data = client.recv(size)
                print("[*]Recived client data from [" + address+"]")
                if data:
                    with clients_lock:
                        for c in clients:
                            c.sendall(data)
                else:
                    raise error('[!]Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    print("#### Encoded Chat Server By CRY0g3n ####")
    port_num = input("[*]Server port: ")
    ThreadedServer('0.0.0.0',int(port_num)).listen()
