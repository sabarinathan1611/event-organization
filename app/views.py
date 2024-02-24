#views.py
from flask import Blueprint, render_template, request, jsonify,redirect,url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid
from .models import Event
from sqlalchemy.exc import SQLAlchemyError

views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@views.route('/')
def home():
	all_events = Event.query.all()
	return render_template('index.html',events=all_events)

@views.route('/event-view',methods=['GET'])
def event_view():
	return render_template('event-view.html')
@views.route('/admin')
@login_required
def admin():
	return render_template('admin.html')

from datetime import datetime, time

from datetime import datetime, time

@views.route('/create_event', methods=['POST', 'GET'])
@login_required
def create_event():
    if request.method == 'POST':
        coordinator_name = request.form['coordinator_name']
        event_name = request.form['event_name']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        place = request.form['place']
        judge = request.form['judge']
        number = request.form['number']
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        
        # Convert string time to datetime.time objects
        start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
        end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None
        
        if 'images1' in request.files:
            images1 = request.files['images1']
            if images1 and allowed_file(images1.filename):
                images1_filename = secure_filename(str(uuid.uuid4()) + "_" + images1.filename)
                images1.save(os.path.join(app.config['UPLOAD_FOLDER'], images1_filename))

        if 'images2' in request.files:
            images2 = request.files['images2']
            if images2 and allowed_file(images2.filename):
                images2_filename = secure_filename(str(uuid.uuid4()) + "_" + images2.filename)
                images2.save(os.path.join(app.config['UPLOAD_FOLDER'], images2_filename))

        print("coordinator_name:", coordinator_name)
        print("event_name:", event_name)
        print("description:", description)
        print("date:", date)
        print("place:", place)
        print("judge:", judge)
        print("number:", number)
        print("start_time:", start_time)
        print("end_time:", end_time)
        print("images1 filename:", images1_filename)
        print("images2 filename:", images2_filename)
        
        # Create and add event to the database
        create = Event(coordinator_name=coordinator_name, event_name=event_name, description=description,
                       date=date, place=place, judge=judge, number=number,
                       start_time=start_time, end_time=end_time,
                       images1=images1_filename, images2=images2_filename)
        db.session.add(create)
        db.session.commit()  
        
        return redirect('/list_event')  # Redirect after successful creation

    return render_template('event_form.html')


@views.route('/list_event')
def list_event():
	all_events = Event.query.all()
	return render_template('list_event.html',events=all_events)

@views.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    # Retrieve the event from the database
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        if request.method == 'POST':
	        event.coordinator_name = request.form['coordinator_name']
	        event.event_name = request.form['event_name']
	        event.description = request.form['description']
	        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
	        event.place = request.form['place']
	        event.judge = request.form['judge']
	        event.number = request.form['number']
	
	        
	        # Convert string time to datetime.time objects
	        start_time = datetime.strptime(request.form['start_time'], '%H:%M:%S').time() if request.form['start_time'] else None
	        end_time = datetime.strptime(request.form['end_time'], '%H:%M:%S').time() if request.form['end_time'] else None
	        event.start_time_str = start_time
	        event.end_time_str = end_time
	        # Handle file uploads
	        if 'images1' in request.files:
	            images1 = request.files['images1']
	            if images1 and allowed_file(images1.filename):
	                filename = secure_filename(str(uuid.uuid4()) + "_" + images1.filename)
	                images1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	                event.images1 = filename

	        if 'images2' in request.files:
	            images2 = request.files['images2']
	            if images2 and allowed_file(images2.filename):
	                filename = secure_filename(str(uuid.uuid4()) + "_" + images2.filename)
	                images2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	                event.images2 = filename
         

        
        db.session.commit()

        
        return redirect(url_for('views.list_event'))

   
    return render_template('edit_event.html', event=event)

@views.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
    except SQLAlchemyError as e:  
        return e

    return redirect(url_for('views.list_event'))