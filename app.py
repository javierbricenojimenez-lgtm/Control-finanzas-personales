
import streamlit as st
import pandas as pd
import sqlite3
from config import MODO_PUBLICO
from demo_sesion import crear_base_demo_temporal, eliminar_base_demo_temporal
from pathlib import Path
from io import BytesIO
from repositorio import (
    obtener_movimientos,
    agregar_movimiento,
    actualizar_movimiento,
    eliminar_movimiento_sql
)


# Formato de pesos chilenos
def formato_clp(valor):
    monto = f"{abs(valor):,.0f}".replace(",", ".")

    if valor < 0:
        return f"-${monto}"

    return f"${monto}"


# Configuracion de la pagina
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker")
st.subheader("Dashboard financiero")
if "mensaje_edicion" in st.session_state:
    st.success(st.session_state.pop("mensaje_edicion"))
if "mensaje_eliminacion" in st.session_state:
    st.success(st.session_state.pop("mensaje_eliminacion"))
# 1. Obtener datos desde SQLite


# Elegir origen de datos
if MODO_PUBLICO:
    # Cada sesión obtiene una base temporal independiente
    if "base_demo_sesion" not in st.session_state:
        st.session_state["base_demo_sesion"] = crear_base_demo_temporal()

    base_datos_actual = st.session_state["base_demo_sesion"]
    modo_demo = True

    st.sidebar.success("🧪 Demostración pública")
    st.sidebar.caption("Los datos son ficticios.")

    if st.sidebar.button("🔄 Reiniciar demostración"):
        ruta_anterior = st.session_state["base_demo_sesion"]
        ruta_nueva = crear_base_demo_temporal()

        st.session_state["base_demo_sesion"] = ruta_nueva
        eliminar_base_demo_temporal(ruta_anterior)

        st.rerun()

else:
    modo_demo = st.sidebar.toggle(
        "🧪 Modo demostración",
        value=False
    )

    if modo_demo:
        base_datos_actual = "finanzas_demo.db"
        st.sidebar.info("Estás utilizando datos ficticios.")
    else:
        base_datos_actual = "finanzas.db"
        st.sidebar.info("Estás utilizando tu base personal.")

movimientos = obtener_movimientos(base_datos_actual)





if not movimientos:
    st.info("Todavía no hay movimientos registrados.")
    st.stop()

df = pd.DataFrame(movimientos)


# 2. Preparar fechas y periodos
df["periodo"] = df["fecha"].apply(
    lambda fecha: str(fecha)[:7]
    if pd.notna(fecha) and fecha != "Sin fecha"
    else "Sin fecha"
)


# 3. Filtros del dashboard
st.markdown("### 🔎 Filtros")

categorias = sorted(df["categoria"].unique().tolist())
periodos = sorted(df["periodo"].unique().tolist())

col_filtro1, col_filtro2 = st.columns(2)

with col_filtro1:
    categoria_seleccionada = st.selectbox(
        "Filtrar por categoría",
        ["Todas"] + categorias
    )

with col_filtro2:
    periodo_seleccionado = st.selectbox(
        "Filtrar por mes",
        ["Todos"] + periodos
    )


# 4. Aplicar filtros
movimientos_filtrados = df.copy()

if categoria_seleccionada != "Todas":
    movimientos_filtrados = movimientos_filtrados[
        movimientos_filtrados["categoria"]
        == categoria_seleccionada
    ]

if periodo_seleccionado != "Todos":
    movimientos_filtrados = movimientos_filtrados[
        movimientos_filtrados["periodo"]
        == periodo_seleccionado
    ]


# 5. Calcular indicadores filtrados
ingresos = movimientos_filtrados.loc[
    movimientos_filtrados["tipo"] == "Ingreso",
    "cantidad"
].sum()

gastos = movimientos_filtrados.loc[
    movimientos_filtrados["tipo"] == "Gasto",
    "cantidad"
].sum()

saldo = ingresos - gastos


# 6. Mostrar indicadores
st.divider()
st.subheader("📊 Indicadores financieros")

col1, col2, col3 = st.columns(3)

col1.metric("Ingresos", formato_clp(ingresos))
col2.metric("Gastos", formato_clp(gastos))
col3.metric("Saldo", formato_clp(saldo))


# 7. Grafico dinamico de gastos
st.divider()
st.subheader("📊 Gastos por categoría")

gastos_grafico = movimientos_filtrados[
    movimientos_filtrados["tipo"] == "Gasto"
]

resumen_grafico = (
    gastos_grafico.groupby("categoria")["cantidad"]
    .sum()
    .sort_values(ascending=False)
)

if not resumen_grafico.empty:
    st.bar_chart(resumen_grafico)
else:
    st.info("No hay gastos para los filtros seleccionados.")


# Formulario para registrar movimientos

st.divider()
st.subheader("➕ Registrar movimiento")


# Mostrar confirmacion despues de guardar
if "registro_exitoso" in st.session_state:
    st.success(st.session_state.pop("registro_exitoso"))

# Elegir tipo antes de abrir el formulario
tipo_nuevo = st.radio(
    "Tipo de movimiento",
    ["Gasto", "Ingreso"],
    horizontal=True
)

with st.form("formulario_movimiento", clear_on_submit=True):
    

    cantidad_nueva = st.number_input(
        "Monto ($ CLP)",
        min_value=1,
        step=1000
    )

    
    
    # Categorias de gastos
    categorias_gastos = [
        "Alimentación",
        "Transporte",
        "Salud",
        "Vivienda",
        "Servicios",
        "Entretenimiento",
        "Educación",
        "Otros"
    ]

    # Categorias de ingresos
    categorias_ingresos = [
        "Sueldo",
        "Ventas",
        "Bonos",
        "Inversiones",
        "Trabajos independientes",
        "Otros ingresos"
    ]

    # Seleccionar categorias segun el tipo
    if tipo_nuevo == "Gasto":
        categorias_disponibles = categorias_gastos
    else:
        categorias_disponibles = categorias_ingresos

    categoria_nueva = st.selectbox(
        "Categoría",
        categorias_disponibles
    )



    
    fecha_nueva = st.date_input(
        "Fecha del movimiento"
    )

    guardar = st.form_submit_button("Guardar movimiento")



# Guardar el movimiento en SQLite
if guardar:
    if not categoria_nueva.strip():
        st.warning("Debes ingresar una categoría.")
    else:
        
        nuevo_id = agregar_movimiento(
             tipo_nuevo,
             cantidad_nueva,
             categoria_nueva.strip(),
             fecha_nueva.isoformat(),
             base_datos=base_datos_actual
)


        st.session_state["registro_exitoso"] = (
            f"✅ ¡Registro completado correctamente! "
            f"Movimiento #{nuevo_id} guardado."
        )

        st.rerun()



# 8. Historial de movimientos

st.divider()
st.subheader("📋 Historial de movimientos")

st.dataframe(
    movimientos_filtrados,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Movimientos encontrados: {len(movimientos_filtrados)}"
)

# Exportar reportes
st.divider()
st.subheader("📥 Descargar reportes")

# Preparar datos para exportar
reporte = movimientos_filtrados.copy()

# Archivo CSV
csv = reporte.to_csv(
    index=False,
    sep=";"
).encode("utf-8-sig")

# Archivo Excel
archivo_excel = BytesIO()


with pd.ExcelWriter(
    archivo_excel,
    engine="openpyxl"
) as writer:

    reporte.to_excel(
        writer,
        index=False,
        sheet_name="Movimientos"
    )

    hoja = writer.sheets["Movimientos"]

    # Ajustar ancho de columnas
    hoja.column_dimensions["A"].width = 10
    hoja.column_dimensions["B"].width = 15
    hoja.column_dimensions["C"].width = 18
    hoja.column_dimensions["D"].width = 25
    hoja.column_dimensions["E"].width = 18
    hoja.column_dimensions["F"].width = 15

    # Destacar encabezados
    from openpyxl.styles import Font, PatternFill

    for celda in hoja[1]:
        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )
        celda.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

    # Formato de montos en pesos chilenos
    for fila in range(2, hoja.max_row + 1):
        hoja[f"C{fila}"].number_format = '"$"#,##0'

    # Mantener encabezados visibles
    hoja.freeze_panes = "A2"

    # Activar filtros en Excel
    hoja.auto_filter.ref = hoja.dimensions


# Botones de descarga
col_csv, col_excel = st.columns(2)

with col_csv:
    st.download_button(
        label="📄 Descargar CSV",
        data=csv,
        file_name="reporte_movimientos.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_excel:
    st.download_button(
        label="📊 Descargar Excel",
        data=archivo_excel.getvalue(),
        file_name="reporte_movimientos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
 
# 9. Administrar movimientos
st.divider()
st.subheader("⚙️ Administrar movimientos")

if not movimientos_filtrados.empty:

    ids_disponibles = movimientos_filtrados["id"].tolist()

    id_seleccionado = st.selectbox(
        "Selecciona el ID del movimiento",
        ids_disponibles
    )

    movimiento = movimientos_filtrados[
        movimientos_filtrados["id"] == id_seleccionado
    ].iloc[0]

    st.write("Tipo:", movimiento["tipo"])
    st.write("Monto actual:", formato_clp(movimiento["cantidad"]))
    st.write("Categoría actual:", movimiento["categoria"])
    st.write("Fecha:", movimiento["fecha"])

    with st.form("formulario_edicion"):

        monto_editado = st.number_input(
            "Nuevo monto ($ CLP)",
            min_value=1,
            value=int(movimiento["cantidad"]),
            step=1000
        )

        categoria_editada = st.text_input(
            "Nueva categoría",
            value=movimiento["categoria"]
        )

        guardar_cambios = st.form_submit_button(
            "💾 Guardar cambios"
        )

    if guardar_cambios:

        if not categoria_editada.strip():
            st.warning("Debes ingresar una categoría.")
        else:
            
            filas = actualizar_movimiento(
                 int(id_seleccionado),
                 monto_editado,
                 categoria_editada.strip(),
                 base_datos=base_datos_actual
)


            if filas > 0:
                st.session_state["mensaje_edicion"] = (
                    "✅ Movimiento actualizado correctamente."
                )
                st.rerun()
            else:
                st.error("No se pudo actualizar el movimiento.")

else:
    st.info("No hay movimientos disponibles para editar.")

# 10. Eliminar movimientos
st.divider()
st.subheader("🗑️ Eliminar movimiento")

if not movimientos_filtrados.empty:

    id_eliminar = st.selectbox(
        "Selecciona el ID que deseas eliminar",
        movimientos_filtrados["id"].tolist(),
        key="id_eliminar"
    )

    confirmar_eliminacion = st.checkbox(
        f"Confirmo que quiero eliminar el movimiento #{id_eliminar}"
    )

    if st.button(
        "🗑️ Eliminar definitivamente",
        disabled=not confirmar_eliminacion
    ):
        filas = eliminar_movimiento_sql(
             int(id_eliminar),
              base_datos=base_datos_actual
            )

        if filas > 0:
            st.session_state["mensaje_eliminacion"] = (
                f"Movimiento #{id_eliminar} eliminado correctamente."
            )
            st.rerun()
        else:
            st.error("No se pudo eliminar el movimiento.")

else:
    st.info("No hay movimientos disponibles para eliminar.")
