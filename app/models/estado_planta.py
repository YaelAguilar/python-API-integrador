from app.db import db

class EstadoPlanta(db.Model):
    __tablename__ = 'estado_planta'
    estado_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.sensor_id'), nullable=False)
    humedad = db.Column(db.Float, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    conductividad = db.Column(db.Float, nullable=False)

    sensor = db.relationship('Sensor', back_populates='estados_planta')
