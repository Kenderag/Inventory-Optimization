import random
from datetime import datetime, timedelta
import csv

# Define your column names
columns = ["product_id", "product_name", "category", "brand", "price", "current_stock", "reorder_level", "last_sale_date", "is_refurbished", "weight_kg"]

# Initialize an empty list to store the data
data = []

# Define the number of rows in the dataset (200)
num_rows = 200

# Loop through each row and populate it with random data
for i in range(num_rows):
    product_id = f"P{str(i+1).zfill(3)" if i < 10 else "P" + str(i+1)
    product_name = f"Product {i+1} Name"
    category = random.choice(["Electronics", "Computers", "Wearables", "Drones", "Audio"])
    brand = random.choice(["TechBrand", "GadgetPlus", "UltraTech", "AeroTech", "SoundMaster"])
    price = round(random.uniform(50.00, 2000.00), 2)
    current_stock = random.randint(0, 200) if not i % 10 else None
    reorder_level = random.randint(5, 30) if not i % 7 else None
    last_sale_date = datetime.now().strftime("%Y-%m-%d") if random.random() > 0.2 or not i % 10 else None
    is_refurbished = bool(random.getrandbits(1))
    weight_kg = round(random.uniform(0.05, 2.00), 3) if not i % 10 else None

    # Append the row to the data list
    data.append([product_id, product_name, category, brand, price, current_stock, reorder_level, last_sale_date, is_refurbished, weight_kg])

# Write the data to a CSV file
with open("synthetic_dataset.csv", "w", newline="") as csvfile:
    fieldnames = columns
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    for row in data:
        writer.writerow({c: str(v) for c, v in zip(columns, row)})