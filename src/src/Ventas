# FERREX GT - MODULO 2: REGISTRO DE VENTAS
import json
import math
import os
import tempfile
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent
ARCHIVO_INVENTARIO = BASE / 'inventario_ferreteria.json'
ARCHIVO_VENTAS = BASE / 'ventas.json'
IVA = Decimal('0.12')


def guardar_json(ruta, datos):
    """Escribe mediante archivo temporal para evitar archivos JSON incompletos."""
    temporal = None
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=ruta.parent,
                                         prefix='.tmp_', suffix='.json', delete=False) as archivo:
            temporal = Path(archivo.name)
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        os.replace(temporal, ruta)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()


def leer_json(ruta):
    with ruta.open('r', encoding='utf-8') as archivo:
        return json.load(archivo)


def normalizar_codigo(codigo):
    codigo = codigo.strip().upper()
    return 'FER' + codigo if codigo.isdigit() and len(codigo) == 3 else codigo


def leer_cantidad():
    while True:
        texto = input('Cantidad a vender: ').strip()
        try:
            cantidad = int(texto)
            if cantidad > 0:
                return cantidad
        except ValueError:
            pass
        print('Error: ingrese una cantidad entera positiva.')


def dinero(valor):
    return Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def registrar_venta():
    print('\n===== FERREX GT - REGISTRAR VENTA =====')
    if not ARCHIVO_INVENTARIO.exists():
        print('No existe el inventario. Ejecute primero su programa de inventarios.')
        return

    try:
        datos = leer_json(ARCHIVO_INVENTARIO)
        ventas = leer_json(ARCHIVO_VENTAS) if ARCHIVO_VENTAS.exists() else []
        if not isinstance(datos, dict) or not isinstance(datos.get('inventario'), dict):
            raise ValueError('Formato del inventario incorrecto')
        if not isinstance(datos.get('movimientos'), list) or not isinstance(ventas, list):
            raise ValueError('Formato de movimientos o ventas incorrecto')
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print('No se pudieron cargar los datos:', error)
        return

    inventario = datos['inventario']
    carrito = {}
    while True:
        codigo = normalizar_codigo(input('\nCodigo (o FIN para terminar): '))
        if codigo == 'FIN':
            break
        if codigo not in inventario:
            print('Producto no encontrado.')
            continue
        producto = inventario[codigo]
        if not producto.get('activo', True):
            print('Producto desactivado: no disponible para la venta.')
            continue
        try:
            disponible = int(producto['cantidad'])
            precio = dinero(producto['precio'])
            if disponible < 0 or precio < 0 or not precio.is_finite():
                raise ValueError('Cantidad o precio incorrectos')
        except (KeyError, ValueError, TypeError, InvalidOperation) as error:
            print('Datos del producto incorrectos:', error)
            continue
        print(f"{producto['nombre']} | Precio: Q{precio:.2f} | Disponible: {disponible}")
        cantidad = leer_cantidad()
        acumulado = carrito.get(codigo, 0) + cantidad
        if acumulado > disponible:
            print(f'Inventario insuficiente. Disponible: {disponible}; solicitado: {acumulado}.')
            continue
        carrito[codigo] = acumulado
        print('Producto agregado a la venta.')

    if not carrito:
        print('Venta cancelada: no se seleccionaron productos.')
        return

    detalles = []
    subtotal_general = Decimal('0.00')
    for codigo, cantidad in carrito.items():
        producto = inventario[codigo]
        precio = dinero(producto['precio'])
        subtotal = dinero(precio * cantidad)
        subtotal_general += subtotal
        detalles.append({
            'codigo': codigo, 'nombre': producto['nombre'], 'cantidad': cantidad,
            'precio': float(precio), 'subtotal': float(subtotal)
        })

    subtotal_general = dinero(subtotal_general)
    iva = dinero(subtotal_general * IVA)
    total = dinero(subtotal_general + iva)
    print('\n--- RESUMEN DE VENTA ---')
    for detalle in detalles:
        print(f"{detalle['codigo']} - {detalle['nombre']}: {detalle['cantidad']} x "
              f"Q{detalle['precio']:.2f} = Q{detalle['subtotal']:.2f}")
    print(f'Subtotal: Q{subtotal_general:.2f}')
    print(f'IVA 12%: Q{iva:.2f}')
    print(f'TOTAL: Q{total:.2f}')

    if input('Confirmar venta (S/N): ').strip().upper() != 'S':
        print('Venta cancelada. No se modifico el inventario.')
        return

    # Identificador secuencial, compatible con el historial de reportes.
    try:
        numero = max((int(v['numero']) for v in ventas), default=0) + 1
    except (KeyError, TypeError, ValueError):
        print('Historial de ventas incorrecto. No se registro la venta.')
        return

    fecha = datetime.now().isoformat(timespec='seconds')
    venta = {
        'numero': numero, 'fecha': fecha, 'detalles': detalles,
        'subtotal': float(subtotal_general), 'iva': float(iva), 'total': float(total)
    }

    # Preparar nuevos datos sin modificar los originales en memoria.
    import copy
    nuevos_datos = copy.deepcopy(datos)
    for detalle in detalles:
        codigo = detalle['codigo']
        cantidad = detalle['cantidad']
        nuevos_datos['inventario'][codigo]['cantidad'] -= cantidad
        nuevos_datos['movimientos'].append({
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'VENTA', 'codigo': codigo, 'producto': detalle['nombre'],
            'cantidad': cantidad, 'detalle': f'Venta No. {numero}'
        })

    # Primero guardar la venta, despues el inventario. Si falla el segundo,
    # intentar restaurar el historial anterior para evitar una venta fantasma.
    try:
        guardar_json(ARCHIVO_VENTAS, ventas + [venta])
        try:
            guardar_json(ARCHIVO_INVENTARIO, nuevos_datos)
        except OSError:
            guardar_json(ARCHIVO_VENTAS, ventas)
            raise
    except OSError as error:
        print('Error al guardar la venta o inventario:', error)
        print('Revise los archivos antes de intentar nuevamente.')
        return

    print(f'Venta No. {numero} guardada correctamente.')
    print('Inventario actualizado y movimientos registrados.')


def menu_ventas():
    while True:
        print('\n===== FERREX GT - VENTAS =====')
        print('1. Registrar venta')
        print('2. Regresar al menu principal')
        opcion = input('Seleccione una opcion: ').strip()
        if opcion == '1':
            registrar_venta()
        elif opcion == '2':
            break
        else:
            print('Opcion invalida. Intente nuevamente.')


if __name__ == '__main__':
    menu_ventas()
