from curses import keyname
from os import urandom
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def key_resizer(key):
    """
    Function [key_sizer] resizes [key] if necessary.
    """
    key = key.encode()
    key = hashlib.sha256(key).digest()
    return key

def encrypter(key, msg):
    """
    Function [encrypter] uses [key] to encrypt a message [msg] according to 
    AES (Advanced Encryption Standard). 
    [msg] must be a string <= 16 bytes. 
    Returns encrypted msg for decryption.
    """
    key = key_resizer(key)
    BS = AES.block_size     

    # Define lambda function to pad msg if insufficient length
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # Pad msg and encode in binary
    msg_array = base64.b64encode(pad(msg).encode('utf8'))   
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key= key, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(iv + cipher.encrypt(msg_array))


def decrypter(key, enc_msg):
    """
    Function [decrypter] uses [key] to decrypt [enc_msg] for the original
    message, according to AES (Advanced Encryption Standard). 
    It removes any padding if padding was added in encrypter.
    Returns original message.
    """
    key = key_resizer(key)
    # Define lambda function to unpad msg to get back original msg
    unpad = lambda s: s[:-ord(s[-1:])]

    enc = base64.b64decode(enc_msg)
    iv = enc[:AES.block_size]

    try:
        cipher = AES.new(key, AES.MODE_CFB, iv)
        plaintext = base64.b64decode(cipher.decrypt(enc[AES.block_size:]))
        plaintext = unpad(plaintext.decode('utf8'))
        print("The message is authentic:" + plaintext)
    except ValueError:
         print("Key incorrect or message corrupted")
    return plaintext

# Main function for testing purposes
def main():
    key = "my_secret_key2342352342342342342342342323423423423434234445455555555556566"
    msg = "Hello World!"
    enc_msg = encrypter(key, msg)
    
    print(decrypter(key, enc_msg))

if __name__ == "__main__":
    main()