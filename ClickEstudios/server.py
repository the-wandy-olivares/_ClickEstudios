import subprocess
import sys

# Comando para ejecutar el servidor
def run_server():
    subprocess.Popen([sys.executable, 'manage.py', 'runserver', '8500'])

# Comando para ejecutar livereload
def run_livereload():
    subprocess.Popen([sys.executable, 'manage.py', 'livereload'])

if __name__ == "__main__":
    run_server()
    run_livereload()