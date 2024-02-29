from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Admin,Ticket,IEEEEvent
from flask import current_app as app 
from collections import defaultdict
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the admin exists in the database
        admin = Admin.query.filter_by(id=1).first()
        if admin:
            # Verify password
            if check_password_hash(admin.password, password):
                login_user(admin)
                return redirect(url_for('views.admin'))  # Redirect to homepage after login
            else:
                return 'Incorrect password'
        else:
            # If admin doesn't exist, create one and add to the database
            hashed_password = generate_password_hash(password)
            new_admin = Admin(username=username,  password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin)
            return redirect(url_for('views.admin'))  
    
    return render_template('login.html')
@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Fetching form data
        tl_name = request.form.get('tl_name')
        tm_name = request.form.get('tm_name')
        tl_roll = request.form.get('tl_roll')
        tm_roll = request.form.get('tm_roll')
        tl_section = request.form.get('tl_section')
        tm_section = request.form.get('tm_section')
        tl_email = request.form.get('tl_email')
        tm_email = request.form.get('tm_email')
        
        # Retrieving the selected radio button value
        event = None
        if 'first' in request.form:
            event = request.form.get('first')
        elif 'second' in request.form:
            event = request.form.get('second')
        elif 'third' in request.form:
            event = request.form.get('third')
        elif 'fourth' in request.form:
            event = request.form.get('fourth')
        
        # Debug print all form values
        print("Team Leader Name:", tl_name)
        print("Team Member Name:", tm_name)
        print("Team Leader Roll:", tl_roll)
        print("Team Member Roll:", tm_roll)
        print("Team Leader Section:", tl_section)
        print("Team Member Section:", tm_section)
        print("Team Leader Email:", tl_email)
        print("Team Member Email:", tm_email)
        print("Selected Event:", event)
        
        # Check if team leader has already registered for the event
        team_leader_event = IEEEEvent.query.filter_by(team_leader_roll=tl_roll, event_type=event).first()
        if team_leader_event:
            return "Team leader has already registered for this event."

        # Check if team member has already registered for the event
        team_member_event = IEEEEvent.query.filter_by(team_member_roll=tm_roll, event_type=event).first()
        if team_member_event:
            return "Team member has already registered for this event."

        # Check if team leader has already registered for two events
        team_leader_events = IEEEEvent.query.filter(IEEEEvent.team_leader_roll == tl_roll).count()
        if team_leader_events >= 2:
            return "Team leader has already registered for two events."

        # Check if team member has already registered for two events
        team_member_events = IEEEEvent.query.filter(IEEEEvent.team_member_roll == tm_roll).count()
        if team_member_events >= 2:
            return "Team member has already registered for two events."

        # Creating a new Event object and adding it to the database session
        new_event = IEEEEvent(
            team_leader_name=tl_name,
            team_member_name=tm_name,
            team_leader_roll=tl_roll,
            team_member_roll=tm_roll,
            team_leader_section=tl_section,
            team_member_section=tm_section,
            team_leader_email=tl_email,
            team_member_email=tm_email,
            event_type=event
        )
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('views.home'))

    
    return render_template('register.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))