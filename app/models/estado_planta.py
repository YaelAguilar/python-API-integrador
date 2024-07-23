from app.db import db

class EstadoPlanta(db.Model):
    __tablename__ = 'estado_planta'
    estado_id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    conductividad = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)

    estimativos = db.relationship('EstimativoProduccion', backref='estado', lazy=True)
