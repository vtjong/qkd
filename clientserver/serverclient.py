from encrypt import encrypter, decrypter
from time import sleep
import os
import socket
import pickle
import sys
sys.path.append('../')


def send_secure_msg(key, fullmsg, server_ip):
    """
    Function [send_secure_msg] acts as a client, sending a message [fullmsg], 
    which is then encrypted with key [key] to server at IP [server_ip]. 
    """
    SERVER_HOST = server_ip
    SERVER_PORT = 9090

    # Encrypt msg before sending
    enc_msg = encrypter(key, fullmsg)
    data = pickle.dumps(enc_msg)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, SERVER_PORT))
        client.sendall(data)
        server_reply = client.recv(8192)

    print('Received msg: ', repr(server_reply.decode('utf8')))


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
                data = connection.recv(8192)
                try:
                    enc_msg = pickle.loads(data)
                    if enc_msg != b'':
                        decryped_msg = decrypter(key, enc_msg)
                    if not enc_msg:
                        break
                    connection.sendall(decryped_msg.encode('utf8'))
                except:
                    break
        s.close()
