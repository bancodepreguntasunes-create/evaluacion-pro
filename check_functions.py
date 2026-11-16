# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Let's check the function definitions
import re
functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', code)
print(f"Total functions found: {len(functions)}")
print("Sample functions:", functions[:15])

# Let's check if there are syntax errors in the new functions
for fn_name in ['renderDashboard', 'renderGraficos', 'cargarDB', 'renderMapa']:
    idx = code.find(f"function {fn_name}")
    print(f"Function {fn_name} found at {idx}")
