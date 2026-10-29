# FERREX GT - MODULO 4: REPORTES Y ESTADISTICAS
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
ARCHIVO_INVENTARIO = BASE / 'inventario_ferreteria.json'
ARCHIVO_VENTAS = BASE / 'ventas.json'


def leer_json(ruta, predeterminado):
    if not ruta.exists():
        return predeterminado
    try:
        with ruta.open('r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (OSError, json.JSONDecodeError) as error:
        print(f'No se pudo leer {ruta.name}: {error}')
        return None


def cargar_inventario():
    datos = leer_json(ARCHIVO_INVENTARIO, None)
    if datos is None:
        print('No existe un inventario legible. Ejecute primero el programa de inventarios.')
        return None
    inventario = datos.get('inventario') if isinstance(datos, dict) else None
    if not isinstance(inventario, dict):
        print('El archivo no contiene un diccionario "inventario" valido.')
        return None
    return inventario


def cargar_ventas():
    ventas = leer_json(ARCHIVO_VENTAS, [])
    if ventas is None:
        return None
    if not isinstance(ventas, list):
        print('El archivo ventas.json debe contener una lista de ventas.')
        return None
    return ventas


def dinero(valor):
    return f'Q{float(valor):,.2f}'


def reporte_productos():
    inventario = cargar_inventario()
    if inventario is None:
        return
    print('\n--- LISTADO GENERAL DE PRODUCTOS ---')
    if not inventario:
        print('No hay productos registrados.')
    for codigo, p in sorted(inventario.items()):
        estado = 'Activo' if p.get('activo', True) else 'Inactivo'
        print(f"{codigo} | {p.get('nombre', '')} | {p.get('categoria', '')} | "
              f"{p.get('cantidad', 0)} {p.get('unidad', 'unidad')} | "
              f"{dinero(p.get('precio', 0))} | {estado}")


def reporte_stock_minimo():
    inventario = cargar_inventario()
    if inventario is None:
        return
    print('\n--- PRODUCTOS EN STOCK MINIMO O INFERIOR ---')
    bajos = [(codigo, p) for codigo, p in sorted(inventario.items())
             if p.get('cantidad', 0) <= p.get('stock_minimo', 0)]
    if not bajos:
        print('No hay productos con stock bajo.')
    for codigo, p in bajos:
        print(f"{codigo} | {p.get('nombre', '')} | Existencia: {p.get('cantidad', 0)} "
              f"| Minimo: {p.get('stock_minimo', 0)}")


def reporte_historial_ventas():
    ventas = cargar_ventas()
    if ventas is None:
        return
    print('\n--- HISTORIAL DE VENTAS ---')
    if not ventas:
        print('No hay ventas registradas. Las salidas de inventario no son ventas.')
    for venta in ventas:
        print(f"\nVenta: {venta.get('numero', 'Sin numero')} | "
              f"Fecha: {venta.get('fecha', 'Sin fecha')}")
        for d in venta.get('detalles', []):
            print(f"  {d.get('codigo', '')} - {d.get('nombre', '')}: "
                  f"{d.get('cantidad', 0)} x {dinero(d.get('precio', 0))} "
                  f"= {dinero(d.get('subtotal', 0))}")
        print(f"Subtotal: {dinero(venta.get('subtotal', 0))} | "
              f"IVA: {dinero(venta.get('iva', 0))} | "
              f"Total: {dinero(venta.get('total', 0))}")


def reporte_ingresos():
    ventas = cargar_ventas()
    if ventas is None:
        return
    print('\n--- INGRESOS POR VENTAS ---')
    print('Cantidad de ventas:', len(ventas))
    print('Ingresos totales (incluido IVA):', dinero(sum(v.get('total', 0) for v in ventas)))


def reporte_mas_vendido():
    ventas = cargar_ventas()
    if ventas is None:
        return
    print('\n--- PRODUCTO MAS VENDIDO ---')
    cantidades = defaultdict(int)
    nombres = {}
    for venta in ventas:
        for d in venta.get('detalles', []):
            codigo = d.get('codigo')
            if codigo:
                cantidades[codigo] += d.get('cantidad', 0)
                nombres[codigo] = d.get('nombre', codigo)
    if not cantidades:
        print('No hay unidades vendidas registradas.')
        return
    maximo = max(cantidades.values())
    for codigo in sorted(c for c, n in cantidades.items() if n == maximo):
        print(f'{codigo} | {nombres[codigo]} | {maximo} unidades')


def reporte_valor_inventario():
    inventario = cargar_inventario()
    if inventario is None:
        return
    print('\n--- VALOR TOTAL DEL INVENTARIO ---')
    valor = sum(p.get('cantidad', 0) * p.get('precio', 0)
                for p in inventario.values())
    print('Valor a precios de venta:', dinero(valor))


def reporte_promedio_periodo():
    ventas = cargar_ventas()
    if ventas is None:
        return
    print('\n--- PROMEDIO POR VENTA EN CADA MES ---')
    periodos = defaultdict(list)
    for v in ventas:
        try:
            fecha = datetime.fromisoformat(v['fecha'])
            periodos[fecha.strftime('%Y-%m')].append(v['total'])
        except (KeyError, TypeError, ValueError):
            print('Advertencia: se omitio una venta con fecha o total invalido.')
    if not periodos:
        print('No hay ventas con fechas validas.')
    for periodo, totales in sorted(periodos.items()):
        print(f'{periodo} | Ventas: {len(totales)} | '
              f'Promedio por venta: {dinero(sum(totales) / len(totales))}')


def menu_reportes():
    opciones = {
        '1': reporte_productos,
        '2': reporte_stock_minimo,
        '3': reporte_historial_ventas,
        '4': reporte_ingresos,
        '5': reporte_mas_vendido,
        '6': reporte_valor_inventario,
        '7': reporte_promedio_periodo,
    }
    while True:
        print('\n===== FERREX GT - REPORTES Y ESTADISTICAS =====')
        print('1. Listado general de productos')
        print('2. Productos con stock minimo')
        print('3. Historial de ventas')
        print('4. Total de ingresos por ventas')
        print('5. Producto mas vendido')
        print('6. Valor total del inventario')
        print('7. Promedio de ventas por mes')
        print('8. Regresar al menu principal')
        opcion = input('Seleccione una opcion: ').strip()
        if opcion == '8':
            break
        funcion = opciones.get(opcion)
        if funcion is None:
            print('Opcion invalida. Intente nuevamente.')
        else:
            try:
                funcion()
            except (TypeError, ValueError, KeyError) as error:
                print('Datos almacenados con formato incorrecto:', error)


if __name__ == '__main__':
    menu_reportes()
