# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('function renderMapa(')
print(text[idx:idx+1500].encode('ascii', 'replace').decode('ascii'))
