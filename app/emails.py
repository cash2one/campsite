from flask_mail import Message
from app import mail

def send_email(subject, recipients, text_body='', html_body='', sender='hhsc.register@gmail.com'):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)