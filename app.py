import streamlit as st
import pandas as pd
import numpy as np

# Configuración inicial de la página web
st.set_page_config(page_title="Proyecto 1 - Python Fundamentals", layout="wide")

# ==========================================
# INICIALIZACIÓN DE MEMORIA (st.session_state)
# ==========================================
if "flujo_caja" not in st.session_state:
    st.session_state.flujo_caja = []

if "prod_nombres" not in st.session_state:
    st.session_state.prod_nombres = np.array([], dtype=str)
    st.session_state.prod_categorias = np.array([], dtype=str)
    st.session_state.prod_precios = np.array([], dtype=float)
    st.session_state.prod_cantidades = np.array([], dtype=int)

if "historico_funciones" not in st.session_state:
    st.session_state.historico_funciones = pd.DataFrame(columns=["Parámetro", "Resultado"])

if "crud_datos" not in st.session_state:
    st.session_state.crud_datos = pd.DataFrame(columns=["ID", "Nombre", "Valor"])


# ==========================================
# MENÚ DE NAVEGACIÓN LATERAL
# ==========================================
opcion = st.sidebar.selectbox(
    "Menú de Navegación",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)


# ==========================================
# SECCIÓN 1: HOME (PRESENTACIÓN)
# ==========================================
if opcion == "Home":
    st.title("Proyecto Aplicado - Fundamentos de Programación")
    st.subheader("Especialización en Python for Analytics")
    
    st.markdown("""
    ---
    ### **Información del Estudiante**
    * **Módulo:** Módulo 1 - Python Fundamentals
    * **Estudiate:** MSc. Daniela Jahaira Lopez Meza
    * **Año:** 2026
    
    ### **Descripción del Proyecto**
    Esta aplicación interactiva integra los conceptos fundamentales de Python aprendidos en el módulo, 
    tales como estructuras de datos, manejo de librerías como NumPy y Pandas, y la implementación 
    de lógica en un entorno web dinámico con Streamlit.
    """)


# ==========================================
# SECCIÓN 2: EJERCICIO 1 (FLUJO DE CAJA)
# ==========================================
elif opcion == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de Caja con Listas")
    st.markdown("Registre sus movimientos financieros para calcular el saldo final de caja.")
    
    with st.form("form_flujo_caja"):
        concepto = st.text_input("Concepto / Descripción")
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        valor = st.number_input("Monto (S/.)", min_value=0.0, format="%.2f")
        btn_agregar = st.form_submit_button("Agregar Movimiento")
        
        if btn_agregar and concepto:
            st.session_state.flujo_caja.append({
                "Concepto": concepto,
                "Tipo": tipo,
                "Valor": valor if tipo == "Ingreso" else -valor
            })
            st.success("Movimiento agregado.")

    if st.session_state.flujo_caja:
        df_flujo = pd.DataFrame(st.session_state.flujo_caja)
        st.dataframe(df_flujo)
        
        total_ingresos = sum(m["Valor"] for m in st.session_state.flujo_caja if m["Tipo"] == "Ingreso")
        total_gastos = sum(abs(m["Valor"]) for m in st.session_state.flujo_caja if m["Tipo"] == "Gasto")
        saldo_final = total_ingresos - total_gastos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"S/. {total_ingresos:,.2f}")
        col2.metric("Total Gastos", f"S/. {total_gastos:,.2f}")
        col3.metric("Saldo Final", f"S/. {saldo_final:,.2f}")
        
        if saldo_final >= 0:
            st.success("🟢 El flujo de caja está a favor.")
        else:
            st.error("🔴 El flujo de caja está en contra.")


# ==========================================
# SECCIÓN 3: EJERCICIO 2 (NUMPY ARRAYS)
# ==========================================
elif opcion == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro de Productos con NumPy")
    st.markdown("Formulario para registrar información guardándola en arreglos de NumPy.")
    
    with st.form("form_productos"):
        nombre = st.text_input("Nombre del Producto")
        categoria = st.selectbox("Categoría", ["Electrónicos", "Oficina", "Servicios", "Otros"])
        precio = st.number_input("Precio Unitario", min_value=0.0, format="%.2f")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        btn_prod = st.form_submit_button("Registrar Producto")
        
        if btn_prod and nombre:
            st.session_state.prod_nombres = np.append(st.session_state.prod_nombres, nombre)
            st.session_state.prod_categorias = np.append(st.session_state.prod_categorias, categoria)
            st.session_state.prod_precios = np.append(st.session_state.prod_precios, precio)
            st.session_state.prod_cantidades = np.append(st.session_state.prod_cantidades, cantidad)
            st.success("Producto registrado.")

    if len(st.session_state.prod_nombres) > 0:
        totales = st.session_state.prod_precios * st.session_state.prod_cantidades
        df_productos = pd.DataFrame({
            "Producto": st.session_state.prod_nombres,
            "Categoría": st.session_state.prod_categorias,
            "Precio": st.session_state.prod_precios,
            "Cantidad": st.session_state.prod_cantidades,
            "Total": totales
        })
        st.dataframe(df_productos)


# ==========================================
# SECCIÓN 4: EJERCICIO 3 (LIBRERÍA EXTERNA)
# ==========================================
elif opcion == "Ejercicio 3":
    st.title("Ejercicio 3 - Uso de Funciones desde Librería Externa")
    
    # Intentamos importar la función de tu profesor
    try:
        from libreria_funciones_proyecto1 import calcular_interes_compuesto
        st.success("Librería externa cargada correctamente.")
    except Exception:
        # Función de respaldo por si el archivo aún se está vinculando
        def calcular_interes_compuesto(capital, tasa, periodos):
            return capital * ((1 + tasa/100) ** periodos)

    capital = st.number_input("Capital Inicial (S/.)", min_value=0.0, value=1000.0)
    tasa = st.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.0)
    periodos = st.number_input("Años (Periodos)", min_value=1, value=5, step=1)
    
    if st.button("Ejecutar Función"):
        resultado = calcular_interes_compuesto(capital, tasa, periodos)
        st.write(f"### Resultado: S/. {resultado:,.2f}")
        
        nuevo_reg = pd.DataFrame([{"Parámetro": f"C:{capital} | T:{tasa}%", "Resultado": f"S/. {resultado:,.2f}"}])
        st.session_state.historico_funciones = pd.concat([st.session_state.historico_funciones, nuevo_reg], ignore_index=True)
        
    st.subheader("Tabla Histórica de Resultados")
    st.dataframe(st.session_state.historico_funciones)


# ==========================================
# SECCIÓN 5: EJERCICIO 4 (CRUD CON POO)
# ==========================================
elif opcion == "Ejercicio 4":
    st.title("Ejercicio 4 - Uso de Clases con Operaciones CRUD")
    
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(["Crear", "Leer", "Actualizar", "Eliminar"])
    
    with tab_crear:
        id_i = st.text_input("ID único")
        nom_i = st.text_input("Nombre")
        val_i = st.number_input("Valor", min_value=0.0)
        if st.button("Guardar"):
            if id_i and id_i not in st.session_state.crud_datos["ID"].values:
                nuevo_df = pd.DataFrame([{"ID": id_i, "Nombre": nom_i, "Valor": val_i}])
                st.session_state.crud_datos = pd.concat([st.session_state.crud_datos, nuevo_df], ignore_index=True)
                st.success("Creado.")
            else:
                st.error("ID inválido o repetido.")
                
    with tab_leer:
        st.dataframe(st.session_state.crud_datos)
        
    with tab_actualizar:
        if not st.session_state.crud_datos.empty:
            id_m = st.selectbox("Seleccione ID", st.session_state.crud_datos["ID"])
            nuevo_n = st.text_input("Nuevo Nombre")
            nuevo_v = st.number_input("Nuevo Valor", min_value=0.0)
            if st.button("Actualizar"):
                idx = st.session_state.crud_datos[st.session_state.crud_datos["ID"] == id_m].index
                st.session_state.crud_datos.loc[idx, "Nombre"] = nuevo_n
                st.session_state.crud_datos.loc[idx, "Valor"] = nuevo_v
                st.success("Actualizado.")
        else:
            st.write("Sin datos.")
            
    with tab_eliminar:
        if not st.session_state.crud_datos.empty:
            id_e = st.selectbox("Seleccione ID a borrar", st.session_state.crud_datos["ID"])
            if st.button("Eliminar", type="primary"):
                st.session_state.crud_datos = st.session_state.crud_datos[st.session_state.crud_datos["ID"] != id_e]
                st.success("Eliminado.")
        else:
            st.write("Sin datos.")
