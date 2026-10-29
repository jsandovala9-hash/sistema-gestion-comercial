
# ==========================================
# FERREX GT
# ESTRUCTURAS Y VALIDACIONES
# ==========================================

from decimal import Decimal, InvalidOperation


IVA = Decimal("0.12")


# Normalizar codigo del producto
def normalizar_codigo(codigo):
    codigo = str(codigo).strip().upper()

    if codigo.isdigit() and len(codigo) == 3:
        codigo = "FER" + codigo

    return codigo


# Validar cantidades
def validar_cantidad(cantidad):
    try:
        numero = int(cantidad)

        if numero <= 0:
            return False

        return True

    except (ValueError, TypeError):
        return False


# Validar precios
def validar_precio(precio):
    try:
        numero = Decimal(str(precio))

        return numero.is_finite() and numero >= 0

    except (InvalidOperation, TypeError, ValueError):
        return False


# Calcular subtotal
def calcular_subtotal(precio, cantidad):
    return Decimal(str(precio)) * cantidad


# Calcular IVA del 12 %
def calcular_iva(subtotal):
    impuesto = Decimal(str(subtotal)) * IVA
    return impuesto.quantize(Decimal("0.01"))


# Calcular total de venta
def calcular_total(subtotal):
    subtotal = Decimal(str(subtotal))
    iva = calcular_iva(subtotal)

    return subtotal + iva


# Verificar existencia suficiente
def verificar_stock(disponible, solicitado):
    return (
        validar_cantidad(solicitado)
        and disponible >= int(solicitado)
    )
