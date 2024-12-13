import subprocess
import webbrowser
import time
import os

def run_server():
    # Iniciar el servidor de Django
    subprocess.Popen(['py', 'manage.py', 'runserver'])

def open_browser():
    # Esperar unos segundos para asegurarse de que el servidor esté en funcionamiento
    time.sleep(5)
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    run_server()
    open_browser()
    # Mantener el script en ejecución
    input("Presiona Enter para cerrar...")