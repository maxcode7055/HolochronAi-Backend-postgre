
from flask_mail import Message
from .flask_mail_config import mail


def send_email(subject, recipients, html_content):
    
    msg = Message(subject,sender='hello@holochronai.com', recipients=[recipients])
    msg.html = html_content
    mail.send(msg)
    return True

def send_multiple_email(subject, recipients, html_content):

    msg = Message(subject,sender='hello@holochronai.com', recipients=recipients)
    msg.html = html_content
    mail.send(msg)
    return True