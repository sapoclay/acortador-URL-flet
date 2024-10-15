import os
import subprocess
import sys

# Obtener el directorio donde se encuentra el archivo run_app.py
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Nombre del entorno virtual
VENV_DIR = os.path.join(DIRECTORIO_SCRIPT, "venv")  # Crear la ruta completa

# Determinar el ejecutable de Python dentro del entorno virtual
def obtener_python_ejecutable():
    if os.name == 'nt':  # Windows
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:  # Linux/macOS
        return os.path.join(VENV_DIR, "bin", "python")

# Comprobar si el entorno virtual está creado
def entorno_virtual_existe():
    return os.path.isdir(VENV_DIR)

# Crear el entorno virtual
def crear_entorno_virtual():
    print("Creando el entorno virtual...")
    subprocess.run([sys.executable, "-m", "virtualenv", VENV_DIR], check=True)

# Instalar pip si no está instalado
def asegurar_pip(python_executable):
    try:
        subprocess.run([python_executable, "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("pip no está instalado. Intentando instalar pip manualmente...")
        try:
            # Descargar get-pip.py
            subprocess.run([sys.executable, "-c", "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')"], check=True)
            # Instalar pip usando get-pip.py
            subprocess.run([python_executable, "get-pip.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar pip manualmente: {e}")
            raise

# Instalar las dependencias desde requirements.txt
def instalar_dependencias(python_executable):
    print("Instalando dependencias...")
    asegurar_pip(python_executable)
    
    ruta_requirements = os.path.join(DIRECTORIO_SCRIPT, "requirements.txt")
    
    if os.path.exists(ruta_requirements):
        subprocess.run([python_executable, "-m", "pip", "install", "-r", ruta_requirements], check=True)
    else:
        print("No se encontró el archivo requirements.txt.")

# Comprobar si flet está instalado en el entorno virtual
def flet_instalado(python_executable):
    try:
        result = subprocess.run(
            [python_executable, "-m", "pip", "show", "flet"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return "Name: flet" in result.stdout
    except FileNotFoundError:
        print(f"Archivo no encontrado: {python_executable}")
        return False
    except subprocess.CalledProcessError:
        return False

# Mostrar mensajes usando Flet si está instalado
def mostrar_mensaje(mensaje):
    python_executable = obtener_python_ejecutable()
    
    if flet_instalado(python_executable):
        try:
            import flet as ft
            def main(page: ft.Page):
                page.add(ft.Text(mensaje))
                page.update()
            ft.app(target=main)
        except ImportError:
            print("Error al importar Flet.")
    else:
        print(mensaje)

# Ejecutar el script principal dentro del entorno virtual
def ejecutar_app():
    python_executable = obtener_python_ejecutable()
    
    ruta_main = os.path.join(DIRECTORIO_SCRIPT, "main.py")
    
    if os.path.isfile(python_executable):
        subprocess.run([python_executable, ruta_main], check=True)
    else:
        print(f"El ejecutable no se encuentra: {python_executable}")

# Comprobar si el paquete python3-virtualenv está instalado
def verificar_virtualenv_instalado():
    try:
        subprocess.run(["dpkg", "-s", "python3-virtualenv"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Lógica principal
def main():
    python_executable = obtener_python_ejecutable()

    if not entorno_virtual_existe():
        # Si no existe el entorno virtual, crearlo e instalar dependencias
        print("El entorno virtual no existe. Creando uno nuevo...")
        if not verificar_virtualenv_instalado():
            print("El paquete python3-virtualenv no está instalado. Por favor, instálalo y vuelve a intentarlo.")
            sys.exit(1)
        crear_entorno_virtual()
        instalar_dependencias(python_executable)
    else:
        # Si el entorno virtual ya existe
        print("El entorno virtual ya existe.")
        
        # Instalar dependencias si no lo hicimos aún
        instalar_dependencias(python_executable)

        # Comprobar si Flet está instalado
        if not flet_instalado(python_executable):
            print("Flet no está instalado. Instalando Flet...")
            subprocess.run([python_executable, "-m", "pip", "install", "flet"], check=True)
            print("Flet instalado correctamente.")
    
    # Ejecutar la aplicación
    ejecutar_app()

# Ejecutar el script
if __name__ == "__main__":
    main()
