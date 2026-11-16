# -*- coding: utf-8 -*-
import os, sys, re, json

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

replacements = {
    'ANZOTEGUI': 'ANZOÁTEGUI',
    'ANZO?TEGUI': 'ANZOÁTEGUI',
    'BOLVAR': 'BOLÍVAR',
    'BOL?VAR': 'BOLÍVAR',
    'FALCN': 'FALCÓN',
    'FALC?N': 'FALCÓN',
    'GURICO': 'GUÁRICO',
    'GU?RICO': 'GUÁRICO',
    'MRIDA': 'MÉRIDA',
    'M?RIDA': 'MÉRIDA',
    'TCHIRA': 'TÁCHIRA',
    'T?CHIRA': 'TÁCHIRA'
}

def clean_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    count = 0
    for bad, good in replacements.items():
        if bad in content:
            content = content.replace(bad, good)
            count += 1
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{filename}: limpiado con éxito ({count} reemplazos).")

for fn in ["index.html", "unes_sistema_final.js", "app.js", "datos_importados.json"]:
    clean_file(fn)

print("Nombres de estados normalizados con UTF-8 perfecto.")
