from app.models.consumo_fertilizante import ConsumoFertilizante
from app.db import db

def calcular_cantidad_fertilizante(sensor_id, cantidad):
    consumo = ConsumoFertilizante(sensor_id=sensor_id, cantidad=cantidad)
    db.session.add(consumo)
    db.session.commit()
    print(f"Fertilizante consumido registrado: Sensor ID {sensor_id}, Cantidad {cantidad} litros")
