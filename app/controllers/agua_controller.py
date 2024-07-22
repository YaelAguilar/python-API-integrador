from app.models.consumo_agua import ConsumoAgua
from app.db import db

def calcular_cantidad_agua(sensor_id, cantidad, timestamp):
    print(f"Datos recibidos para agua - Sensor ID: {sensor_id}, Cantidad: {cantidad}, Timestamp: {timestamp}")
    consumo = ConsumoAgua(sensor_id=sensor_id, cantidad=cantidad, timestamp=timestamp)
    db.session.add(consumo)
    db.session.commit()
    print(f"Agua consumida registrada: Sensor ID {sensor_id}, Cantidad {cantidad} litros")
