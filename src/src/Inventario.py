# CONTROL DE INVENTARIO PARA FERRETERIA

import json
import os
from pathlib import Path
from datetime import datetime

ARCHIVO = str(Path(__file__).resolve().parent / "inventario_ferreteria.json")

PRODUCTOS_INICIALES = {
    "FER001": {"nombre": "Cemento", "categoria": "Construccion", "unidad": "bolsa", "cantidad": 30, "stock_minimo": 10, "precio": 85.00},
    "FER002": {"nombre": "Clavos de 2 pulgadas", "categoria": "Ferreteria", "unidad": "libra", "cantidad": 20, "stock_minimo": 5, "precio": 12.00},
    "FER003": {"nombre": "Tornillos para madera", "categoria": "Ferreteria", "unidad": "caja", "cantidad": 25, "stock_minimo": 5, "precio": 18.50},
    "FER004": {"nombre": "Martillo", "categoria": "Herramientas", "unidad": "unidad", "cantidad": 12, "stock_minimo": 3, "precio": 45.00},
    "FER005": {"nombre": "Destornillador", "categoria": "Herramientas", "unidad": "unidad", "cantidad": 15, "stock_minimo": 3, "precio": 20.00},
    "FER006": {"nombre": "Alicate", "categoria": "Herramientas", "unidad": "unidad", "cantidad": 10, "stock_minimo": 2, "precio": 35.00},
    "FER007": {"nombre": "Brocha de 3 pulgadas", "categoria": "Pintura", "unidad": "unidad", "cantidad": 18, "stock_minimo": 4, "precio": 15.00},
    "FER008": {"nombre": "Pintura blanca", "categoria": "Pintura", "unidad": "galon", "cantidad": 14, "stock_minimo": 3, "precio": 110.00},
    "FER009": {"nombre": "Tubo PVC de 1 pulgada", "categoria": "Plomeria", "unidad": "unidad", "cantidad": 22, "stock_minimo": 5, "precio": 28.00},
    "FER010": {"nombre": "Codo PVC de 1 pulgada", "categoria": "Plomeria", "unidad": "unidad", "cantidad": 40, "stock_minimo": 10, "precio": 4.50},
    "FER011": {"nombre": "Cable electrico", "categoria": "Electricidad", "unidad": "metro", "cantidad": 100, "stock_minimo": 20, "precio": 6.75},
    "FER012": {"nombre": "Interruptor electrico", "categoria": "Electricidad", "unidad": "unidad", "cantidad": 16, "stock_minimo": 4, "precio": 12.50},
    "FER013": {"nombre": "Tomacorriente", "categoria": "Electricidad", "unidad": "unidad", "cantidad": 20, "stock_minimo": 5, "precio": 14.00},
    "FER014": {"nombre": "Llave ajustable", "categoria": "Herramientas", "unidad": "unidad", "cantidad": 8, "stock_minimo": 2, "precio": 55.00},
    "FER015": {"nombre": "Candado", "categoria": "Seguridad", "unidad": "unidad", "cantidad": 13, "stock_minimo": 3, "precio": 25.00}
}


def guardar_datos(inventario, movimientos):
    datos = {
        "inventario": inventario,
        "movimientos": movimientos
    }

    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except OSError as error:
        print("Error al guardar el inventario:", error)
        return False


def cargar_datos():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            inventario = datos.get("inventario", {})
            movimientos = datos.get("movimientos", [])

            if isinstance(inventario, dict) and inventario:
                return inventario, movimientos

        except (OSError, json.JSONDecodeError):
            print("No se pudo leer el archivo de inventario.")

    inventario = {
        codigo: producto.copy()
        for codigo, producto in PRODUCTOS_INICIALES.items()
    }

    movimientos = []

    for codigo, producto in inventario.items():
        registrar_movimiento(
            movimientos,
            "INVENTARIO INICIAL",
            codigo,
            producto["nombre"],
            producto["cantidad"],
            "Carga inicial del sistema"
        )

    guardar_datos(inventario, movimientos)
    return inventario, movimientos


def normalizar_codigo(texto):
    codigo = texto.strip().upper()

    # Acepta FER004, fer004 y 004.
    if codigo.isdigit() and len(codigo) == 3:
        codigo = "FER" + codigo

    return codigo


def leer_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje).strip())

            if numero < minimo:
                print("Ingrese un numero igual o mayor que", minimo)
            else:
                return numero

        except ValueError:
            print("Entrada invalida. Escriba un numero entero.")


def leer_precio(mensaje):
    while True:
        try:
            precio = float(input(mensaje).strip().replace(",", "."))

            if precio < 0:
                print("El precio no puede ser negativo.")
            else:
                return round(precio, 2)

        except ValueError:
            print("Ingrese un precio valido, por ejemplo 25.50.")


def registrar_movimiento(
    movimientos, tipo, codigo, producto, cantidad, detalle=""
):
    movimientos.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "codigo": codigo,
        "producto": producto,
        "cantidad": cantidad,
        "detalle": detalle
    })


def registrar_producto(inventario, movimientos):
    print("\n--- REGISTRAR PRODUCTO ---")

    codigo = normalizar_codigo(
        input("Codigo del producto (ej. FER016): ")
    )

    if not codigo:
        print("El codigo no puede estar vacio.")
        return

    if codigo in inventario:
        print("Ese codigo ya existe.")
        return

    nombre = input("Nombre del producto: ").strip()

    if not nombre:
        print("El nombre no puede estar vacio.")
        return

    categoria = input("Categoria: ").strip() or "General"
    unidad = input("Unidad: ").strip() or "unidad"
    cantidad = leer_entero("Cantidad inicial: ", 0)
    minimo = leer_entero("Stock minimo: ", 0)
    precio = leer_precio("Precio unitario en Q: ")

    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "unidad": unidad,
        "cantidad": cantidad,
        "stock_minimo": minimo,
        "precio": precio
    }

    registrar_movimiento(
        movimientos,
        "REGISTRO",
        codigo,
        nombre,
        cantidad,
        "Producto registrado"
    )

    guardar_datos(inventario, movimientos)
    print("Producto registrado correctamente con codigo", codigo)


def consultar_existencias(inventario):
    print("\n--- CONSULTAR EXISTENCIAS ---")

    if not inventario:
        print("No hay productos registrados.")
        return

    print("-" * 88)
    print(
        f"{'CODIGO':<10} {'PRODUCTO':<28} "
        f"{'CANTIDAD':>10} {'UNIDAD':<12} "
        f"{'PRECIO Q':>10} {'VALOR Q':>12}"
    )
    print("-" * 88)

    for codigo, producto in sorted(inventario.items()):
        cantidad = producto.get("cantidad", 0)
        precio = producto.get("precio", 0.0)
        unidad = producto.get("unidad", "unidad")
        valor = cantidad * precio

        print(
            f"{codigo:<10} "
            f"{producto.get('nombre', 'Sin nombre'):<28.28} "
            f"{cantidad:>10} "
            f"{unidad:<12.12} "
            f"{precio:>10.2f} "
            f"{valor:>12.2f}"
        )

    print("-" * 88)


def buscar_producto(inventario):
    print("\n--- BUSCAR PRODUCTO ---")

    busqueda = input(
        "Ingrese el codigo (FER004 o 004) o nombre: "
    ).strip()

    if not busqueda:
        print("Debe ingresar un codigo o nombre.")
        return

    codigo_buscado = normalizar_codigo(busqueda)
    encontrados = []

    for codigo, producto in inventario.items():
        nombre = producto.get("nombre", "")

        if codigo.upper() == codigo_buscado:
            encontrados.append((codigo, producto))
        elif busqueda.lower() in nombre.lower():
            encontrados.append((codigo, producto))

    if not encontrados:
        print("Producto no encontrado.")
        return

    for codigo, producto in encontrados:
        print("\nCodigo:", codigo)
        print("Nombre:", producto.get("nombre", ""))
        print("Categoria:", producto.get("categoria", ""))
        print("Cantidad actual:", producto.get("cantidad", 0))
        print("Unidad:", producto.get("unidad", "unidad"))
        print("Stock minimo:", producto.get("stock_minimo", 0))
        print(
            "Precio unitario: Q",
            f"{producto.get('precio', 0.0):.2f}"
        )


def registrar_entrada(inventario, movimientos):
    print("\n--- REGISTRAR ENTRADA ---")

    codigo = normalizar_codigo(
        input("Codigo del producto (FER001 o 001): ")
    )

    if codigo not in inventario:
        print("Producto no encontrado.")
        return

    cantidad = leer_entero("Cantidad que ingresa: ", 1)
    producto = inventario[codigo]

    producto["cantidad"] = producto.get("cantidad", 0) + cantidad

    registrar_movimiento(
        movimientos,
        "ENTRADA",
        codigo,
        producto["nombre"],
        cantidad,
        "Entrada de mercaderia"
    )

    guardar_datos(inventario, movimientos)

    print("Entrada registrada correctamente.")
    print("Nueva existencia:", producto["cantidad"])


def registrar_salida(inventario, movimientos):
    print("\n--- REGISTRAR SALIDA ---")

    codigo = normalizar_codigo(
        input("Codigo del producto (FER001 o 001): ")
    )

    if codigo not in inventario:
        print("Producto no encontrado.")
        return

    producto = inventario[codigo]
    disponible = producto.get("cantidad", 0)

    print("Producto:", producto["nombre"])
    print("Existencia actual:", disponible)

    cantidad = leer_entero("Cantidad que sale: ", 1)

    if cantidad > disponible:
        print("No hay suficiente existencia. Operacion cancelada.")
        return

    producto["cantidad"] = disponible - cantidad

    registrar_movimiento(
        movimientos,
        "SALIDA",
        codigo,
        producto["nombre"],
        cantidad,
        "Salida de mercaderia"
    )

    guardar_datos(inventario, movimientos)

    print("Salida registrada correctamente.")
    print("Nueva existencia:", producto["cantidad"])


def actualizar_cantidad(inventario, movimientos):
    print("\n--- ACTUALIZAR CANTIDAD ---")

    codigo = normalizar_codigo(
        input("Codigo del producto (FER001 o 001): ")
    )

    if codigo not in inventario:
        print("Producto no encontrado.")
        return

    producto = inventario[codigo]
    cantidad_anterior = producto.get("cantidad", 0)

    print("Producto:", producto["nombre"])
    print("Cantidad actual:", cantidad_anterior)

    nueva_cantidad = leer_entero(
        "Ingrese la NUEVA cantidad total: ", 0
    )

    diferencia = nueva_cantidad - cantidad_anterior

    # Actualiza el mismo inventario que consulta la opcion 2.
    inventario[codigo]["cantidad"] = nueva_cantidad

    registrar_movimiento(
        movimientos,
        "ACTUALIZACION",
        codigo,
        producto["nombre"],
        diferencia,
        f"Cantidad anterior: {cantidad_anterior}; "
        f"cantidad nueva: {nueva_cantidad}"
    )

    if guardar_datos(inventario, movimientos):
        print("Cantidad actualizada y guardada correctamente.")
    else:
        print("No se pudo guardar el cambio en el archivo.")

    print("Nueva existencia:", inventario[codigo]["cantidad"])


def consultar_stock_minimo(inventario):
    print("\n--- PRODUCTOS CON STOCK MINIMO ---")
    encontrados = False

    for codigo, producto in sorted(inventario.items()):
        cantidad = producto.get("cantidad", 0)
        minimo = producto.get("stock_minimo", 0)

        if cantidad <= minimo:
            encontrados = True
            print(
                codigo, "-", producto.get("nombre", ""),
                "| Cantidad:", cantidad,
                "| Stock minimo:", minimo
            )

    if not encontrados:
        print("No hay productos con stock minimo.")


def consultar_historial(movimientos):
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")

    if not movimientos:
        print("No hay movimientos registrados.")
        return

    for movimiento in reversed(movimientos):
        print(
            movimiento.get("fecha", ""),
            "|", movimiento.get("tipo", ""),
            "|", movimiento.get("codigo", ""),
            "|", movimiento.get("producto", ""),
            "| Cantidad:", movimiento.get("cantidad", 0),
            "|", movimiento.get("detalle", "")
        )


def menu_principal():
    inventario, movimientos = cargar_datos()

    while True:
        print("\n===== CONTROL DE INVENTARIO DE FERRETERIA =====")
        print("1. Registrar producto")
        print("2. Consultar existencias")
        print("3. Registrar entrada")
        print("4. Registrar salida")
        print("5. Actualizar cantidad")
        print("6. Consultar stock minimo")
        print("7. Consultar historial de movimientos")
        print("8. Buscar producto")
        print("9. Guardar inventario")
        print("10. Salir")

        opcion = input("Seleccione una opcion (1-10): ").strip()

        if opcion == "1":
            registrar_producto(inventario, movimientos)

        elif opcion == "2":
            consultar_existencias(inventario)

        elif opcion == "3":
            registrar_entrada(inventario, movimientos)

        elif opcion == "4":
            registrar_salida(inventario, movimientos)

        elif opcion == "5":
            actualizar_cantidad(inventario, movimientos)

        elif opcion == "6":
            consultar_stock_minimo(inventario)

        elif opcion == "7":
            consultar_historial(movimientos)

        elif opcion == "8":
            buscar_producto(inventario)

        elif opcion == "9":
            if guardar_datos(inventario, movimientos):
                print("Inventario guardado correctamente.")

        elif opcion == "10":
            guardar_datos(inventario, movimientos)
            print("Inventario guardado. Hasta luego.")
            break

        else:
            print("Opcion invalida. Elija un numero del 1 al 10.")


if __name__ == "__main__":
    menu_principal()
