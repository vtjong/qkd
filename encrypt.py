from curses import keyname
from os import urandom
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def msg_partitioner(fullmsg):
    """
    Function [msg_partitioner] partitions string msg into 16 byte chunks.
    """
    fullmsg_barr = fullmsg.encode('utf-8')
    count = len(fullmsg_barr)
    num_encryptions = count/16
    len_diff = count % 16

    msg_chunks = [(fullmsg_barr[i:i + 16]).decode('utf-8')
                  for i in range(0, count, 16)]
    return msg_chunks


def key_resizer(key):
    """
    Function [key_sizer] resizes [key] if necessary.
    """
    key = key.encode()
    key = hashlib.sha256(key).digest()
    return key


def encrypter(key, fullmsg):
    """
    Function [encrypter] uses [key] to encrypt a message [fullmsg] according to 
    AES (Advanced Encryption Standard). Returns encrypted msg (array of bytes)
    for decryption.
    """
    key = key_resizer(key)
    BS = AES.block_size

    # Define lambda function to pad msg if insufficient length
    def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # Split msg
    msg_chunks = msg_partitioner(fullmsg)
    enc_msg_chunks = []
    enc_msg_bytearr = b''

    # Pad msg and encrypt
    for msg in msg_chunks:
        msg_array = base64.b64encode(pad(msg).encode('utf8'))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
        enc_msg = base64.b64encode(iv + cipher.encrypt(msg_array))
        enc_msg_chunks.append(enc_msg)
    return enc_msg_chunks


def simple_encrypt(key, fullmsg):
    """
    Function [simple_encrypter] uses [key] to encrypt a message [fullmsg] according to 
    AES (Advanced Encryption Standard). Returns short encrypted msg of bytes
    for decryption.
    """
    key = key_resizer(key)
    BS = AES.block_size

    # Define lambda function to pad msg if insufficient length
    def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # Pad msg and encrypt
    msg_array = base64.b64encode(pad(fullmsg).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
    enc_msg = base64.b64encode(iv + cipher.encrypt(msg_array))
    return enc_msg


def decrypter(key, enc_msg_chunks):
    """
    Function [decrypter] uses [key] to decrypt [enc_msg_chunks] for the original
    message, according to AES (Advanced Encryption Standard). Removes any padding 
    if padding was added in encrypter. Returns original message.
    """
    key = key_resizer(key)
    # Define lambda function to unpad msg to get back original msg
    def unpad(s): return s[:-ord(s[-1:])]
    plaintext = ""

    # Unpad msg and decrypt
    for enc_msg in enc_msg_chunks:
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
