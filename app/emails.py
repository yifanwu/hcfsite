from flask import render_template
from flask.ext.mail import Message
from app import mail
from decorators import async
from config import ADMINS, TEST

@async
def send_async_email(msg):
    mail.send(msg)
    
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)
    
def contact_notification(name, subject, email_add, body):
    send_email(subject,
        ADMINS[0],
        #send to self
        ADMINS,
        "Sent by: "+name+" <"+str(email_add)+">\n\n"+body,
        ''
    )
