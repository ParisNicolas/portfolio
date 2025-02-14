from flask import Flask, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

from collections import defaultdict
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
    
    # Formulario de inicio de sesión
    class LoginForm(FlaskForm):
        nombre = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
        constraseña = PasswordField("Password", validators=[DataRequired()])
        submit = SubmitField("Sign in")
    

    @app.cli.command("create_user")
    @click.argument("name")
    @click.argument("password")
    def create_user(name, password):
        new_user = Usuario(nombre=name, contraseña=password)
        db.session.add(new_user)
        db.session.commit()
        click.echo(f"User {name} created successfully")
        


    from app.models import Info,Experiencia,Proyecto,Tecnologia
    @app.route('/', methods=['GET','POST'])
    def home():
        infos = db.session.query(Info).all()
        experiencias = db.session.query(Experiencia).order_by(Experiencia.orden).all()
        proyectos = db.session.query(Proyecto).order_by(Proyecto.orden).all()
        tecnologias = db.session.query(Tecnologia).all()

        infos_obj = {}
        for info in infos:
            if info.data == "extra":
                infos_obj[info.data] = str(info.content).split('.')[:-1]
            elif info.data == "presentacion":
                infos_obj[info.data] = info.content

        experiencias_obj = defaultdict(list)
        for item in experiencias:
            key = getattr(item, "tipo")
            experiencias_obj[key].append(item)

        tecnologias_obj = defaultdict(list)
        for item in tecnologias:
            key = getattr(item, "ubicacion")
            tecnologias_obj[key].append(item)

        for proyecto in proyectos:
            proyecto.tecnologias = proyecto.tecnologias.split(",")


        form = LoginForm()
        if form.validate_on_submit():
            user = Usuario.query.filter_by(name=form.name.data).first()
            if user and user.verificar_contraseña(form.constraseña.data):
                login_user(user)
                return redirect(url_for("editMode"))
            else:
                print("Contraseña o usuario incorrectos")

        return render_template('base.html', 
                               infos=infos_obj, 
                               experiencias=experiencias_obj, 
                               proyectos=proyectos, 
                               tecnologias=tecnologias_obj,
                               form=form)
    
    @login_required
    @app.route('/editMode')
    def editMode():
        return "Aun no"

    with app.app_context():
        # Crea las tablas
        db.create_all()

    return app
