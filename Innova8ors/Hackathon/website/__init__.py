from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .image_gen import image_gen_bp

db = SQLAlchemy()  # Instantiate SQLAlchemy
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'We are going to build a bella ecosystem #9530776688,7206333935 :) !!!!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(image_gen_bp)

    from .models import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    create_database(app) 

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
