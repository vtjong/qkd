import socket
import os
from time import sleep
from encrypt import simple_encrypter, simple_decrypter


"""
NOT COMPLETE WITH LONGER MSGS
"""

def send_secure_msg(key, fullmsg, server_ip):
    """
    Function [send_secure_msg] acts as a client, sending a message [fullmsg], 
    which is then encrypted with key [key] to server at IP [server_ip]. 
    """
    SERVER_HOST = server_ip
    SERVER_PORT = 9090

    # Encrypt msg before sending
    enc_msg = simple_encrypter(key, fullmsg)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, SERVER_PORT))
        client.sendall(enc_msg)
        server_reply = client.recv(1024)

    print('Received', repr(server_reply))

def receive_secure_msg(key, local_host):
    """
    Function [receive_secure_msg] receives an encrypted message [enc_msg] and
    decrypts it with key [key]. 
    """
    HOST = local_host
    PORT = 9090

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        connection, addr = s.accept()
        
        with connection:
            print('Connected by', addr)
            while True:
                enc_msg = connection.recv(1024)
                print(enc_msg)
                decryped_msg = simple_decrypter(key,enc_msg)
                if not enc_msg:
                    break
                connection.sendall(decryped_msg.encode('utf8'))

    