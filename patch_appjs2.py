
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    raw = f.read()

js = raw.decode('latin-1')

# ── A. Add archivosImportados to variable declaration ───────────────────────
# Find excelRows=[], excelHeaders=[] anywhere
import re

# pattern might be: let excelRows=[], excelHeaders=[];
pattern = r"let excelRows\s*=\s*\[\s*\]\s*,\s*excelHeaders\s*=\s*\[\s*\]\s*;"
match = re.search(pattern, js)
if match:
    old = match.group(0)
    new = "let excelRows=[], excelHeaders=[], archivosImportados=[];"
    js = js.replace(old, new, 1)
    print('archivosImportados var OK (regex)')
else:
    print('Trying byte-level search for excelRows var...')
    idx = js.find('excelRows')
    while idx != -1:
        snippet = js[max(0,idx-5):idx+60]
        if 'let ' in snippet and 'excelHeaders' in snippet:
            print(f'  Found at {idx}:', repr(snippet))
            break
        idx = js.find('excelRows', idx+1)

# ── B. CAMPOS_SISTEMA: add puntaje field ────────────────────────────────────
# Find by key:'estatus' pattern
idx_cam = js.find("key:'estatus'")
if idx_cam == -1:
    idx_cam = js.find('key:"estatus"')
if idx_cam != -1:
    # Find the end of that object entry (next comma+newline after })
    end_obj = js.find('},', idx_cam)
    if end_obj == -1:
        end_obj = js.find('}', idx_cam)
    # Get the original estatus entry
    orig = js[idx_cam-4:end_obj+2]  # includes leading "  { "
    print('Found estatus campo entry:', repr(orig[:120]))
    new_entry = orig.rstrip() + "\n  { key:'puntaje',  label:'Puntaje (Opcional, si es columna separada)', req:false },"
    js = js.replace(orig, new_entry, 1)
    print('CAMPOS_SISTEMA puntaje added OK')
else:
    print('ERROR: estatus campo not found at all')

# ── C. FileReader: accumulate rows ──────────────────────────────────────────
# Use byte position we found: excelRows=json at 20448 (but re-search after prior edits)
idx_r = js.find('excelRows    = json;')
if idx_r == -1:
    idx_r = js.find('excelRows = json;')
if idx_r != -1:
    # Find the surrounding block: from 'const json = XLSX' back to previous line
    block_start = js.rfind('\n', 0, idx_r) + 1  # start of line
    # Find where mostrarMapeo line ends
    mapeo_end = js.find('\n', js.find('mostrarMapeo(file.name', idx_r)) + 1
    
    old_block = js[block_start:mapeo_end]
    print('Old FileReader block:', repr(old_block))
    
    new_block = (
        '      if (!excelRows.length) { excelHeaders = Object.keys(json[0]); }\n'
        '      excelRows = [...excelRows, ...json];\n'
        '      archivosImportados.push({ nombre: file.name, filas: json.length });\n'
        "      mostrarMapeo(archivosImportados.map(a=>a.nombre).join(' + '), excelRows.length);\n"
        "      toast('\"'+file.name+'\" cargado ('+json.length+' filas). Total: '+excelRows.length+'.','success');\n"
    )
    js = js[:block_start] + new_block + js[mapeo_end:]
    print('FileReader multi-file patched OK')
else:
    print('ERROR: excelRows=json not found')

# ── D. Update the HTML dropzone to accept multiple files ────────────────────
# This is in index.html not app.js - we'll handle that separately

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))

print('\nDone. app.js saved.')
