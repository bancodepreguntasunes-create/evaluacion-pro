# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'\brenderMapa\b', text)]
print("Total occurrences of renderMapa:", len(matches))
for pos in matches:
    print(text[max(0, pos-40):min(len(text), pos+60)].replace('\n', ' '))
