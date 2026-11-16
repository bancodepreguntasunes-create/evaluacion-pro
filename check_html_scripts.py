# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re
scripts = re.findall(r'<script.*?>.*?</script>', html, re.DOTALL)
for s in scripts:
    print("SCRIPT TAG:")
    if len(s) > 300:
        print(s[:200] + " ... " + s[-100:])
    else:
        print(s)
