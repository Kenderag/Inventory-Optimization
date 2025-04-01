import snowflake.connector

SNOWFLAKE_CONFIG = {
    "user": "KENDERAG",
    "password": "Hp7g33snkm64alqxlixn",
    "account": "NDVNNHP-ZM24191",
    "warehouse": "COMPUTE_WH",
    "database": "INV_DB",
    "schema": "SYSADMIN"
}

try:
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    print("Conexión exitosa")
except Exception as e:
    print(f"Error al conectar: {e}")
