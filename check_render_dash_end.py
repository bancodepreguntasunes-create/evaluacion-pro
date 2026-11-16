# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find("function renderGraficos(est)")
print(text[idx-500:idx].encode('ascii', 'replace').decode('ascii'))
