# QuTech Challenges @ MIT iQuHACK 2022

<p align="left">
  <a href="https://qutech.nl" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151484481-7cedb7da-603e-43cc-890c-979fb66aeb60.png" width="25%" style="padding-right: 0%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="10%" style="padding-left: 0%"/> </a>
</p>

## Description
For this challenge you will be tasked with creating an interface and method to use quantum key
distribution to send an encrypted message between the members of your team.

## Our Solution

In our group, we have developped 4 main divisions of the challenge:

### QKD Algorithm
We chose the protocol E91 to distribute sifted key between two parties. This protocol is based on Quantum Teleportation. 
The algorithm is coded in Python language as shown in 'E91.py'. We have implemented the protocol on the Emulator in order to get benefit of the large number of qubits available.

### Encrytption
After obtaining the sifted key from QKD Algorithm, it is time to use the private key to encrypt and decode messages between two parties. In our case, we have used mainly the 'Symmetric Key Algorithms' as shown in 'encrypt.py'. These encryption algorithms are tested on client-server communication and email sending as it is shown by 'serverclient.py' and other relevant testing scripts.

### Chatting Server
Chatting server is a platform of chatroom that maintains group messaging using sockets. The chatroom server and clients are programmed by 'server_side.py' and 'client_side.py'.

### Website
The chat website is programmed using Django. It contains all HTML, CSS, Python and javascript files.
The website is used for the users to securely chat with each other. First there is a room name and then they add their name. Once inside the room a person can send a message. Now when a message is sent, information such as username, message content, and ip address is passed to the chatting server which will then safely encrypt the message. This chatting server gets the key from the Quantum Key Distribution making it safe and secure. 

## Resources:
### What QKD does?
“Quantum key distribution is only used to produce and distribute a key, not to transmit any message data. This key can then be used with any chosen encryption algorithm to encrypt (and decrypt) a message, which can then be transmitted over a standard communication channel. The algorithm most commonly associated with QKD is the one-time pad, as it is provably secure when used with a secret, random key. In real-world situations, it is often also used with encryption using symmetric key algorithms like the Advanced Encryption Standard algorithm.”

### Protocols
1. BB84 Protocol: Using randomly X basis and Z basis.
2. B92 Protocol: Simplified BB84 protocol.
3. Eckert's Protocol E91: Using quantum teleportation and Bell states instead of superposition.

### Privacy Amplification
“Since there is some error, we must assume that Eve may have successfully learned some of the key's bits. QKD protocols can employ a technique known as privacy amplification to reduce the information Eve has about the key down to an arbitrary level.”
