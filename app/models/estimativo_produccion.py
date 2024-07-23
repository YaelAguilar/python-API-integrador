from app.db import db

class EstimativoProduccion(db.Model):
    __tablename__ = 'estimativo_produccion'
    estimativo_id = db.Column(db.Integer, primary_key=True)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_planta.estado_id'), nullable=False)
    nivel_produccion = db.Column(db.String(50), nullable=False)
