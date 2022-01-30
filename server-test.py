from http import client
from serverclient import send_secure_msg, receive_secure_msg
from encrypt import simple_encrypter, simple_decrypter

key = "HELLWORoweroerjk"
fullmsg = "Hello World!"
server_ip = "192.168.1.7"
receive_secure_msg(key, server_ip)

