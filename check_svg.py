import sys, re
sys.stdout.reconfigure(encoding='utf-8')
f = open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', encoding='utf-8').read()

# Buscar primer path del mapa
m = re.search(r'<path id="VE-[A-Z]"[^>]*d="([^"]{0,80})', f)
if m:
    print("Primer path encontrado:")
    print(m.group(0)[:200])
else:
    print("NO se encontraron paths SVG con id VE-*")

# Buscar el bloque states-g
sg = re.search(r'<g id="states-g">(.*?)</g>', f, re.DOTALL)
if sg:
    content = sg.group(1).strip()
    print("\nstates-g tiene", len(content), "chars")
    print("Primeros 300 chars:", content[:300])
else:
    print("NO se encontro el grupo states-g")

# Verificar viewBox
vb = re.search(r'viewBox="([^"]+)"', f)
print("\nviewBox:", vb.group(1) if vb else "NO ENCONTRADO")
