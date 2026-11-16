# -*- coding: utf-8 -*-
"""
Extrae los paths SVG reales de Venezuela del archivo venezuela_real.svg
y los clasifica por estado venezolano con sus IDs correctos.
"""
import re

with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\archivo_historico\venezuela_real.svg", "r", encoding="utf-8", errors="ignore") as f:
    svg_text = f.read()

# Extraer todos los paths con title y id
paths = re.findall(r'<path\s+(.*?)/>', svg_text, re.DOTALL)

estados_venezuela = {
    'VE-A': 'CARACAS',
    'VE-B': 'ANZOÁTEGUI',
    'VE-C': 'APURE',
    'VE-D': 'ARAGUA',
    'VE-E': 'BARINAS',
    'VE-F': 'BOLÍVAR',
    'VE-G': 'CARABOBO',
    'VE-H': 'COJEDES',
    'VE-I': 'FALCÓN',
    'VE-J': 'GUÁRICO',
    'VE-K': 'LARA',
    'VE-L': 'MÉRIDA',
    'VE-M': 'MIRANDA',
    'VE-N': 'MONAGAS',
    'VE-O': 'NUEVA ESPARTA',
    'VE-P': 'PORTUGUESA',
    'VE-R': 'SUCRE',
    'VE-S': 'TÁCHIRA',
    'VE-T': 'TRUJILLO',
    'VE-U': 'YARACUY',
    'VE-V': 'ZULIA',
    'VE-W': 'AMAZONAS',
    'VE-X': 'LA GUAIRA',
    'VE-Y': 'DELTA AMACURO',
}

result_paths = {}
for p in paths:
    id_m = re.search(r'id="([^"]+)"', p)
    d_m = re.search(r'd="([^"]+)"', p)
    title_m = re.search(r'title="([^"]+)"', p)
    if id_m and d_m:
        pid = id_m.group(1)
        d = d_m.group(1)
        title = title_m.group(1) if title_m else pid
        if pid in estados_venezuela:
            result_paths[pid] = {'estado': estados_venezuela[pid], 'd': d}
            print(f"Found: {pid} -> {estados_venezuela[pid]} ({len(d)} chars)")

print(f"\nTotal estados venezolanos encontrados: {len(result_paths)}")

# Guardar para usar en la construcción del mapa
import json
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\ve_paths.json", "w", encoding="utf-8") as f:
    json.dump(result_paths, f, ensure_ascii=False, indent=2)
print("Guardado en ve_paths.json")
