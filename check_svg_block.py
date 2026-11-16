# -*- coding: utf-8 -*-
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html", "r", encoding="utf-8") as f:
    html = f.read()

marker = 'id="venezuelaMap"'
idx = html.find(marker)
end = html.find('</svg>', idx) + 6
print("SVG block found, length:", end - idx)
print("First 300 chars of SVG:")
print(html[idx-20:idx+300].encode('ascii','replace').decode('ascii'))
