
# 💰 Expense Tracker

## 🚀 Aplicación en línea

Prueba el dashboard interactivo aquí:

[🔗 Abrir Expense Tracker](https://expense-tracker-javier.streamlit.app/)
Aplicación web de gestión financiera personal desarrollada con Python, SQLite y Streamlit.

Permite registrar ingresos y gastos, analizar movimientos financieros mediante indicadores y gráficos interactivos, y exportar reportes en Excel y CSV.

## 📊 Funcionalidades

- Registro de ingresos y gastos.
- Edición y eliminación de movimientos.
- Almacenamiento de información mediante SQLite.
- Indicadores de ingresos, gastos y saldo.
- Filtros dinámicos por categoría y período.
- Visualización de gastos por categoría.
- Historial de movimientos.
- Exportación de reportes a Excel y CSV.
- Formato monetario en pesos chilenos (CLP).
- Modo demostración con datos ficticios.
- Bases de datos temporales independientes por sesión.
- Reinicio de datos de demostración.

## 🛠️ Tecnologías utilizadas

- **Python:** lógica de la aplicación.
- **Streamlit:** interfaz web interactiva.
- **SQLite:** almacenamiento de datos.
- **Pandas:** procesamiento y análisis de información.
- **OpenPyXL:** generación de reportes Excel.
- **Matplotlib:** visualización de datos en herramientas del proyecto.
- **Git y GitHub:** control de versiones.

## 📁 Estructura del proyecto

```text
expense-tracker/
├── app.py
├── repositorio.py
├── config.py
├── demo_sesion.py
├── generar_demo.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Ejecución local

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd expense-tracker
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la demostración pública

En PowerShell:

```powershell
$env:EXPENSE_TRACKER_PUBLIC="true"
python -m streamlit run app.py
```

La aplicación se abrirá en el navegador.

## 🧪 Modo demostración

La aplicación incluye movimientos financieros ficticios para explorar sus funcionalidades.

Cada sesión utiliza una base de datos temporal independiente, lo que permite registrar, editar y eliminar movimientos de prueba sin afectar los datos de otros visitantes.

El botón **Reiniciar demostración** restaura los movimientos ficticios originales.

## 🔒 Privacidad

Los archivos de bases de datos locales, respaldos y configuraciones privadas están excluidos del repositorio mediante `.gitignore`.

La versión pública está diseñada para utilizar exclusivamente información ficticia.

## 🎯 Objetivo del proyecto

Proyecto de portafolio orientado a demostrar habilidades prácticas en:

- Desarrollo de aplicaciones con Python.
- Consultas y operaciones CRUD con SQL.
- Procesamiento de datos financieros.
- Construcción de indicadores de gestión.
- Visualización de información.
- Automatización de reportes.

## 📌 Estado

Versión 1.0 — Preparación para publicación.
