
import sqlite3
from pathlib import Path

# Base de datos independiente
RUTA_DEMO = Path(__file__).parent / "finanzas_demo.db"

# Movimientos completamente ficticios
movimientos_demo = [
    ("Ingreso", 950000, "Sueldo", "2026-08-05"),
    ("Ingreso", 150000, "Ventas", "2026-08-15"),
    ("Gasto", 300000, "Vivienda", "2026-08-06"),
    ("Gasto", 120000, "Alimentación", "2026-08-10"),
    ("Gasto", 45000, "Transporte", "2026-08-18"),
    ("Ingreso", 950000, "Sueldo", "2026-09-05"),
    ("Gasto", 300000, "Vivienda", "2026-09-06"),
    ("Gasto", 135000, "Alimentación", "2026-09-12"),
    ("Gasto", 55000, "Servicios", "2026-09-20"),
    ("Ingreso", 950000, "Sueldo", "2026-10-05"),
    ("Ingreso", 100000, "Bonos", "2026-10-10"),
    ("Gasto", 300000, "Vivienda", "2026-10-06"),
    ("Gasto", 140000, "Alimentación", "2026-10-12"),
    ("Gasto", 50000, "Transporte", "2026-10-15"),
    ("Gasto", 35000, "Entretenimiento", "2026-10-18"),
]
def generar_base_demo():
# Crear una base de datos separada
    with sqlite3.connect(RUTA_DEMO) as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
        """)

        cantidad_actual = conexion.execute(
            "SELECT COUNT(*) FROM movimientos"
        ).fetchone()[0]

        if cantidad_actual == 0:
            conexion.executemany("""
                INSERT INTO movimientos
                (tipo, cantidad, categoria, fecha)
                VALUES (?, ?, ?, ?)
            """, movimientos_demo)

            print("Datos ficticios creados correctamente.")
        else:
            print("La base de demostración ya contiene datos.")

    print(f"Base de demostración: {RUTA_DEMO}")

if __name__ == "__main__":
    generar_base_demo()