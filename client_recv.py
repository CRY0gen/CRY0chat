import socket
import libs.reorderer as reorderer

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=9009
s.connect((host,port))
while True:
                messg=s.recv(1024).decode('utf-8')
                print(reorderer.dereorderer(messg,"6547"))
input("Press enter to close...")
s.close()
