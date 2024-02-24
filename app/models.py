#models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import secrets


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coordinator_name = db.Column(db.String(50), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    judge = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    images1 = db.Column(db.String(100), nullable=False)
    images2 = db.Column(db.String(100), nullable=False)
    
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('event_tickets', lazy=True))
    dept=db.Column(db.String(100), nullable=False)
    clg=db.Column(db.String(100), nullable=False)
    year=db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Event_basic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name=db.Column(db.String(100))
    clg_name=db.Column(db.String(100))
    dept_name=db.Column(db.String(100))
    club=db.Column(db.String(100))
    event_logo=db.Column(db.String(100), nullable=False)