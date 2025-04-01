import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, when

# ===== CONFIGURACIÓN ESPECÍFICA =====
os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-11.0.26.4-hotspot"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PYSPARK_PYTHON"] = r"C:\Users\k\Desktop\Inventory Optimization\venv\Scripts\python.exe"

# ===== INICIALIZACIÓN SPARK =====
spark = SparkSession.builder\
    .appName("InventoryETL")\
    .config("spark.jars.packages", "net.snowflake:spark-snowflake_2.12:2.12.0-spark_3.5")\
    .master("local[*]")\
    .getOrCreate()

# ===== ETL PRINCIPAL =====
try:
    input_path = r"C:\Users\k\Desktop\Inventory Optimization\data\tech_inventory_150k.csv"
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    df_transformed = df.withColumn(
        "DIAS_STOCK_RESTANTE",
        when(col("DAILY_SALES_AVG") > 0, 
            round(col("CURRENT_STOCK") / col("DAILY_SALES_AVG"), 1)
        ).otherwise(None)
    ).withColumn(
        "PRIORITY_FLAG",
        (col("ABC_CLASS") == "A") & (col("STOCK_STATUS") == "RISK")
    )

    df_transformed.write\
        .format("snowflake")\
        .options(
            sfUrl="NDVNNHP-ZM24191.snowflakecomputing.com",
            sfUser="KENDERAG",
            sfPassword="Hp7g33snkm64alqxlixn",
            sfDatabase="INV_DB",
            sfSchema="PUBLIC",
            sfWarehouse="COMPUTE_WH"
        )\
        .option("dbtable", "INVENTORY_ANALYTICS")\
        .mode("append")\
        .save()

    print("✅ ETL completado!")

except Exception as e:
    print(f"❌ Error: {e}")
    raise

finally:
    spark.stop()