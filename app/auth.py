from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Admin,Ticket,Event
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
        
        name = request.form['name']
        email = request.form['email']
        event_name = request.form['event_name']
        dept = request.form['dept']
        team_name = request.form['team_name']
        team_members = request.form['team_members']
        clg = request.form['clg']
        year = request.form['year']

        # Find the event by event_name
        event = Event.query.filter_by(event_name=event_name).first()
        if not event:
            return "Error: Event not found."

        # Get the event_id
        event_id = event.id

        # Split the team members' roll numbers and store them in a list
        team_members_rollnum_list = [roll.strip() for roll in team_members.split(',')]

        # Create a dictionary to track the number of events each team member has registered for
        member_event_count = defaultdict(int)

        # Check if the team members are already registered for the same event
        for member_rollnum in team_members_rollnum_list:
            existing_ticket = Ticket.query.filter_by(event_id=event_id, rollnum=member_rollnum).first()
            if existing_ticket:
                return "Error: One of the team members is already registered for this event."

            # Increment the event count for the current team member
            member_event_count[member_rollnum] += 1

        # Check if any team member has already registered for two events
        for member_rollnum, count in member_event_count.items():
            if count >= 2:
                return "Error: {} has already registered for the maximum number of events.".format(member_rollnum)

        # Create Ticket objects for each team member and save them to the database
        for member_rollnum in team_members_rollnum_list:
            ticket = Ticket(rollnum=member_rollnum, name=name, email=email, event_id=event_id,
                            dept=dept, team_name=team_name, team_members=team_members,
                            clg=clg, year=year)
            db.session.add(ticket)

        db.session.commit()
        return "Success: Tickets registered successfully."

    return render_template('register.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))