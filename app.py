from app import create_app
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
    print("Ejecutando la aplicación")
    
    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')

    if not os.path.isfile(certfile_path):
        raise FileNotFoundError(f"Certificado no encontrado: {certfile_path}")
    if not os.path.isfile(keyfile_path):
        raise FileNotFoundError(f"Clave privada no encontrada: {keyfile_path}")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
    
    app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
