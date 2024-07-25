import ssl
from flask import Flask
from dotenv import load_dotenv
import logging
import os
from threading import Thread
import pymysql

pymysql.install_as_MySQLdb()

from app import create_app, run_rabbitmq_subscriber

load_dotenv()

def run_websocket_client():
    from app.utils.websocket_client import connect_to_server, start_listening_to_rabbitmq
    connect_to_server()
    start_listening_to_rabbitmq()

if __name__ == '__main__':
    app = create_app()
    print("Ejecutando la aplicación")

    if not hasattr(app, 'thread_rabbitmq'):
        print("Iniciando el hilo del suscriptor de RabbitMQ")
        app.thread_rabbitmq = Thread(target=run_rabbitmq_subscriber, args=(app,))
        app.thread_rabbitmq.start()

    if not hasattr(app, 'thread_websocket'):
        print("Iniciando el cliente WebSocket")
        app.thread_websocket = Thread(target=run_websocket_client)
        app.thread_websocket.start()    
    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')
    
    if certfile_path and keyfile_path:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
        app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
    else:  
        app.run(host='0.0.0.0', port=3004, debug=True)

    app.thread_rabbitmq.join()
    app.thread_websocket.join()
