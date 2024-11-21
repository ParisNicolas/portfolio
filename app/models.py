from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, bcrypt

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    _contraseña = db.Column(db.String(255), nullable=False)  # Atributo privado

    @property
    def contraseña(self):
        """Obtiene la contraseña (no permitido)."""
        raise AttributeError("La contraseña no puede ser leída directamente.")

    @contraseña.setter
    def contraseña(self, valor):
        """Cifra y almacena la contraseña."""
        self._contraseña = bcrypt.generate_password_hash(valor).decode('utf-8')

    def verificar_contraseña(self, contraseña):
        """Verifica si una contraseña coincide con el hash."""
        return bcrypt.check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'



class BaseModel(db.Model):
    __abstract__ = True  # Marca la clase como abstracta, no crea una tabla para ella

    id = db.Column(db.Integer, primary_key=True)
    orden = db.Column(db.Integer, nullable=False)

    def imprimir_elemetos(self):
        elementos = self.query.all()
        for i, elemento in enumerate(elementos):
            print(f"{i}: {elemento}")
        

    @staticmethod
    def asignar_ultimo_orden(model_class):
        """
        Calcula el último valor de `orden` en la tabla del modelo dado y retorna el siguiente número.
        """
        ultimo_orden = db.session.query(db.func.max(model_class.orden)).scalar() or 0
        return ultimo_orden + 1

    @classmethod
    def crear_elemento(cls, **kwargs):
        """
        Crea un nuevo elemento del modelo, asignándole automáticamente el último valor de `orden`.
        """
        kwargs['orden'] = cls.asignar_ultimo_orden(cls)
        nuevo_elemento = cls(**kwargs)
        db.session.add(nuevo_elemento)
        db.session.commit()
        return nuevo_elemento

    def cambiar_orden(self, nuevo_orden):
        """
        Cambia el orden del elemento actual y ajusta los demás elementos para evitar conflictos.
        """
        if nuevo_orden < 1:
            raise ValueError("El orden debe ser mayor o igual a 1.")

        elementos = self.query.order_by(self.__class__.orden).all()

        if nuevo_orden > len(elementos):
            nuevo_orden = len(elementos)

        for elem in elementos:
            if elem.id == self.id:
                continue
            if elem.orden >= nuevo_orden:
                elem.orden += 1

        self.orden = nuevo_orden
        db.session.commit()

    @classmethod
    def reordenar(cls):
        """
        Reorganiza los elementos de la tabla del modelo para garantizar que los valores de `orden` sean consecutivos.
        """
        elementos = cls.query.order_by(cls.orden).all()
        for indice, elemento in enumerate(elementos, start=1):
            elemento.orden = indice
        db.session.commit()



class Info(db.Model):
    __tablename__ = 'infos'

    data = db.Column(db.String(30), primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Info {self.data}: {self.content}>'


class Experiencia(BaseModel):
    __tablename__ = 'experiencias'

    tipo = db.Column(db.String(30), nullable=False)
    titulo = db.Column(db.String(60), nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    fecha = db.Column(db.String(30), nullable=False)

    def imprimir_elemetos(self):
        elementos = self.query.all()
        print("Listando experiencias")
        for i, elemento in enumerate(elementos):
            print(f"Experiencia{i}: {elemento}")

    def __repr__(self):
        return f'<{self.tipo} {self.titulo} {self.descripcion} {self.fecha}>'


class Tecnologia(BaseModel):
    __tablename__ = 'tecnologias'

    tecnologia = db.Column(db.String(50), nullable=False, unique=True)
    ubicacion = db.Column(db.String(50), nullable=False)

    def imprimir_elemetos(self):
        elementos = self.query.all()
        print("Listando tecnologias")
        for i, elemento in enumerate(elementos):
            print(f"Tecnologia{i}: {elemento}")

    def __repr__(self):
        return f'<{self.tecnologia} : {self.ubicacion}>'


class Proyecto(BaseModel):
    __tablename__ = 'proyectos'

    imagen = db.Column(db.String(60), nullable=False)
    url = db.Column(db.String(60), nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    fecha = db.Column(db.String(30), nullable=False)
    tecnologias = db.Column(db.String(120), nullable=False)

    def imprimir_elemetos(self):
        elementos = self.query.all()
        print("Listando proyectos")
        for i, elemento in enumerate(elementos):
            print(f"Proyecto{i}: {elemento}")

    def __repr__(self):
        return f'<{self.titulo} {self.descripcion} {self.fecha} : {self.tecnologias}>'