# FERREX GT - MODULO 1: GESTION DE PRODUCTOS
# Comparte inventario_ferreteria.json con ventas.py e inventario.py.
import math
from inventario import cargar_datos, guardar_datos, registrar_movimiento, normalizar_codigo


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print('Error: este campo no puede estar vacio.')


def leer_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje).strip().replace(',', '.'))
            if math.isfinite(valor) and valor >= 0:
                return round(valor, 2)
        except ValueError:
            pass
        print('Error: ingrese un precio valido no negativo.')


def leer_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor >= 0:
                return valor
        except ValueError:
            pass
        print('Error: ingrese un numero entero no negativo.')


def mostrar_producto(codigo, producto):
    print('-' * 40)
    print('Codigo:', codigo)
    print('Nombre:', producto.get('nombre', ''))
    print('Categoria:', producto.get('categoria', ''))
    print('Unidad:', producto.get('unidad', 'unidad'))
    print(f"Precio: Q{producto.get('precio', 0):.2f}")
    print('Cantidad:', producto.get('cantidad', 0))
    print('Stock minimo:', producto.get('stock_minimo', 0))
    print('Estado:', 'Activo' if producto.get('activo', True) else 'Inactivo')


def registrar_producto():
    inventario, movimientos = cargar_datos()
    print('\n--- REGISTRAR PRODUCTO ---')
    codigo = normalizar_codigo(leer_texto('Codigo del producto: '))
    if codigo in inventario:
        print('Error: el codigo ya existe.')
        return
    nombre = leer_texto('Nombre: ')
    categoria = leer_texto('Categoria: ')
    unidad = leer_texto('Unidad (unidad, bolsa, caja, etc.): ')
    precio = leer_decimal('Precio Q: ')
    cantidad = leer_entero('Cantidad inicial: ')
    stock_minimo = leer_entero('Stock minimo: ')
    inventario[codigo] = dict(nombre=nombre, categoria=categoria, unidad=unidad,
                             precio=precio, cantidad=cantidad, stock_minimo=stock_minimo,
                             activo=True)
    registrar_movimiento(movimientos, 'REGISTRO', codigo, nombre, cantidad, 'Registro desde productos')
    if guardar_datos(inventario, movimientos):
        print('Producto registrado correctamente.')
    else:
        print('No se pudo guardar el producto.')


def consultar_producto():
    inventario, _ = cargar_datos()
    codigo = normalizar_codigo(leer_texto('Codigo: '))
    if codigo in inventario:
        mostrar_producto(codigo, inventario[codigo])
    else:
        print('Producto no encontrado.')


def listar_productos():
    inventario, _ = cargar_datos()
    if not inventario:
        print('No hay productos registrados.')
    for codigo, producto in sorted(inventario.items()):
        mostrar_producto(codigo, producto)


def modificar_producto():
    inventario, movimientos = cargar_datos()
    codigo = normalizar_codigo(leer_texto('Codigo: '))
    if codigo not in inventario:
        print('Producto no encontrado.')
        return
    producto = inventario[codigo]
    mostrar_producto(codigo, producto)
    print('Ingrese los nuevos datos:')
    nombre = leer_texto('Nuevo nombre: ')
    categoria = leer_texto('Nueva categoria: ')
    unidad = leer_texto('Nueva unidad: ')
    precio = leer_decimal('Nuevo precio Q: ')
    cantidad = leer_entero('Nueva cantidad: ')
    stock_minimo = leer_entero('Nuevo stock minimo: ')
    diferencia = cantidad - producto.get('cantidad', 0)
    producto.update(nombre=nombre, categoria=categoria, unidad=unidad, precio=precio,
                    cantidad=cantidad, stock_minimo=stock_minimo)
    registrar_movimiento(movimientos, 'MODIFICACION', codigo, nombre, diferencia,
                         'Modificacion de datos y cantidad desde productos')
    if guardar_datos(inventario, movimientos):
        print('Producto modificado correctamente.')
    else:
        print('No se pudo guardar la modificacion.')


def desactivar_producto():
    inventario, movimientos = cargar_datos()
    codigo = normalizar_codigo(leer_texto('Codigo: '))
    if codigo not in inventario:
        print('Producto no encontrado.')
        return
    if not inventario[codigo].get('activo', True):
        print('El producto ya esta desactivado.')
        return
    if input('Desea desactivar el producto? (S/N): ').strip().upper() != 'S':
        print('Operacion cancelada.')
        return
    inventario[codigo]['activo'] = False
    registrar_movimiento(movimientos, 'DESACTIVACION', codigo,
                         inventario[codigo]['nombre'], 0, 'Producto desactivado')
    if guardar_datos(inventario, movimientos):
        print('Producto desactivado correctamente.')
    else:
        print('No se pudo guardar la desactivacion.')


def menu_productos():
    while True:
        print('\n===== FERREX GT - GESTION DE PRODUCTOS =====')
        print('1. Registrar producto')
        print('2. Consultar producto')
        print('3. Listar productos')
        print('4. Modificar producto')
        print('5. Desactivar producto')
        print('6. Regresar al menu principal')
        opcion = input('Seleccione una opcion: ').strip()
        if opcion == '1': registrar_producto()
        elif opcion == '2': consultar_producto()
        elif opcion == '3': listar_productos()
        elif opcion == '4': modificar_producto()
        elif opcion == '5': desactivar_producto()
        elif opcion == '6': break
        else: print('Opcion invalida.')


if __name__ == '__main__':
    menu_productos()
