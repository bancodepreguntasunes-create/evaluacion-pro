# -*- coding: utf-8 -*-
import os, sys, re, json

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

with open(os.path.join(BASE_DIR, "unes_sistema_final.js"), "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

with open(os.path.join(BASE_DIR, "styles.css"), "r", encoding="utf-8", errors="ignore") as f:
    css = f.read()

print("Verificación:")
print("1. btnSyncDB en index.html:", "btnSyncDB" in html)
print("2. forzarSincronizacionOficial en js:", "forzarSincronizacionOficial" in js)
print("3. stat-card-executive en css:", "stat-card-executive" in css)
print("4. dash-charts-grid en html y css:", "dash-charts-grid" in html and "dash-charts-grid" in css)
print("5. Script tag con v10:", "unes_sistema_final.js?v=20261113_v10" in html)

m = re.search(r'const INITIAL_ESTUDIANTES = (\[.*?\]);', js)
if m:
    data = json.loads(m.group(1))
    print(f"6. INITIAL_ESTUDIANTES total: {len(data)}")
    ap = sum(1 for x in data if x.get('estatus') == 'Aprobado')
    rep = sum(1 for x in data if x.get('estatus') == 'Reprobado')
    print(f"   Aprobados: {ap}, Reprobados: {rep}")
