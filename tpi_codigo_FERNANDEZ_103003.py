"""
UTN - TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN
ORGANIZACIÓN EMPRESARIAL - TPI
Nombre: Nancy Fernandez
Matricula: 103003
"""

import csv
import os

ARCHIVO_VALES = "vales_caja.csv"
ARCHIVO_FACTURAS = "facturas_cargadas.csv"

CAMPOS_VALES = [
    "codigo_vale",
    "nombre_empleado",
    "concepto",
    "monto_solicitado",
    "estado",
    "monto_rendido",
    "diferencia",
    "resultado"
]

CAMPOS_FACTURAS = [
    "proveedor",
    "numero_factura",
    "codigo_vale",
    "monto_factura"
]


def crear_archivos():
    if not os.path.exists(ARCHIVO_VALES):
        with open(ARCHIVO_VALES, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_VALES)
            escritor.writeheader()

    if not os.path.exists(ARCHIVO_FACTURAS):
        with open(ARCHIVO_FACTURAS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_FACTURAS)
            escritor.writeheader()


def leer_csv(nombre_archivo):
    try:
        with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        return []


def guardar_vales(vales):
    with open(ARCHIVO_VALES, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_VALES)
        escritor.writeheader()
        escritor.writerows(vales)


def pedir_texto(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Error: el campo no puede quedar vacío.")


def pedir_monto(mensaje):
    while True:
        try:
            monto = float(input(mensaje).replace(",", "."))
            if monto > 0:
                return monto
            print("Error: el importe debe ser mayor a cero.")
        except ValueError:
            print("Error: ingrese un importe numérico válido.")


def generar_codigo_vale():
    vales = leer_csv(ARCHIVO_VALES)
    numero = len(vales) + 1
    return f"VC-{numero:04d}"


def buscar_vale(codigo):
    vales = leer_csv(ARCHIVO_VALES)
    for vale in vales:
        if vale["codigo_vale"].upper() == codigo.upper():
            return vale
    return None


def factura_duplicada(proveedor, numero_factura):
    facturas = leer_csv(ARCHIVO_FACTURAS)

    for factura in facturas:
        mismo_proveedor = factura["proveedor"].strip().lower() == proveedor.strip().lower()
        misma_factura = factura["numero_factura"].strip().lower() == numero_factura.strip().lower()

        if mismo_proveedor and misma_factura:
            return True

    return False


def registrar_factura(proveedor, numero_factura, codigo_vale, monto_factura):
    with open(ARCHIVO_FACTURAS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_FACTURAS)
        escritor.writerow({
            "proveedor": proveedor,
            "numero_factura": numero_factura,
            "codigo_vale": codigo_vale,
            "monto_factura": monto_factura
        })


def mostrar_comprobante_solicitud(codigo, empleado, concepto, monto):
    print("\n======================================")
    print(" COMPROBANTE DE SOLICITUD DE VALE")
    print("======================================")
    print(f"Código de vale: {codigo}")
    print(f"Empleado: {empleado}")
    print(f"Concepto del gasto: {concepto}")
    print(f"Monto solicitado: ${monto:.2f}")
    print("Estado: ACTIVO")
    print("--------------------------------------")
    print("Firma empleado: ______________________")
    print("Firma supervisor: ____________________")
    print("======================================")
    print("El empleado debe imprimir este comprobante, hacerlo firmar por su supervisor y presentarlo en Caja.")


def mostrar_comprobante_rendicion(vale):
    print("\n======================================")
    print(" COMPROBANTE DE RENDICIÓN DE VALE")
    print("======================================")
    print(f"Código de vale: {vale['codigo_vale']}")
    print(f"Empleado: {vale['nombre_empleado']}")
    print(f"Concepto: {vale['concepto']}")
    print(f"Monto solicitado: ${float(vale['monto_solicitado']):.2f}")
    print(f"Monto rendido: ${float(vale['monto_rendido']):.2f}")
    print(f"Diferencia: ${abs(float(vale['diferencia'])):.2f}")
    print(f"Resultado: {vale['resultado']}")
    print("Estado: RENDIDO")
    print("--------------------------------------")
    print("Firma empleado: ______________________")
    print("Firma supervisor: ____________________")
    print("======================================")
    print("El empleado debe imprimir este comprobante, hacerlo firmar por su supervisor y presentarlo en Caja junto con las facturas.")


def solicitar_vale():
    print("\n--- SOLICITUD DE VALE DE CAJA ---")

    empleado = pedir_texto("Ingrese nombre completo del empleado: ")
    concepto = pedir_texto("Ingrese concepto del gasto: ")
    monto = pedir_monto("Ingrese monto solicitado: $")

    codigo = generar_codigo_vale()

    nuevo_vale = {
        "codigo_vale": codigo,
        "nombre_empleado": empleado,
        "concepto": concepto,
        "monto_solicitado": monto,
        "estado": "ACTIVO",
        "monto_rendido": "",
        "diferencia": "",
        "resultado": ""
    }

    with open(ARCHIVO_VALES, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_VALES)
        escritor.writerow(nuevo_vale)

    print("\nSolicitud registrada correctamente.")
    mostrar_comprobante_solicitud(codigo, empleado, concepto, monto)


def rendir_vale():
    print("\n--- RENDICIÓN DE VALE DE CAJA ---")

    codigo = pedir_texto("Ingrese código del vale: ").upper()
    vales = leer_csv(ARCHIVO_VALES)

    vale_encontrado = None

    for vale in vales:
        if vale["codigo_vale"].upper() == codigo:
            vale_encontrado = vale
            break

    if vale_encontrado is None:
        print("Error: el vale ingresado no existe. Se vuelve al menú principal.")
        return

    if vale_encontrado["estado"].upper() == "RENDIDO":
        print("Error: este vale ya fue rendido. No puede utilizarse nuevamente.")
        return

    print("\nVale encontrado:")
    print(f"Empleado: {vale_encontrado['nombre_empleado']}")
    print(f"Concepto: {vale_encontrado['concepto']}")
    print(f"Monto solicitado: ${float(vale_encontrado['monto_solicitado']):.2f}")

    total_rendido = 0
    facturas_temporales = []

    while True:
        print("\nCarga de factura respaldatoria")

        proveedor = pedir_texto("Ingrese proveedor: ")
        numero_factura = pedir_texto("Ingrese número de factura: ")

        if factura_duplicada(proveedor, numero_factura):
            print("Error: la factura ya fue cargada anteriormente para ese proveedor.")
            print("No se permite duplicar el gasto. Se cancela la rendición.")
            return

        monto_factura = pedir_monto("Ingrese monto de la factura: $")

        facturas_temporales.append({
            "proveedor": proveedor,
            "numero_factura": numero_factura,
            "codigo_vale": codigo,
            "monto_factura": monto_factura
        })

        total_rendido += monto_factura

        otra = input("¿Desea cargar otra factura? (S/N): ").strip().upper()
        if otra != "S":
            break

    monto_solicitado = float(vale_encontrado["monto_solicitado"])
    diferencia = monto_solicitado - total_rendido

    if diferencia > 0:
        resultado = f"El empleado debe devolver ${diferencia:.2f} a Caja."
    elif diferencia < 0:
        resultado = f"Caja debe reintegrar ${abs(diferencia):.2f} al empleado."
    else:
        resultado = "No existe diferencia de dinero."

    for factura in facturas_temporales:
        registrar_factura(
            factura["proveedor"],
            factura["numero_factura"],
            factura["codigo_vale"],
            factura["monto_factura"]
        )

    vale_encontrado["estado"] = "RENDIDO"
    vale_encontrado["monto_rendido"] = total_rendido
    vale_encontrado["diferencia"] = diferencia
    vale_encontrado["resultado"] = resultado

    guardar_vales(vales)

    print("\nRendición registrada correctamente.")
    mostrar_comprobante_rendicion(vale_encontrado)


def ver_solicitudes_activas():
    print("\n--- SOLICITUDES ACTIVAS PENDIENTES DE RENDICIÓN ---")

    vales = leer_csv(ARCHIVO_VALES)
    hay_activas = False

    for vale in vales:
        if vale["estado"].upper() == "ACTIVO":
            hay_activas = True
            print("--------------------------------------")
            print(f"Código de vale: {vale['codigo_vale']}")
            print(f"Empleado: {vale['nombre_empleado']}")
            print(f"Concepto: {vale['concepto']}")
            print(f"Monto solicitado: ${float(vale['monto_solicitado']):.2f}")

    if not hay_activas:
        print("No existen solicitudes activas pendientes de rendición.")


def menu():
    crear_archivos()

    while True:
        print("\n======================================")
        print(" Bot Auditoria - Vales de Caja")
        print("======================================")
        print("1) Solicitud de vale de caja")
        print("2) Rendición de vale de caja")
        print("3) Ver solicitudes activas")
        print("4) Cerrar")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            solicitar_vale()
        elif opcion == "2":
            rendir_vale()
        elif opcion == "3":
            ver_solicitudes_activas()
        elif opcion == "4":
            print("Gracias por utilizar Bot Auditoría.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


menu()