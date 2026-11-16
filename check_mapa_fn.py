# -*- coding: utf-8 -*-
"""
Corrige la función renderMapaCoropletico en app.js para que:
1. Asigne fill correctamente a los polígonos SVG reales
2. Inicialice el mapa al cargar el dashboard
3. Tenga el estado sin datos en gris claro (#cbd5e1)
"""
import os, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "app.js"), "r", encoding="utf-8") as f:
    js = f.read()

# Fix getCoroplethColor - return string not needed to change
# Check renderMapaCoropletico function
idx = js.find("function renderMapaCoropletico()")
print("renderMapaCoropletico found at:", idx)
print(js[idx:idx+800].encode('ascii','replace').decode('ascii'))
