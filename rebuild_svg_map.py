# -*- coding: utf-8 -*-
"""
Reconstruye el index.html con el mapa vectorial real de Venezuela
usando los polígonos reales extraídos del SVG oficial.
"""
import json, re, os

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "ve_paths.json"), "r", encoding="utf-8") as f:
    ve_paths = json.load(f)

# Centroides aproximados por estado (en viewBox 600x527) para las etiquetas
CENTROIDES = {
    'VE-A': (290, 94, 'D.C.'),
    'VE-B': (395, 175, 'Anzoátegui'),
    'VE-C': (220, 300, 'Apure'),
    'VE-D': (265, 115, 'Aragua'),
    'VE-E': (170, 230, 'Barinas'),
    'VE-F': (430, 320, 'Bolívar'),
    'VE-G': (242, 110, 'Carabobo'),
    'VE-H': (230, 175, 'Cojedes'),
    'VE-I': (200, 72, 'Falcón'),
    'VE-J': (305, 205, 'Guárico'),
    'VE-K': (175, 140, 'Lara'),
    'VE-L': (130, 215, 'Mérida'),
    'VE-M': (318, 110, 'Miranda'),
    'VE-N': (450, 185, 'Monagas'),
    'VE-O': (530, 95, 'Nva. Esparta'),
    'VE-P': (195, 185, 'Portuguesa'),
    'VE-R': (460, 140, 'Sucre'),
    'VE-S': (95, 250, 'Táchira'),
    'VE-T': (148, 175, 'Trujillo'),
    'VE-U': (220, 118, 'Yaracuy'),
    'VE-V': (88, 130, 'Zulia'),
    'VE-W': (280, 420, 'Amazonas'),
    'VE-X': (288, 80, 'La Guaira'),
    'VE-Y': (530, 215, 'Delta Amacuro'),
}

# Construir el contenido SVG con polígonos reales
svg_paths_html = ""
for pid, data in ve_paths.items():
    estado = data['estado']
    d_path = data['d']
    cx, cy, label = CENTROIDES.get(pid, (300, 250, estado))

    svg_paths_html += f"""              <path
                id="map-{pid}"
                class="map-state"
                data-estado="{estado}"
                data-pid="{pid}"
                d="{d_path}"
                onclick="seleccionarEstado('{estado}')"
                onmouseenter="hoverEstado('{estado}', event)"
                onmouseleave="leaveEstado()"
              />
              <text class="map-label" x="{cx}" y="{cy}" onclick="seleccionarEstado('{estado}')">{label}</text>
"""

print("Paths SVG generados correctamente.")

# Leer index.html
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Reemplazar el bloque SVG de Venezuela
svg_start = html.find('<svg id="venezuelaMap"')
svg_end = html.find('</svg>', svg_start) + 6  # include closing tag
old_svg = html[svg_start:svg_end]

new_svg = f"""<svg id="venezuelaMap" viewBox="0 0 600 527" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
              <!-- Polígonos Reales de los 24 Estados de Venezuela -->
{svg_paths_html}
              <!-- Capa dinámica de Pines de Núcleos (Georreferenciados) -->
              <g id="nucleosLayer"></g>
            </svg>"""

html = html[:svg_start] + new_svg + html[svg_end:]

with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("index.html actualizado con el mapa vectorial real.")
print(f"SVG anterior ({len(old_svg)} chars) → SVG nuevo ({len(new_svg)} chars)")
