
def main():
    while True:
        print("\nSISTEMA DE GESTION COMERCIAL")
        print("1. Registrar producto")
        print("2. Ver productos")
        print("3. Registrar venta")
        print("4. Consultar inventario")
        print("5. Generar reportes")
        print("6. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion seleccionada:", opcion)


if __name__ == "__main__":
    main()
