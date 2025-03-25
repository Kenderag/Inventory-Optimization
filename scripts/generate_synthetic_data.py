import random
from datetime import datetime, timedelta
import pandas as pd

# Configuración
num_rows = 200
output_file = "tech_inventory.csv"

# Columnas y reglas
columns = [
    "product_id", "product_name", "category", "brand", 
    "price", "current_stock", "reorder_level", 
    "last_sale_date", "is_refurbished", "weight_kg"
]

# Datos de ejemplo realistas
categories = ["Electronics", "Computers", "Wearables", "Drones", "Audio"]
brands = ["TechBrand", "GadgetPlus", "UltraTech", "AeroTech", "SoundMaster"]
product_names = ["Quantum Laptop", "Neural Phone", "Holo Glasses", "Nano Drone", "Sound Sphere"]

# Generación de datos
data = []
for i in range(num_rows):
    product_id = f"P{str(i+1).zfill(3)}"
    product_name = f"{random.choice(product_names)} {random.randint(1, 5)}"
    category = random.choice(categories)
    brand = random.choice(brands) if random.random() > 0.1 else None  # 10% nulos
    price = round(random.uniform(50, 2000), 2)
    current_stock = random.randint(0, 200) if random.random() > 0.05 else None  # 5% nulos
    reorder_level = random.randint(5, 30) if random.random() > 0.15 else None  # 15% nulos
    
    # ¡LÍNEA CRÍTICA CORREGIDA! (Versión simplificada)
    days_ago = random.randint(1, 60)
    last_sale_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d") if random.random() > 0.2 else None  # 20% nulos
    
    is_refurbished = random.random() > 0.7  # 30% True
    weight_kg = round(random.uniform(0.05, 2.0), 2) if random.random() > 0.1 else None  # 10% nulos
    
    data.append([
        product_id, product_name, category, brand, price,
        current_stock, reorder_level, last_sale_date,
        is_refurbished, weight_kg
    ])

# Guardar CSV
df = pd.DataFrame(data, columns=columns)
df.to_csv(output_file, index=False)
print(f"✅ Dataset generado en '{output_file}'")