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
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
    
    app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
