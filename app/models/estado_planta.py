from app.db import db

class EstadoPlanta(db.Model):
    __tablename__ = 'estado_planta'
    estado_id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    potasio = db.Column(db.Float, nullable=False)
    nitrogeno = db.Column(db.Float, nullable=False)
    conductividad = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    estimativos = db.relationship('EstimativoProduccion', backref='estado', lazy=True)
