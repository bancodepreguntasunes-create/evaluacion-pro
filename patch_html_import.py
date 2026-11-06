
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','rb') as f:
    html = f.read().decode('utf-8', 'replace')

# ── 1. File input: add multiple attribute ────────────────────────────────────
old_input = 'id="fileInput" accept=".xlsx,.xls"'
new_input = 'id="fileInput" accept=".xlsx,.xls" multiple'
if old_input in html:
    html = html.replace(old_input, new_input, 1)
    print('file input multiple OK')
else:
    # Try without quotes style
    idx = html.find('fileInput')
    print(f'fileInput at {idx}:', html[idx:idx+100])

# ── 2. Dropzone: update label text to reflect multiple files ─────────────────
old_drop_label = 'Arrastra tu archivo .xlsx aquí'
new_drop_label = 'Arrastra uno o más archivos .xlsx aquí'
if old_drop_label in html:
    html = html.replace(old_drop_label, new_drop_label, 1)
    print('dropzone label OK')
else:
    old_drop_label2 = 'Arrastra tu archivo'
    idx = html.find(old_drop_label2)
    print(f'drop label at {idx}:', html[idx:idx+80])

# ── 3. Update the "Seleccionar archivo" button text ──────────────────────────
old_btn = '>Seleccionar archivo<'
new_btn = '>Seleccionar archivo(s)<'
if old_btn in html:
    html = html.replace(old_btn, new_btn, 1)
    print('select btn label OK')

# ── 4. Add file list indicator div after dropzone if not present ─────────────
if 'archivos-cargados-lista' not in html:
    old_anchor = 'id="importConfig"'
    idx = html.find(old_anchor)
    if idx != -1:
        # Insert a div that JS will populate to show loaded files
        insert = '\n    <div id="archivos-cargados-lista" style="display:none;margin-bottom:12px;"></div>\n    '
        html = html[:idx] + insert + html[idx:]
        print('archivos-cargados-lista div added OK')
    else:
        print('WARNING: importConfig anchor not found')

# ── 5. Add a "Limpiar archivos" button near the import config area ───────────
old_reset_btn = "onclick=\"resetImport()\""
if old_reset_btn in html:
    # Already exists somewhere, that's fine
    print('resetImport button already exists')
    
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','wb') as f:
    f.write(html.encode('utf-8'))
print('index.html saved.')
