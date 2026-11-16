# -*- coding: utf-8 -*-
"""
Verifica que el mapa SVG real está en index.html y que el CSS está bien.
Versiona index.html con el nuevo app.js correcto.
"""
import os, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

# Confirm proper data-estado attributes match what the JS expects
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

estados_in_svg = re.findall(r'data-estado="([^"]+)"', html)
print("States in SVG:", sorted(set(estados_in_svg)))
print("Total path elements:", len(estados_in_svg))

# Verify onclick matches data-estado
onclick_states = re.findall(r"seleccionarEstado\('([^']+)'\)", html)
print("States with onclick:", sorted(set(onclick_states)))

# Check that CSS has correct .map-state fill
with open(os.path.join(BASE_DIR, "styles.css"), "r", encoding="utf-8") as f:
    css = f.read()

idx = css.rfind('.map-state {')
print("\n.map-state block:")
print(css[idx:idx+300].encode('ascii','replace').decode('ascii'))

# Update cache-busting version 
html = html.replace('app.js?v=20261116_prod', 'app.js?v=20261116b')
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("\nVersion bumped to 20261116b")
