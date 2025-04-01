import snowflake.connector
from dotenv import load_dotenv
import os

# --- Configuración exacta ---
load_dotenv()

# 1. Ruta del CSV 
csv_path = r"C:\Users\k\Desktop\Inventory Optimization\data\tech_inventory_150k.csv"

# 2. Parámetros
database = "INV_DB"        
schema = "PUBLIC"          
table = "TECH_INVENTORY"   
role = "ACCOUNTADMIN"      

# --- Conexión con parámetros exactos ---
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=database,     
    schema=schema,          
    role=role              
)

cursor = conn.cursor()

try:
    # 1. Subir archivo 
    put_command = f"""
        PUT 'file://{csv_path.replace(os.sep, "/")}' @~
        AUTO_COMPRESS = FALSE
        OVERWRITE = TRUE
    """
    cursor.execute(put_command)
    print("✅ Archivo subido a la etapa de usuario")


    copy_command = f"""
        COPY INTO {database}.{schema}.{table}
        FROM @~/{os.path.basename(csv_path)}
        FILE_FORMAT = (TYPE = CSV, SKIP_HEADER = 1)
    """
    cursor.execute(copy_command)
    print(f"✅ Datos cargados en {table}. Filas insertadas: {cursor.rowcount}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    cursor.execute("ROLLBACK")

finally:
    cursor.close()
    conn.close()