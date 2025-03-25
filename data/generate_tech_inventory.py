import ollama
import pandas as pd

# Configuration
num_rows = 200
output_file = "tech_inventory.csv"  # Nombre en inglés

# Prompt for Mistral (in English)
prompt = f"""
Generate a synthetic dataset of {num_rows} technology products in CSV format with these columns:
1. product_id (format P001, P002...),
2. product_name (e.g., "Smartphone X Pro", "Tablet Lite"),
3. category (Electronics, Computers, Wearables, Drones, Audio),
4. brand (TechBrand, GadgetPlus, UltraTech, AeroTech, SoundMaster),
5. price (float between 50.00 and 2000.00 USD),
6. current_stock (int 0-200, 5% nulls),
7. reorder_level (int 5-30, 15% nulls),
8. last_sale_date (YYYY-MM-DD, 20% nulls),
9. is_refurbished (boolean),
10. weight_kg (float 0.05-2.00, 10% nulls).

Rules:
- Use commas as delimiters.
- Include null values as per specified percentages.
- Maintain consistent ranges and formats.

Example of 2 rows:
P001,Smartphone X Pro,Electronics,TechBrand,899.99,45,20,2024-03-15,False,0.18
P002,Tablet Lite,Electronics,,199.99,,30,,True,0.45
"""

# Generate data with Mistral
print("Generating data with Mistral... (this may take a few minutes)")
response = ollama.generate(
    model="mistral",
    prompt=prompt,
    options={"temperature": 0.7}
)

# Save to CSV
with open(output_file, "w") as f:
    f.write(response["response"])

print(f"✅ Dataset generated at '{output_file}'")