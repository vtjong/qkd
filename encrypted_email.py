import sendgrid
import os
import base64
import pickle
from sendgrid.helpers.mail import *
from encrypt import encrypter, decrypter, msg_partitioner, simple_encrypt


class Encrypted_Mail():
    def __init__(self, key, from_email, to_email, subject, textmsg):
        self.key = key
        self.from_email = from_email
        self.to_email = to_email
        self.API_key()  # validate API key to use sendgrid

    def API_key(self):
        SEND_GRID_API_KEY = "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"
        self.sg = sendgrid.SendGridAPIClient(api_key=SEND_GRID_API_KEY)

    def send_encrypted_email(self, subject, textmsg):
        encrypted_subject = encrypter(key=self.key, fullmsg=subject)
        self.encrypted_subject = encrypted_subject
        encrypted_subject = ''.join(e.decode('utf8')
                                    for e in encrypted_subject)
        encrypted_msg = encrypter(key=self.key, fullmsg=textmsg)
        self.encrypted_msg = encrypted_msg
        encrypted_msg = ''.join(e.decode('utf8') for e in encrypted_msg)
        content = Content("text/plain", encrypted_msg)
        mail = Mail(self.from_email, self.to_email, encrypted_subject, content)

        print("Email successfully sent to: ", self.to_email)
        print("Encrypted subject: ", encrypted_subject)
        print("Encrypted message: ", encrypted_msg)
        response = self.sg.client.mail.send.post(request_body=mail.get())

    def generate_attachment(self, attachment_name, encrypted_subject, encrypted_msg):
        with open('sample_attachment.pkl', 'wb') as f:
            pickle.dump(encrypted_msg, f)

    def send_encrypted_attachment(self, subject, textmsg, filepath):
        encrypted_subject = simple_encrypt(key=self.key, fullmsg=subject)
        encrypted_msg = encrypter(key=self.key, fullmsg=textmsg)

        self.generate_attachment(encrypted_subject, encrypted_msg, filepath)
        filepath = 'sample_attachment.pdf'
        with open(filepath, 'rb') as f:
            data = f.read()

        # Encode contents of file as Base 64
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.content = encoded
        attachment.type = "sample_attachment/pdf"
        attachment.filename = "sample_attachment.pdf"
        attachment.disposition = "sample_attachment"
        attachment.content_id = "PDF file"
        mail = Mail(self.from_email, self.to_email,
                    subject, "content")
        mail.add_attachment(attachment)
        response = self.sg.client.mail.send.post(request_body=mail.get())

    def get_encrypted_email(self, key):
        """
        Note that this method is currently hacky and for demo purposes.
        Working model with be updated shortly. 
        """
        subject = decrypter(key, self.encrypted_subject)
        msg = decrypter(key, self.encrypted_msg)
        print("\n------------Begin decrypted message------------")
        print("Subject: ", subject)
        print("Email Body: ", msg)
