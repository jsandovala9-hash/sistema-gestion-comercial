
productos = {}


def leer_numero(mensaje):
    while True:
        try:
            numero = float(input(mensaje))
            if numero < 0:
                print("No se permiten valores negativos.")
            else:
                return numero
        except ValueError:
            print("Ingrese un numero valido.")


def leer_entero(mensaje):
    while True:
        numero = leer_numero(mensaje)
        if numero.is_integer():
            return int(numero)
        print("Ingrese un numero entero.")


def registrar_producto():
    print("\n--- REGISTRAR PRODUCTO ---")
    codigo = input("Codigo: ").strip()

    if not codigo:
        print("El codigo no puede estar vacio.")
        return

    if codigo in productos:
        print("Error: el codigo ya existe.")
        return

    nombre = input("Nombre: ").strip()
    categoria = input("Categoria: ").strip()

    if not nombre or not categoria:
        print("Nombre y categoria son obligatorios.")
        return

    precio = leer_numero("Precio de venta: Q")
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

    print("Producto registrado correctamente.")


def consultar_producto():
    codigo = input("Ingrese el codigo: ").strip()

    if codigo in productos:
        producto = productos[codigo]
        for campo, valor in producto.items():
            print(f"{campo}: {valor}")
    else:
        print("Producto no encontrado.")


def listar_productos():
    print("\n--- LISTADO DE PRODUCTOS ---")

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos.values():
        print(
            f"{producto['codigo']} | "
            f"{producto['nombre']} | "
            f"Q{producto['precio']:.2f} | "
            f"Cantidad: {producto['cantidad']} | "
            f"Activo: {producto['activo']}"
        )


def modificar_producto():
    codigo = input("Codigo del producto: ").strip()

    if codigo not in productos:
        print("Producto no encontrado.")
        return

    producto = productos[codigo]

    nombre = input("Nuevo nombre: ").strip()
    categoria = input("Nueva categoria: ").strip()

    if not nombre or not categoria:
        print("Nombre y categoria son obligatorios.")
        return

    precio = leer_numero("Nuevo precio: Q")
    cantidad = leer_entero("Nueva cantidad: ")
    stock_minimo = leer_entero("Nuevo stock minimo: ")

    producto["nombre"] = nombre
    producto["categoria"] = categoria
    producto["precio"] = precio
    producto["cantidad"] = cantidad
    producto["stock_minimo"] = stock_minimo

    print("Producto modificado correctamente.")


def desactivar_producto():
    codigo = input("Codigo del producto: ").strip()

    if codigo in productos:
        productos[codigo]["activo"] = False
        print("Producto desactivado correctamente.")
    else:
        print("Producto no encontrado.")


def menu_productos():
    while True:
        print("\n===== GESTION DE PRODUCTOS =====")
        print("1. Registrar producto")
        print("2. Consultar producto")
        print("3. Listar productos")
        print("4. Modificar producto")
        print("5. Desactivar producto")
        print("6. Regresar al menu principal")

        opcion = input("Seleccione una opcion: ")

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
            break
        else:
            print("Opcion invalida. Intente nuevamente.")
