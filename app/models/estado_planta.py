from app.db import db

class EstadoPlanta(db.Model):
    __tablename__ = 'estado_planta'
    estado_id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    conductividad = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)

# Asegúrate de que `EstimativoProduccion` esté definido antes de definir la relación
from app.models.estimativo_produccion import EstimativoProduccion

# Definición de la relación después de importar `EstimativoProduccion`
EstadoPlanta.estimativos = db.relationship('EstimativoProduccion', backref='estado', lazy=True)
