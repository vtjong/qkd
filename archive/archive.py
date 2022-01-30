from curses import keyname
from os import urandom
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def simple_encrypter(key, fullmsg):
    """
    Function [encrypter] uses [key] to encrypt a message [fullmsg] according to 
    AES (Advanced Encryption Standard). Returns encrypted msg for decryption.
    """
    key = key_resizer(key)
    BS = AES.block_size     

    # Define lambda function to pad msg if insufficient length
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # Pad msg and encrypt
    msg_array = base64.b64encode(pad(fullmsg).encode('utf8'))   
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key= key, mode= AES.MODE_CFB,iv= iv)
    enc_msg = base64.b64encode(iv + cipher.encrypt(msg_array))
    
    return enc_msg


def simple_decrypter(key, enc_msg):
    """
    Function [decrypter] uses [key] to decrypt [enc_msg] for the original
    message, according to AES (Advanced Encryption Standard). Removes any padding 
    if padding was added in encrypter. Returns original  message.
    """
    key = key_resizer(key)
    # Define lambda function to unpad msg to get back original msg
    unpad = lambda s: s[:-ord(s[-1:])]
    plaintext = ""

    # Unpad msg and decrypt
    enc = base64.b64decode(enc_msg)
    iv = enc[:AES.block_size]

    try:
        cipher = AES.new(key, AES.MODE_CFB, iv)
        txt_chunk = base64.b64decode(cipher.decrypt(enc[AES.block_size:]))
        txt_chunk = unpad(txt_chunk.decode('utf8'))
        plaintext += txt_chunk
    except ValueError:
        print("Key incorrect or message corrupted")
    return plaintext