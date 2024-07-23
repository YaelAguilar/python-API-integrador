from app.db import db

class LecturaSensor(db.Model):
    __tablename__ = 'lecturas_sensores'
    lectura_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.sensor_id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
