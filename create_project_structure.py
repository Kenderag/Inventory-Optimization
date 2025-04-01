import os

project_structure = {
    'Inventory Optimization': [
        'data/raw',
        'data/processed',
        'notebooks',
        'scripts',
        'pipelines',
        'dashboards/powerbi',
        'genai_app/prompts',
    ]
}

base_path = os.path.expanduser('~') + '/Desktop'  

for project, folders in project_structure.items():
    for folder in folders:
        dir_path = os.path.join(base_path, project, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Carpeta creada: {dir_path}")

print("✨ Estructura del proyecto .")