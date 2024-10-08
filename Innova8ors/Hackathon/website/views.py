from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, jsonify

views = Blueprint('views',__name__)

@views.route('/about_developers')
def about_developers():
    return render_template("about_us.html")

@views.route('/base')
def base():
    return render_template("base.html")

@views.route('/json')
def json():
    return render_template("json.html")

@views.route('/contact')
def contact_us():
    return render_template("contact_us.html")

@views.route('/bella')
@login_required
def bella():
    return render_template("bella.html")

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/terms')
def terms():
    return render_template("terms.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

@views.route('/research')
def research():
    return render_template("research.html")

@views.route('/guidelines')
def guidelines():
    return render_template("guidelines.html")
