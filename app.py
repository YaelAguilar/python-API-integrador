from app import create_app, run_rabbitmq_subscriber
import ssl
import os
from dotenv import load_dotenv
from threading import Thread

from app.config.rabbitmq import start_consuming

load_dotenv()

app = create_app()

def run_rabbitmq_subscriber(app):
    with app.app_context():
        app.logger.info("Iniciando el suscriptor de RabbitMQ")
        start_consuming()

if __name__ == '__main__':
    print("Ejecutando la aplicación")

    if not hasattr(app, 'thread_rabbitmq'):
        print("Iniciando el hilo del suscriptor de RabbitMQ")
        app.thread_rabbitmq = Thread(target=run_rabbitmq_subscriber, args=(app,))
        app.thread_rabbitmq.start()

    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
    
    app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
    
    app.thread_rabbitmq.join()
