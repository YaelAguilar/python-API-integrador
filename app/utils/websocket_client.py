import socketio
import json
import time
import jwt
import os
from dotenv import load_dotenv

from app.config.rabbitmq import get_rabbitmq_connection

load_dotenv()

WS_SERVER_URL = "https://wss.soursop.lat:3005"
JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret_default')

sio = socketio.Client()

def create_jwt_token():
    token = jwt.encode({'userId': '123'}, JWT_SECRET, algorithm='HS256')
    return token

def connect_to_server():
    if sio.connected:
        print("Cliente WebSocket ya está conectado.")
        return
    try:
        print("Intentando conectar al servidor WebSocket...")
        token = create_jwt_token()
        sio.connect(WS_SERVER_URL, headers={'Authorization': f'Bearer {token}'}, wait_timeout=10)
        print("Conectado al servidor WebSocket")
    except Exception as e:
        print(f"Error al conectar al servidor WebSocket: {e}")
        disconnect_from_server()
        time.sleep(5)
        connect_to_server()

def send_to_websocket(event_type, data):
    try:
        if not sio.connected:
            connect_to_server()
        print(f"Enviando datos a WebSocket: {event_type} - {data}")
        sio.emit(event_type, data)
        print(f"Datos enviados a WebSocket: {data}")
    except Exception as e:
        print(f"Error al enviar datos a WebSocket: {e}")

def disconnect_from_server():
    if sio.connected:
        try:
            sio.disconnect()
            print("Desconectado del servidor WebSocket")
        except Exception as e:
            print(f"Error al desconectar del servidor WebSocket: {e}")
    else:
        print("Cliente WebSocket ya está desconectado.")

@sio.event
def connect():
    print("Conectado al servidor WebSocket")

@sio.event
def connect_error(data):
    print(f"Error de conexión: {data}")

@sio.event
def disconnect():
    print("Desconectado del servidor WebSocket")

def start_listening_to_rabbitmq():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Datos recibidos de RabbitMQ: {data}")
        send_to_websocket(method.routing_key, data)

    channel.basic_consume(queue='flujoAgua', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='nivelAgua', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='nivelFertilizante', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='ph', on_message_callback=callback, auto_ack=True)
    print("Esperando mensajes de RabbitMQ...")
    channel.start_consuming()

if __name__ == "__main__":
    connect_to_server()
    start_listening_to_rabbitmq()
