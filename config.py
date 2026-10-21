
import os

# Por seguridad, el modo público está activado por defecto.
# Solo se permite el modo personal si lo activamos
# explícitamente en nuestro computador.

MODO_PUBLICO = os.getenv(
    "EXPENSE_TRACKER_PUBLIC",
    "true"
).lower() == "true"
