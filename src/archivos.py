
# ==========================================
# FERREX GT
# MODULO DE MANEJO DE ARCHIVOS
# ==========================================

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ARCHIVO_INVENTARIO = BASE_DIR / "inventario_ferreteria.json"
ARCHIVO_VENTAS = BASE_DIR / "ventas.json"


def leer_archivo(ruta):
    if not ruta.exists():
        print("El archivo aun no existe.")
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except (OSError, json.JSONDecodeError) as error:
        print("Error al leer el archivo:", error)
        return None


def guardar_archivo(ruta, datos):
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        print("Informacion guardada correctamente.")
        return True

    except OSError as error:
        print("Error al guardar:", error)
        return False


def consultar_inventario():
    print("\n===== ARCHIVO DE INVENTARIO =====")

    datos = leer_archivo(ARCHIVO_INVENTARIO)

    if datos is not None:
        print(json.dumps(datos, indent=4, ensure_ascii=False))


def consultar_ventas():
    print("\n===== ARCHIVO DE VENTAS =====")

    datos = leer_archivo(ARCHIVO_VENTAS)

    if datos is not None:
        print(json.dumps(datos, indent=4, ensure_ascii=False))


def menu_archivos():
    while True:
        print("\n===================================")
        print("             FERREX GT")
        print("        CONSULTA DE ARCHIVOS")
        print("===================================")
        print("1. Consultar archivo de inventario")
        print("2. Consultar archivo de ventas")
        print("3. Regresar al menu principal")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            consultar_inventario()

        elif opcion == "2":
            consultar_ventas()

        elif opcion == "3":
            break

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    menu_archivos()
