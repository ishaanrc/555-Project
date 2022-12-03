import socket	
import threading
import time
from subprocess import Popen
import os  
import rsa
import binascii

publicKey = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALoJfUHJ4wA5DgajmX85KnZy4JEwarUxQomiv5cHkqgtrhQbooJujTA8PSA7B5SkwiVSsWX9fs7LBi2ESwOSGdECAwEAAQ=="
privateKey = "MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAugl9QcnjADkOBqOZfzkqdnLgkTBqtTFCiaK/lweSqC2uFBuigm6NMDw9IDsHlKTCJVKxZf1+zssGLYRLA5IZ0QIDAQABAkB7w/Rg4D701wBNymlECnQFeUeNT/itsqfhiTSM9azL1PR6safJFQFsZRpCY/hw46kH6jvblkE7ZASNco2ilQQBAiEA7udLH2IFcNwvPUZ2nvfQ2p4wmpGNx/AlkPiZua4puPkCIQDHWa8lrql+xj/g5hWbgJK+B7mBnG7LJvP/A+3ieM81mQIhALtQnIUxvORdr6hSrEU+NwKCj8dRoqIGd93wHdAJb2s5AiEAu01Aix84kayjiCOmWZzMQ0/utCDO2IGY7xo6AHeR+MECIDcf1fb3xaT5fnajRh42Nx0gk3oB6MxB7rRSKO3vz8D2"

######
#os.system(' /path/shellscriptfile.sh {}'.format(str(publicKey)) )


# Import socket module
import socket	
encryptedVal=""		
def listening():
    # Create a socket object
    s = socket.socket()		

    # Define the port on which you want to connect
    port = 12346		

    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    # receive data from the server and decoding to get the string.
    #print (s.recv(1024).decode())
   
    encryptedVal=s.recv(1024).decode()
  
    if(encryptedVal):
        print("encrypted value of result received ")
   

    # close the connection
    s.close()	
        
def sending():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    serverSocket.bind(("127.0.0.1",12345))

    serverSocket.listen()

    while(True):
        (clientConnected, clientAddress) = serverSocket.accept()
        print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
        clientConnected.send("Hello Clien!".encode())
        break

listening()
