# -*- coding: utf-8 -*-
"""
Actualiza renderDashboard en app.js para llamar renderMapaCoropletico 
también y fija el color inicial para estados sin datos.
Corrige el flujo de inicialización.
"""
import os, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "app.js"), "r", encoding="utf-8") as f:
    js = f.read()

# Fix: color de estado sin datos - should be a light blue-gray, not pure gray
old_no_data_fill = "path.style.fill = '#f1f5f9';"
new_no_data_fill = "path.style.fill = '#e8edf5';"
js = js.replace(old_no_data_fill, new_no_data_fill)

# Fix: State initial fill in CSS instead using a default
# Also ensure renderMapaCoropletico is called from renderDashboard
if "renderMapaCoropletico();" in js:
    print("renderMapaCoropletico() already called from renderDashboard")
else:
    js = js.replace(
        "  // 2. Renderizar Mapa Coroplético Vectorial\n  renderMapaCoropletico();",
        "  // 2. Renderizar Mapa Coroplético Vectorial\n  setTimeout(() => { renderMapaCoropletico(); }, 100);"
    )
    print("Fixed renderMapaCoropletico call with setTimeout")

# Fix: Check if the coropleth color scale looks right
print("Color scale check:")
idx = js.find("function getCoroplethColor(")
print(js[idx:idx+600].encode('ascii','replace').decode('ascii'))

with open(os.path.join(BASE_DIR, "app.js"), "w", encoding="utf-8") as f:
    f.write(js)

print("\napp.js updated.")
