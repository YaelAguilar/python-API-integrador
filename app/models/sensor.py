from app.db import db

class Sensor(db.Model):
    __tablename__ = 'sensores'
    sensor_id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)

    lecturas = db.relationship('LecturaSensor', backref='sensor', lazy=True)
    consumos_agua = db.relationship('ConsumoAgua', backref='sensor', lazy=True)
    consumos_fertilizante = db.relationship('ConsumoFertilizante', backref='sensor', lazy=True)
