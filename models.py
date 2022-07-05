from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)

    recetas = db.relationship('Receta', backref='usuario', cascade="all, delete-orphan")

    def __str__(self):
        cadena = 'Nombre: ' + self.nombre + ' Correo: ' + self.correo
        return cadena

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    tiempo = db.Column(db.Integer, nullable=False)
    elaboracion = db.Column(db.Text, nullable=False)
    cantidadmegusta = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime) ### clase datetime

    usuarioid = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    ingredientes = db.relationship('Ingrediente', backref='receta', cascade='all, delete-orphan')

    def __gt__(self, otrareceta):
        if self.cantidadmegusta > otrareceta.cantidadmegusta:
            result = True
        else:
            result = False
        return result

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    unidad = db.Column(db.String(30), nullable=False) ## gr, cc, a gusto, etc.

    recetaid= db.Column(db.Integer, db.ForeignKey('receta.id'))