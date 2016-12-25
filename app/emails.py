from flask_mail import Message
from app import mail, app
from .decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body='', html_body='', sender='hhsc.register@gmail.com', attach=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # print attach
    # if attach:
    #     with app.open_resource(str(attach)) as fp:
    #         msg.attach("Document", "pdf", fp.read())
    send_async_email(app, msg)