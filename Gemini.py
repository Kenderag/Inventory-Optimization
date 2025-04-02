import streamlit as st
import google.generativeai as genai
import snowflake.connector
import pandas as pd
from datetime import datetime

# Configuración de Gemini
genai.configure(api_key="AIzaSyArSB-l3lKcyaCG_tFnb46_ZiyIDHi6cNw")
model = genai.GenerativeModel('gemini-1.5-flash')

# Conexión a Snowflake
def get_inventory_data():
    try:
        conn = snowflake.connector.connect(
            user="KENDERAG",
            password="Hp7g33snkm64alqxlixn",
            account="NDVNNHP-ZM24191",
            warehouse="COMPUTE_WH",
            database="INV_DB",
            schema="SYSADMIN"
        )
        
        query = """
        SELECT 
            PRODUCT_ID,
            PRODUCT_NAME,
            CATEGORY,
            BRAND,
            DIAS_STOCK_RESTANTE,
            PRIORITY_FLAG,
            STOCK_STATUS,
            ABC_CLASS,
            REGION,
            STORE_ID,
            LAST_RESTOCK_DATE
        FROM INVENTORY_ANALYTICS 
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Convertir fechas a formato legible
        df['LAST_RESTOCK_DATE'] = pd.to_datetime(df['LAST_RESTOCK_DATE']).dt.strftime('%d/%m/%Y')
        return df
        
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Función para traducir preguntas naturales a filtros técnicos
def translate_query(natural_language):
    natural_language = natural_language.lower()
    
    filters = {
        'productos_urgentes': ['urgente', 'prioridad', 'crítico', 'importante'],
        'stock_bajo': ['agotarse', 'poco stock', 'riesgo', 'bajo stock', 'reponer'],
        'exceso_stock': ['exceso', 'demasiado stock', 'sobrestock'],
        'reabastecimiento': ['reponer', 'pedir', 'comprar', 'reabastecer']
    }
    
    for key, terms in filters.items():
        if any(term in natural_language for term in terms):
            return key
    return None

# Interfaz de usuario
st.set_page_config(page_title="Asistente de Inventario", layout="wide")
st.title("📊 Asistente Inteligente de Inventario")

# Carga de datos
if 'df' not in st.session_state:
    with st.spinner("Analizando inventario..."):
        st.session_state.df = get_inventory_data()
        if st.session_state.df is None:
            st.warning("Modo demo activado (datos de ejemplo)")
            st.session_state.df = pd.DataFrame({
                'PRODUCT_NAME': ['Laptop HP', 'TV Samsung', 'Cámara Sony', 'Tablet Apple'],
                'CATEGORY': ['Electrónicos', 'Electrónicos', 'Electrónicos', 'Electrónicos'],
                'DIAS_STOCK_RESTANTE': [3, 15, 2, 7],
                'PRIORITY_FLAG': [True, False, True, False],
                'STOCK_STATUS': ['RISK', 'OK', 'RISK', 'OK'],
                'LAST_RESTOCK_DATE': ['01/06/2024', '15/05/2024', '03/06/2024', '10/05/2024']
            })

# Panel de consulta
col1, col2 = st.columns([3, 1])
with col1:
    pregunta = st.text_input(
        "Escribe tu pregunta sobre el inventario:",
        placeholder="Ej: ¿Qué productos necesitamos reponer con urgencia?",
        key="pregunta"
    )

with col2:
    st.markdown("""
    <style>
    .stButton>button {
        height: 3em;
        margin-top: 1.8em;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Analizar", type="primary"):
        st.session_state.pregunta_actual = pregunta

# Procesamiento de preguntas
if 'pregunta_actual' in st.session_state and st.session_state.df is not None:
    with st.spinner("Buscando la mejor respuesta..."):
        try:
            # Traducción a filtro técnico
            filtro = translate_query(st.session_state.pregunta_actual)
            
            # Construcción del prompt dinámico
            prompt = f"""
            Eres un experto en gestión de inventarios para minoristas. Responde en español natural usando SOLO estos datos:
            
            **Datos actuales (ejemplo):**
            {st.session_state.df[['PRODUCT_NAME', 'CATEGORY', 'DIAS_STOCK_RESTANTE', 'PRIORITY_FLAG', 'LAST_RESTOCK_DATE']].head().to_string(index=False)}
            
            **Pregunta del usuario:** "{st.session_state.pregunta_actual}"
            
            **Instrucciones:**
            1. Lenguaje: Simple y profesional (sin términos técnicos)
            2. Estructura:
               - [Icono] [Contexto]: [Productos] ([Días restantes], [Última reposición])
               - Acción: [Sugerencia específica]
            3. Iconos:
               - 🚨 Para productos críticos (<3 días o prioridad alta)
               - ⚠️ Para productos en riesgo (3-7 días)
               - ℹ️ Para información general
            4. Sugerencias:
               - Urgente: "Contactar proveedor hoy"
               - Riesgo: "Planificar reposición en 48h"
               - Exceso: "Considerar promociones"
            """
            
            # Generar respuesta
            response = model.generate_content(prompt)
            
            # Mostrar resultados
            st.subheader("🔍 Análisis de Inventario")
            st.markdown(f"**Pregunta:** {st.session_state.pregunta_actual}")
            st.markdown(f"**Respuesta:** {response.text}")
            
            # Tabla detallada (si aplica)
            if filtro:
                st.subheader("📋 Detalles Técnicos")
                if filtro == 'productos_urgentes':
                    df_filtrado = st.session_state.df[st.session_state.df['PRIORITY_FLAG'] == True]
                elif filtro == 'stock_bajo':
                    df_filtrado = st.session_state.df[st.session_state.df['DIAS_STOCK_RESTANTE'] < 7]
                elif filtro == 'exceso_stock':
                    df_filtrado = st.session_state.df[st.session_state.df['DIAS_STOCK_RESTANTE'] > 30]
                
                if not df_filtrado.empty:
                    st.dataframe(
                        df_filtrado[['PRODUCT_NAME', 'CATEGORY', 'DIAS_STOCK_RESTANTE', 'LAST_RESTOCK_DATE']],
                        column_config={
                            "DIAS_STOCK_RESTANTE": st.column_config.NumberColumn(
                                "Días Restantes",
                                format="%d días",
                                help="Stock proyectado"
                            ),
                            "LAST_RESTOCK_DATE": "Última Reposición"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
            
        except Exception as e:
            st.error(f"Error al procesar: {str(e)}")

# Ejemplos de preguntas
with st.expander("💡 Ejemplos de preguntas"):
    st.markdown("""
    - **Urgencia:** "¿Qué productos necesitan atención inmediata?"
    - **Stock bajo:** "¿Hay algo que se vaya a agotar esta semana?"
    - **Exceso:** "¿Tenemos productos acumulados?"
    - **Categorías:** "¿Qué electrónicos están bajos de stock?"
    - **Reposición:** "Muéstrame los electrónicos más urgentes""
    """)

# Footer
st.markdown("---")
st.markdown("🔄 Fecha Actual " + datetime.now().strftime("%d/%m/%Y %H:%M"))