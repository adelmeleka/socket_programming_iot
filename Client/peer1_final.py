import socket
import time

#################### Main Function ########################

### Constants
PEER_ID = 1
UDP_SERVER_PORT = 33333
TCP_SERVER_PORT = 0     #fixed for all peers
UDP_CLIENT_PORT = 50000 #fixed for all peers


### UDP server side
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", UDP_SERVER_PORT))
message = "Peer'" + str(PEER_ID) + "'UDP server-side message"
# server.sendto(message, ('<broadcast>', UDP_CLIENT_PORT))
server.sendto(message.encode(), ('<broadcast>', UDP_CLIENT_PORT))
print("message sent from Peer " + str(PEER_ID) + " server-side!")
print("-----------------------------------------------------")
time.sleep(1)


### UDP client side
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", UDP_CLIENT_PORT))
#while True:
print("Entering Peer " + str(PEER_ID) + " client-side")
data, addr = client.recvfrom(1024)
# peerID = data.decode().split("'")[1]
# print("received message from Peer" + peerID + ":%s" % data)
print("received message from Peer 2 :%s" % data)
print("-----------------------------------------------------")


### Implementation of server & client side of TCP
TCPmessage = "Lets Establish TCP Connection"
if data.decode().split(",")[0] != TCPmessage:
    ###TCP Server Side
    print("Entering Peer " + str(PEER_ID) + " TCP server side...")
    time.sleep(1)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("", TCP_SERVER_PORT))
    serverSocket.listen(1)

    # brodcasting TCP greeting message to the
    # corresponding peer who accepted the UDP request
    # client.sendto(TCPmessage+","+TCP_SERVER_PORT.encode(), (addr[0], UDP_CLIENT_PORT))

    TCP_SERVER_PORT = serverSocket.getsockname()[1]
    TCPmessage = TCPmessage + "," + str(TCP_SERVER_PORT)
    client.sendto(TCPmessage.encode(), (addr[0], UDP_CLIENT_PORT))


    print("TCP server is ready to receive")

    # while True:
    #recieve client's request in a new socket
    connectionSocket, addr = serverSocket.accept()

    #server's logic
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()

    #send response to client
    connectionSocket.send(capitalizedSentence.encode())

    #close socket connections
    connectionSocket.close()
    serverSocket.close()

    print("TCP Server OK")
    print("-----------------------------------------------------")

else:
    ###TCP Client Side
    print("Entering Peer " + str(PEER_ID) + " TCP client side...")

    TCPserverPort = int(data.decode().split(",")[1])
    TCPserverName = addr[0]
    print("done")

    TCPclientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPclientSocket.connect((TCPserverName, TCPserverPort))

    # send command
    sentence = input("Input lower case sentence:")
    TCPclientSocket.send(sentence.encode())

    # recieve response
    modifiedSentence = TCPclientSocket.recv(1024)
    print("FromServer:", modifiedSentence.decode())

    TCPclientSocket.close()

