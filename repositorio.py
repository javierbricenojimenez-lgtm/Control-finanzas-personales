
import sqlite3

from pathlib import Path
import tempfile

from config import MODO_PUBLICO


def validar_base_datos(base_datos):
    if MODO_PUBLICO:
        ruta = Path(base_datos).resolve()
        carpeta_temporal = Path(tempfile.gettempdir()).resolve()

        if (
            ruta.parent != carpeta_temporal
            or not ruta.name.startswith("expense_tracker_demo_")
            or ruta.suffix != ".db"
        ):
            raise PermissionError(
                "Acceso bloqueado: base de datos no permitida "
                "en modo público."
            )

    return base_datos

# Base de datos personal por defecto
BASE_DATOS = "finanzas.db"


def obtener_movimientos(base_datos=BASE_DATOS):
    conexion = sqlite3.connect(validar_base_datos(base_datos))
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, tipo, cantidad, categoria, fecha
        FROM movimientos
        ORDER BY id
    """)

    filas = cursor.fetchall()
    movimientos = [dict(fila) for fila in filas]

    conexion.close()

    return movimientos


def agregar_movimiento(tipo, cantidad, categoria, fecha, base_datos=BASE_DATOS):
    conexion = sqlite3.connect(validar_base_datos(base_datos))
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO movimientos
        (tipo, cantidad, categoria, fecha)
        VALUES (?, ?, ?, ?)
    """, (tipo, cantidad, categoria, fecha))

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return nuevo_id


def actualizar_movimiento(
    id_movimiento,
    cantidad,
    categoria,
    base_datos=BASE_DATOS
):
    conexion = sqlite3.connect(validar_base_datos(base_datos))
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE movimientos
        SET cantidad = ?, categoria = ?
        WHERE id = ?
    """, (cantidad, categoria, id_movimiento))

    conexion.commit()
    filas_modificadas = cursor.rowcount
    conexion.close()

    return filas_modificadas


def eliminar_movimiento_sql(id_movimiento, base_datos=BASE_DATOS):
    conexion = sqlite3.connect(validar_base_datos(base_datos))
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM movimientos
        WHERE id = ?
    """, (id_movimiento,))

    conexion.commit()
    filas_eliminadas = cursor.rowcount
    conexion.close()

    return filas_eliminadas
