from app.db import db

class CrecimientoPlanta(db.Model):
    __tablename__ = 'crecimiento_planta'
    crecimiento_id = db.Column(db.Integer, primary_key=True)
    altura = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'crecimiento_id': self.crecimiento_id,
            'altura': self.altura
        }
