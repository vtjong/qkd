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
    def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # Pad msg and encrypt
    msg_array = base64.b64encode(pad(fullmsg).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
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
    def unpad(s): return s[:-ord(s[-1:])]
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

    # email1 = Encrypted_Mail(key, from_email, to_email, subject, msg_plaintext)
    email_subj = "B9v8wBkTSaYAfMAk2gzQemaMS6awnMQ1cPg6tarfMMjc+VELhuM2Sw=="
    email_subj = msg_partitioner(email_subj)
    print(decrypter(key=key, enc_msg_chunks=email_subj))
    email_txt = "Fp4j9gcDRMBtChobNCPtTjFXxGn7xjQVHKmxw3vwqy2CXz3FF4FY2VbQmO+4UskyYlq9sHB3oHFBWGrNESify1d34ezvIhNkUtHcMusbhwW2fphnfmvU8KTF77GOq9AkWgIBj2eQ5eGmtLe/a8O4mlMfxhlYjaf2r4MRYgb6Q4QzPWzbd+eaJmp+tYMkMdacvcyPaLMvimr9NkX7gHOdwEiWgUl86ZqZt8J9UWpN0cfEvIEermtwsRCgtNNQh6mzdpY0OBlEnRcnYwpRjJaPt+pv0mdV/pbSaW+yfH1J1LwvEIWEVJ6V0BlK9cRAR5m2PAY/WEV2waGG66W2DjSvOYIqH13RzAYwI7KaEISCeHZ1eTd2JtwTx1n6XaUoaQYQu2a5xGak5fkrviAhh4QPcaiMITIeReuhlFcuxxmCSnD+BL46mKCr3ezTRqn5R4Ut4BXDS+Kg9jtv59San19IaqbKjg5tFQRs1XuJNByS5ds9miBe8BBmPyVoLNXYl8jFlas+nfkIX22mgRdTqklP78mQBhvEQwk2m05WSAEJzVoFhRgMSQI/hggpgbT1XT6f6r9hpdalnWSjPG3wIUqa4Q50C57f1WCIoDaUb1nNdUF73TIPwTWIf8Vy9NfHIWIw9vHF6MHv2xU5RhuIC4dwM3na4QqGk32AcKHerysQJXajEJJSod7Y5g=="
    email_txt = msg_partitioner(email_txt)
    print(decrypter(key=key, enc_msg_chunks=email_txt))
