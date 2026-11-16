# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\dump_out.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("Dump length:", len(text))
print("Dump text:")
print(text.encode('ascii', 'replace').decode('ascii'))
