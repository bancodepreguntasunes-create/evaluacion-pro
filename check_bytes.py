# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html", "rb") as f:
    raw = f.read()

# find ANZO
idx = raw.find(b"ANZO")
if idx != -1:
    print("Raw bytes around ANZO:", raw[idx:idx+20])
