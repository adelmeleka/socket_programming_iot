import socket
import time

### UDP server side
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 11111))
message = b"Peer 2 UDP server-side message"
server.sendto(message, ('<broadcast>', 50000))
print("message sent from Peer 2 server-side!")
time.sleep(1)

### UDP client side
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 60000))

# while True:
print("Entering Peer 2 client-side")
data, addr = client.recvfrom(1024)
message = b"From Peer 2: I'm here lets create a TCP connection"
client.sendto(message, ('<broadcast>', 50000))
print("received message from Peer 1: %s" % data)

### server & client side of TCP

