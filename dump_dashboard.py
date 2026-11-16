# -*- coding: utf-8 -*-
import os, sys, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

v_idx = text.find('id="view-dashboard"')
next_idx = text.find('id="view-estudiantes"')

print(f"v_idx: {v_idx}, next_idx: {next_idx}")
snippet = text[v_idx:next_idx]

with open(os.path.join(BASE_DIR, "snippet_dashboard.html"), "w", encoding="utf-8") as f:
    f.write(snippet)

print("Snippet saved. First 500 chars:")
print(snippet[:500].encode('ascii', 'replace').decode('ascii'))
print("Last 500 chars:")
print(snippet[-500:].encode('ascii', 'replace').decode('ascii'))
