# QuTech Challenges @ MIT iQuHACK 2022

<p align="left">
  <a href="https://qutech.nl" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151484481-7cedb7da-603e-43cc-890c-979fb66aeb60.png" width="25%" style="padding-right: 0%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="10%" style="padding-left: 0%"/> </a>
</p>

## Our Solution

In our group, we have developped three main parts of the challenge:

### QKD Algorithm
We chose the protocol E91 to distribute sifted key between two parties. This protocol is based on Quantum Teleportation. 
The algorithm is coded in Python language as shown in 'E91.py'.
### Encrytption
After obtaining the sifted key from QKD Algorithm, it is time to use the private key to encrypt and decode messages between two parties. In our case, we have used mainly the 'Symmetric Key Algorithms' as shown in 'encrypt.py'. These encryption algorithms are tested on client-server communication and email sending as it is shown by 'serverclient.py' and other relevant testing scripts.
### Chatting Server
Chatting server is a platform of chatroom that maintains group messaging using sockets.
### Website

