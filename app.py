import ssl
from flask import Flask
from dotenv import load_dotenv
import logging
import os
import pymysql

pymysql.install_as_MySQLdb()
from app import create_app

load_dotenv()

if __name__ == '__main__':

    app = create_app()
    print("Ejecutando la aplicación")

    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')

    if certfile_path and keyfile_path:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
        app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
    else:
        app.run(host='0.0.0.0', port=3004, debug=True)
