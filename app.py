from app import create_app, run_rabbitmq_subscriber
import ssl
import os
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

app = create_app()

def run_simulation(app):
    with app.app_context():
        from app.utils.rabbitmq_subscriber import simulate_data
        simulate_data()

if __name__ == '__main__':
    print("Ejecutando la aplicación")

    if not hasattr(app, 'thread_rabbitmq'):
        print("Iniciando el hilo del suscriptor de RabbitMQ")
        app.thread_rabbitmq = Thread(target=run_rabbitmq_subscriber, args=(app,))
        app.thread_rabbitmq.start()

    if not hasattr(app, 'thread_simulation'):
        print("Iniciando el hilo de simulación de datos")
        app.thread_simulation = Thread(target=run_simulation, args=(app,))
        app.thread_simulation.start()

    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')
    
    if certfile_path and keyfile_path:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
        app.run(host='0.0.0.0', port=3004, debug=True)
        ssl_context=context
    else:
        app.run(host='0.0.0.0', port=3004, debug=True)

    app.thread_rabbitmq.join()
    app.thread_simulation.join()
