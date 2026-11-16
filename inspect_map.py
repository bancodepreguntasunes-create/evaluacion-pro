import json, re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\archivo_historico\venezuela_real.svg', 'r', encoding='utf-8', errors='ignore') as f:
    txt = f.read()

print("File size:", len(txt))
m_vb = re.search(r'viewBox=["\']([^"\']+)["\']', txt)
m_w = re.search(r'width=["\']([^"\']+)["\']', txt)
m_h = re.search(r'height=["\']([^"\']+)["\']', txt)

print("viewBox:", m_vb.group(1) if m_vb else "None")
print("width:", m_w.group(1) if m_w else "None")
print("height:", m_h.group(1) if m_h else "None")

# Inspect ve_paths.json
vp = json.load(open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\ve_paths.json', 'r', encoding='utf-8'))
print("\nStates in ve_paths.json:")
for k, v in vp.items():
    print(k, v.get('estado'), "path len:", len(v.get('d', '')))
