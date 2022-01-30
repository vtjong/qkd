from serverclient import send_secure_msg
import sys
sys.path.append('../')

key = "Happy Hacking!"
fullmsg = "Welcome to our MIT iQuHACK Project for QuTech."
server_ip = "192.168.1.7"
send_secure_msg(key, fullmsg, server_ip)
