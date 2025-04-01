import streamlit as st
import google.generativeai as genai
import snowflake.connector
import pandas as pd

# Configuración
genai.configure(api_key="AIzaSyArSB-l3lKcyaCG_tFnb46_ZiyIDHi6cNw")
model = genai.GenerativeModel('gemini-1.5-flash')

# Conexión directa a Snowflake
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
            PRODUCT_NAME as nombre_producto,
            CATEGORY as categoria,
            DIAS_STOCK_RESTANTE as dias_restantes,
            PRIORITY_FLAG as prioridad
        FROM INVENTORY_ANALYTICS 
        LIMIT 75000
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
        
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Interfaz
st.title("📦 Asistente de Inventario")

# Carga de datos
if 'df' not in st.session_state:
    with st.spinner("Cargando productos..."):
        st.session_state.df = get_inventory_data()

if st.session_state.df is not None:
    st.success(f"Base cargada: {len(st.session_state.df)} productos")
    
    # Consulta del usuario
    pregunta = st.text_input(
        "¿Qué necesitas saber del inventario?",
        placeholder="Ej: ¿Qué productos tienen menos de 5 días de stock?",
        key="pregunta"
    )
    
    if st.button("Consultar") and pregunta:
        with st.spinner("Analizando..."):
            try:
                # Prompt 
                prompt = f"""
                Eres un asistente de inventarios. Responde en español claro y natural usando estos datos:
                
                **Datos disponibles:**
                {st.session_state.df.head().to_string()}
                
                **Pregunta:** {pregunta}
                
                **Instrucciones:**
                1. Respuesta en 1-2 oraciones completas
                2. Mencionar solo nombres de productos (sin IDs ni datos técnicos)
                3. Enfocarse en productos con menos días de stock primero
                4. No incluir códigos, columnas o términos de base de datos
                5. Si la pregunta no es de inventarios, responder:
                   "Soy un asistente especializado en inventarios. ¿En qué producto necesitas ayuda?"
                
                **Ejemplo de respuesta:**
                "Los productos con mayor riesgo son: iPhone 13, TV Samsung y Zapatos Nike, con menos de 3 días de stock."
                """
                
                response = model.generate_content(prompt)
                
                # Mostrar respuesta formateada
                st.subheader("📌 Respuesta")
                st.write(response.text)
                
            except Exception as e:
                st.error("Error al procesar la consulta")
else:
    st.warning("No se pudieron cargar los datos")

# Ejemplos de preguntas
with st.expander("💡 Ejemplos de consultas"):
    st.write("- ¿Qué productos electrónicos tienen mayor riesgo?")
    st.write("- Nombra productos con prioridad alta y bajo stock")
    st.write("- ¿Cuáles productos necesitan reabastecimiento urgente?")
