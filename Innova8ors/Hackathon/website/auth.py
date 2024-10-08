from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

from flask import redirect, url_for

# ... (your existing imports)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)

                # Redirect to 'bella' after successful login
                return redirect(url_for('views.bella'))
            else:
                return render_template("login.html", error_message="Incorrect Password")
        else:
            return render_template("login.html", error_message="Email Does not exist")

    return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template("signup.html", error_message="Email already exists. Please choose a different email.")

        if len(email) < 4 or "@" not in email or "." not in email:
            return render_template("signup.html")

        if len(name) < 3:
            return render_template("signup.html")

        if password != confirmpassword or len(password) < 7 or \
           not any(char.isdigit() for char in password) or \
           not any(char.isupper() for char in password) or \
           not any(char.islower() for char in password) or \
           not any(char in "!@#$%^&*()-_+=" for char in password):
            return render_template("signup.html")

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views.bella'))

    return render_template("signup.html")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.base'))
