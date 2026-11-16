# -*- coding: utf-8 -*-
import os, sys

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "unes_sistema_final.js"), "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx1 = text.find("function renderDashboard()")
idx2 = text.find("function renderGraficos")
print("renderDashboard to renderGraficos:", idx2 - idx1)
print(text[idx1+1400:idx2].encode('ascii', 'replace').decode('ascii'))
