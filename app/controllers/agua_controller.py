from app.models.consumo_agua import ConsumoAgua
from app.db import db

def calcular_cantidad_agua(sensor_id, cantidad):
    consumo = ConsumoAgua(sensor_id=sensor_id, cantidad=cantidad)
    db.session.add(consumo)
    db.session.commit()
    print(f"Agua consumida registrada: Sensor ID {sensor_id}, Cantidad {cantidad} litros")
