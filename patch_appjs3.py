
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    raw = f.read()
js = raw.decode('latin-1')

# ── A. Separate variable declarations ───────────────────────────────────────
old_a = "let excelRows    = [];\nlet excelHeaders = [];"
new_a  = "let excelRows    = [];\nlet excelHeaders = [];\nlet archivosImportados = [];"
if old_a in js:
    js = js.replace(old_a, new_a, 1)
    print('archivosImportados var OK')
else:
    print('WARNING: separate let declarations not found')
    print(repr(js[520:600]))

# ── B. CAMPOS_SISTEMA: find estatus line and add puntaje after ───────────────
# Search for the array literal containing key:'estatus'
# Pattern used in this file:
idx = js.find("key: 'estatus'")
if idx == -1: idx = js.find("key:'estatus'")
if idx != -1:
    # Find next newline after the closing } of that object
    close = js.find('}', idx)
    comma_or_newline = js.find('\n', close)
    orig_line = js[close:comma_or_newline+1]
    puntaje_entry = "\n  { key: 'puntaje',  label: 'Puntaje (Opcional, columna separada)', req: false },"
    js = js[:comma_or_newline+1] + puntaje_entry + js[comma_or_newline+1:]
    print('CAMPOS_SISTEMA puntaje added OK')
else:
    print('ERROR: estatus campo still not found, searching context...')
    for kw in ["CAMPOS_SISTEMA", "campos_sistema", "CamposSistema", "camposSistema"]:
        i = js.find(kw)
        if i != -1:
            print(f'Found {kw} at {i}:', repr(js[i:i+300]))
            break

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))
print('app.js saved.')
