from app.db import db

class CrecimientoPlanta(db.Model):
    __tablename__ = 'crecimiento_planta'
    id = db.Column(db.Integer, primary_key=True)
    altura = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'altura': self.altura
        }
