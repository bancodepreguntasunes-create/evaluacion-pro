# -*- coding: utf-8 -*-
import json, re

with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

m = re.search(r'const INITIAL_ESTUDIANTES = (\[.*?\]);', text)
if m:
    data = json.loads(m.group(1))
    estados = set(e.get('estado') for e in data)
    print("Estados in dataset:", sorted([str(s) for s in estados]))
