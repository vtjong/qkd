from clientserver.serverclient import send_secure_msg, receive_secure_msg
from http import client
import sys
sys.path.append('../')

key = "Happy Hacking!"
fullmsg = "Welcome to our MIT iQuHACK Project for QuTech."
server_ip = "192.168.1.7"
receive_secure_msg(key, server_ip)
