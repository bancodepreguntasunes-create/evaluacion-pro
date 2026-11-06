import json
import re

# Load students from datos_importados.json
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
students = datos['estudiantes']

print(f"Loaded {len(students)} students from datos_importados.json")

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/build_full_appjs.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Let's check how build_full_appjs.py creates app.js
# Or read app.js
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the commented out CAMPOS_SISTEMA if present
code = code.replace('// const CAMPOS_SISTEMA =', 'const CAMPOS_SISTEMA =')

# Save cleanly to both app.js and unes_core_v5.js
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_core_v5.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed CAMPOS_SISTEMA in both files successfully!")
