#function.py
from flask_mail import Message
from flask import url_for,render_template
from . import mail
import os
from . import mail
from .models import Admin
from . import db
from werkzeug.security import generate_password_hash

def send_email(to, subject, html):
    sender=''
    print("SENDER MAIL: ",sender)
    msg = Message(subject, sender=sender, recipients=[to])
    msg.html = html
    mail.send(msg)





def create_admi(username,password):

    admin = Admin.query.filter_by(username='username').first()
    if not admin:
        
        admin_password = password
        hashed_password = generate_password_hash(admin_password)
        
        new_admin = Admin(username=username,  password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()