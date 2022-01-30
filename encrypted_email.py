import sendgrid
import os
from sendgrid.helpers.mail import *

SEND_GRID_API_KEY = "API KEY HERE"
sg = sendgrid.SendGridAPIClient(api_key=SEND_GRID_API_KEY)
from_email = Email("vyt3@cornell.edu")
to_email = To("vyt3@cornell.edu")
subject = "Quantum Encrypted Email"
content = Content("text/plain", "Encrypted msg: Welcome to our MIT iQuHACK Project for QuTech.")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())


