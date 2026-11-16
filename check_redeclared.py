# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
print("Occurrences of NUCLEOS in unes_sistema_final.js:")
for m in re.finditer(r'(?:const|let|var)\s+NUCLEOS\b', text):
    print("Found:", text[m.start():m.start()+80])

print("Occurrences of PNF_LIST in unes_sistema_final.js:")
for m in re.finditer(r'(?:const|let|var)\s+PNF_LIST\b', text):
    print("Found:", text[m.start():m.start()+80])
