
# ==========================================
# FERREX GT
# MODULO 1 - GESTION DE PRODUCTOS
# ==========================================

productos = {}


# Validar textos obligatorios
def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print("Error: este campo no puede estar vacio.")


# Validar precios y cantidades decimales
def leer_decimal(mensaje):
    while True:
        try:
            numero = float(input(mensaje))

            if numero < 0 or numero != numero or numero == float("inf"):
                print("Error: ingrese un numero valido y no negativo.")
            else:
                return numero

        except ValueError:
            print("Error: debe ingresar un numero.")


# Validar cantidades enteras
def leer_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))

            if numero < 0:
                print("Error: no se permiten cantidades negativas.")
            else:
                return numero

        except ValueError:
            print("Error: ingrese un numero entero.")


# 1. Registrar productos
def registrar_producto():
    print("\n--- REGISTRAR PRODUCTO ---")

    codigo = leer_texto("Codigo del producto: ").upper()

    if codigo in productos:
        print("Error: el codigo ya esta registrado.")
        return

    nombre = leer_texto("Nombre del producto: ")
    categoria = leer_texto("Categoria: ")
    precio = leer_decimal("Precio de venta Q: ")
    cantidad = leer_entero("Cantidad disponible: ")
    stock_minimo = leer_entero("Stock minimo: ")

    productos[codigo] = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "cantidad": cantidad,
        "stock_minimo": stock_minimo,
        "activo": True
    }

    print("\nProducto registrado correctamente.")


# Mostrar informacion de un producto
def mostrar_producto(producto):
    print("--------------------------------")
    print("Codigo:", producto["codigo"])
    print("Nombre:", producto["nombre"])
    print("Categoria:", producto["categoria"])
    print(f"Precio: Q{producto['precio']:.2f}")
    print("Cantidad:", producto["cantidad"])
    print("Stock minimo:", producto["stock_minimo"])
    print("Estado:", "Activo" if producto["activo"] else "Inactivo")
    print("--------------------------------")


# 2. Consultar producto por codigo
def consultar_producto():
    print("\n--- CONSULTAR PRODUCTO ---")

    codigo = leer_texto("Codigo: ").upper()

    if codigo in productos:
        mostrar_producto(productos[codigo])
    else:
        print("Error: producto no encontrado.")


# 3. Mostrar listado de productos
def listar_productos():
    print("\n--- LISTADO DE PRODUCTOS ---")

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos.values():
        mostrar_producto(producto)


# 4. Modificar producto
def modificar_producto():
    print("\n--- MODIFICAR PRODUCTO ---")

    codigo = leer_texto("Codigo: ").upper()

    if codigo not in productos:
        print("Error: producto no encontrado.")
        return

    producto = productos[codigo]

    print("\nInformacion actual:")
    mostrar_producto(producto)

    print("\nIngrese los nuevos datos:")

    nombre = leer_texto("Nuevo nombre: ")
    categoria = leer_texto("Nueva categoria: ")
    precio = leer_decimal("Nuevo precio Q: ")
    cantidad = leer_entero("Nueva cantidad: ")
    stock_minimo = leer_entero("Nuevo stock minimo: ")

    producto["nombre"] = nombre
    producto["categoria"] = categoria
    producto["precio"] = precio
    producto["cantidad"] = cantidad
    producto["stock_minimo"] = stock_minimo

    print("\nProducto modificado correctamente.")


# 5. Desactivar producto
def desactivar_producto():
    print("\n--- DESACTIVAR PRODUCTO ---")

    codigo = leer_texto("Codigo: ").upper()

    if codigo not in productos:
        print("Error: producto no encontrado.")
        return

    if not productos[codigo]["activo"]:
        print("El producto ya esta desactivado.")
        return

    confirmar = input("¿Desea desactivar el producto? (S/N): ").strip().upper()

    if confirmar == "S":
        productos[codigo]["activo"] = False
        print("Producto desactivado correctamente.")
    else:
        print("Operacion cancelada.")


# Menu del modulo de productos
def menu_productos():
    while True:
        print("\n===================================")
        print("             FERREX GT")
        print("       GESTION DE PRODUCTOS")
        print("===================================")
        print("1. Registrar producto")
        print("2. Consultar producto")
        print("3. Listar productos")
        print("4. Modificar producto")
        print("5. Desactivar producto")
        print("6. Regresar al menu principal")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            registrar_producto()

        elif opcion == "2":
            consultar_producto()

        elif opcion == "3":
            listar_productos()

        elif opcion == "4":
            modificar_producto()

        elif opcion == "5":
            desactivar_producto()

        elif opcion == "6":
            print("Regresando al menu principal...")
            break

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    menu_productos()
