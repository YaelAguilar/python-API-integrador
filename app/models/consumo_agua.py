from app.db import db

class ConsumoAgua(db.Model):
    __tablename__ = 'consumo_agua'
    consumo_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.sensor_id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    litros_por_minuto = db.Column(db.Float, nullable=False)  # Asegúrate de que este campo esté definido y no permita valores nulos

    sensor = db.relationship('Sensor', back_populates='consumos_agua')
