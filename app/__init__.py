from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
import click
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    """Configuracion"""
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    
    """Inicializacion"""
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    """Get user in each request for more info"""
    from app.models import Usuario
    login_manager.login_view = "login"
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    @app.cli.command("create_user")
    @click.argument("name")
    @click.argument("password")
    def create_user(name, password):
        new_user = Usuario(nombre=name, contraseña=password)
        db.session.add(new_user)
        db.session.commit()
        click.echo(f"User {name} created successfully")
        
        
    @app.route('/')
    def home():
        return render_template('home.html')


    return app
