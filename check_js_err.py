# -*- coding: utf-8 -*-
import json, re

with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    js_content = f.read()

print("JS Length:", len(js_content))

# Check for syntax errors by analyzing structure or searching for unclosed quotes/brackets
# Let's check the DOMContentLoaded and initial calls
print("DOMContentLoaded presence:")
for line in js_content.splitlines():
    if "DOMContentLoaded" in line or "cargarDB" in line[:30]:
        print(line[:100])
