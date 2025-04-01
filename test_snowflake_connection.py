import os
from snowflake.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del .env

def test_connection():
    try:
        # Configuración de la conexión
        conn = connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE")
        )
        print("✅ ¡Conexión exitosa!")
        
        # Ejecutar una consulta de prueba
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP() AS current_time, CURRENT_VERSION() AS snowflake_version")
        result = cursor.fetchone()
        print(f"📅 Fecha y hora en Snowflake: {result[0]}")
        print(f"❄️ Versión de Snowflake: {result[1]}")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()