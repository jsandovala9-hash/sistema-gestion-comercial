
from productos import menu_productos
from ventas import menu_ventas
from inventario import menu_principal as menu_inventario
from reportes import menu_reportes


def menu_principal():
    while True:
        print("\n===================================")
        print("             FERREX GT")
        print("     SISTEMA DE GESTION COMERCIAL")
        print("===================================")
        print("1. Gestion de productos")
        print("2. Registro de ventas")
        print("3. Control de inventarios")
        print("4. Reportes y estadisticas")
        print("5. Consultar archivos")
        print("6. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            menu_productos()

        elif opcion == "2":
            menu_ventas()

        elif opcion == "3":
            menu_inventario()

        elif opcion == "4":
            menu_reportes()

        elif opcion == "5":
            print("Modulo de archivos pendiente de desarrollo.")

        elif opcion == "6":
            print("Gracias por utilizar FERREX GT.")
            break

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()
