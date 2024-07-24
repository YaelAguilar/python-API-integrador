from app.models import crecimiento_planta
from app.db import db


class CrecimientoPlantaController:
    @staticmethod
    def get_all():
        return [planta.to_dict() for planta in crecimiento_planta.query.all()]

    @staticmethod
    def get_by_id(id):
        planta = crecimiento_planta.query.get(id)
        return planta.to_dict() if planta else None

    @staticmethod
    def create(altura):
        new_planta = crecimiento_planta(altura=altura)
        db.session.add(new_planta)
        db.session.commit()
        return new_planta.to_dict()

    @staticmethod
    def update(id, altura):
        planta = crecimiento_planta.query.get(id)
        if planta:
            planta.altura = altura
            db.session.commit()
            return planta.to_dict()
        return None

    @staticmethod
    def delete(id):
        planta = crecimiento_planta.query.get(id)
        if planta:
            db.session.delete(planta)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_last():
        planta = crecimiento_planta.query.order_by(crecimiento_planta.crecimiento_id.desc()).first()
        return planta.to_dict() if planta else None
