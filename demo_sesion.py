
import sqlite3
from contextlib import closing
import tempfile
import atexit
from pathlib import Path

from generar_demo import movimientos_demo




def eliminar_base_demo_temporal(ruta):
    """Intenta eliminar una base temporal y sus archivos auxiliares."""
    import gc
    import time

    gc.collect()

    for intento in range(5):
        try:
            Path(ruta).unlink(missing_ok=True)

            for extension in ("-wal", "-shm", "-journal"):
                Path(str(ruta) + extension).unlink(missing_ok=True)

            return True

        except PermissionError:
            time.sleep(0.2)

    return False



def crear_base_demo_temporal():
    """Crea una base de datos ficticia independiente."""

    archivo = tempfile.NamedTemporaryFile(
        suffix=".db",
        prefix="expense_tracker_demo_",
        delete=False
    )

    ruta = Path(archivo.name)
    archivo.close()

    # Programar limpieza al finalizar Python
    atexit.register(eliminar_base_demo_temporal, str(ruta))

    with closing(sqlite3.connect(ruta)) as conexion:
        conexion.execute("""
            CREATE TABLE movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
        """)

        conexion.executemany("""
            INSERT INTO movimientos
            (tipo, cantidad, categoria, fecha)
            VALUES (?, ?, ?, ?)
        """, movimientos_demo)

        conexion.commit()

    return str(ruta)
