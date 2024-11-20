from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, bcrypt

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def verificar_contraseña(self, contraseña):
        """Verifica si una contraseña coincide con el hash."""
        return bcrypt.check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'



# Modelo de Partidos
class Partido(db.Model):
    __tablename__ = 'partidos'

    #Constantes para definir estados
    ESTADO_PENDIENTE = "Pendiente"
    ESTADO_FINALIZADO = "Finalizado"
    ESTADO_CANCELADO = "Cancelado"

    #Datos informativos
    id = db.Column(db.Integer, primary_key=True)
    deporte = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.DateTime, nullable=True)
    cancha = db.Column(db.Integer, nullable=False)

    #Datos del partido
    equipo1_id = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    equipo2_id = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    puntaje1 = db.Column(db.Integer, nullable=False, default=0)
    puntaje2 = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default=ESTADO_PENDIENTE)

    #Relaciones
    equipo1 = db.relationship('Equipo', foreign_keys=[equipo1_id])
    equipo2 = db.relationship('Equipo', foreign_keys=[equipo2_id])

    def __repr__(self):
        return f'<Partido {self.equipo1} vs {self.equipo2} - {self.puntaje1}:{self.puntaje2}>'
