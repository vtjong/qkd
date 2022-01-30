# Python program to implement server side of chat room.
import socket
import select
import sys
import threading

file = open('log.txt', 'w')
file.close()

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# IP address
IP_address, Port = '127.0.0.1', 12346


"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.2
"""
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):

    # sends a message to the client whose user object is conn

    conn.sendall(bytes("Welcome to this chatroom!", encoding="utf-8"))
    # print(f"welcome {addr}")

    while True:
            try:
                message = conn.recv(2048).decode("utf-8")
                if message:

                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    #print ("<" + addr[0] + "> " + message)
                    
                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    
                    # save to log
                    file = open('log.txt', 'a')
                    file.write(f'{message_to_send} \n')
                    file.close()
                    
                    # broadcast(message_to_send, conn)
                    global list_of_clients
    
                    for client in list_of_clients:
                        # if client != connection:
                        try:
                            client.sendall(bytes(message_to_send,
                                                 encoding="utf-8"))
                        except:
                            client.close()
                
                            # if the link is broken, we remove the client
                            remove(client)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)

            except:
                continue

def broadcast(message, connection):
    """Using the below function, we broadcast the message to all
clients """
    global list_of_clients
    
    for client in list_of_clients:
        # if client != connection:
        try:
            client.sendall(bytes(message, encoding="utf-8"))
        except:
            client.close()

            # if the link is broken, we remove the client
            remove(client)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""

    conn, addr = server.accept()
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
    # prints the address of the user that just connected
    print(addr[0] + " connected")
    # creates and individual thread for every user
    # that connects

    threading._start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
