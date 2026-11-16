# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\data.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("data.js length:", len(text))
print("data.js content:")
print(text[:1000].encode('ascii', 'replace').decode('ascii'))
