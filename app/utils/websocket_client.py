import socketio
import json

WS_SERVER_URL = "https://wss.soursop.lat"

sio = socketio.Client()

def connect_to_server():
    try:
        sio.connect(WS_SERVER_URL)
        print("Conectado al servidor WebSocket")
    except Exception as e:
        print(f"Error al conectar al servidor WebSocket: {e}")

def send_to_websocket(event_type, data):
    try:
        if not sio.connected:
            connect_to_server()
        sio.emit(event_type, data)
    except Exception as e:
        print(f"Error al enviar datos a WebSocket: {e}")

def disconnect_from_server():
    try:
        sio.disconnect()
    except Exception as e:
        print(f"Error al desconectar del servidor WebSocket: {e}")
