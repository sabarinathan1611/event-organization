from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Admin
from flask import current_app as app 
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

@auth.route('/register',methods=['POST','GET'])
def register():

    return render_template('register.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))