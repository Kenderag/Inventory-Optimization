import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os

# Configuración
output_file = "data/tech_inventory_150k.csv"
num_rows = 150000  # 150K registros
os.makedirs("data", exist_ok=True)

# Opciones para datos realistas
categories = ["Smartphone", "Laptop", "Tablet", "Smartwatch", "Headphones"]
brands = ["Apple", "Samsung", "Sony", "Huawei", "Xiaomi"]
regions = ["NORTH", "SOUTH", "EAST", "WEST"]
stores_per_region = 3  # 3 tiendas por región
fake = Faker()

# Generar datos
def generate_product_id(start_id):
    return f"P{str(start_id).zfill(5)}"  # Formato: P00001

data = []
for i in range(1, num_rows + 1):
    # --- Identificadores ---
    product_id = generate_product_id(i)
    region = np.random.choice(regions)
    store_id = f"STORE_{region}_{np.random.randint(1, stores_per_region + 1)}"
    
    # --- Categoría y Marca ---
    category = np.random.choice(categories)
    brand = np.random.choice(brands)
    
    # --- Lógica de Stock y Ventas ---
    daily_sales_avg = np.random.randint(1, 20)  # Demanda base
    
    # Ajustar demanda por región (ej: NORTH vende más)
    if region == "NORTH":
        daily_sales_avg = int(daily_sales_avg * 1.5)
    
    # Generar current_stock con desabastecimientos/excesos
    if np.random.random() < 0.15:  # 15% en riesgo
        current_stock = np.random.randint(0, daily_sales_avg * 5)
    elif np.random.random() < 0.10:  # 10% en exceso
        current_stock = np.random.randint(daily_sales_avg * 30, daily_sales_avg * 50)
    else:  # 75% normal
        current_stock = np.random.randint(daily_sales_avg * 5, daily_sales_avg * 20)
    
    # --- Clasificación ABC ---
    abc_class = "A" if daily_sales_avg > 15 else ("B" if daily_sales_avg > 5 else "C")
    
    # --- Estado de Stock ---
    stock_status = (
        "RISK" if current_stock < daily_sales_avg * 5 
        else "EXCESS" if current_stock > daily_sales_avg * 30 
        else "OK"
    )
    
    # --- Fechas ---
    last_restock_date = datetime.now() - timedelta(days=np.random.randint(1, 60))
    
    # --- Append Record ---
    data.append({
        "product_id": product_id,
        "product_name": f"{brand} {category} {fake.word().capitalize()}",
        "category": category,
        "brand": brand,
        "price": round(np.random.uniform(50, 2000), 2),
        "current_stock": current_stock,
        "daily_sales_avg": daily_sales_avg,
        "region": region,
        "store_id": store_id,
        "stock_status": stock_status,
        "ABC_CLASS": abc_class,
        "last_restock_date": last_restock_date
    })

# Guardar CSV
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)
print(f"✅ {num_rows} registros guardados en {output_file}")
print("Columnas generadas:", df.columns.tolist())