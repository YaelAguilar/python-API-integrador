from app.db import db

class ConsumoAgua(db.Model):
    __tablename__ = 'consumo_agua'
    consumo_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.sensor_id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())