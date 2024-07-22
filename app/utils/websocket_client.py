import websocket
import json

WS_SERVER_URL = "wss://wss.soursop.lat"

def send_to_websocket(event_type, data):
    try:
        ws = websocket.create_connection(WS_SERVER_URL)
        message = json.dumps({
            'type': event_type,
            'data': data
        })
        ws.send(message)
        ws.close()
    except Exception as e:
        print(f"Error al enviar datos a WebSocket: {e}")
