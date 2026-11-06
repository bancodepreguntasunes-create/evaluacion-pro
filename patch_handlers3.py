
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    js = f.read().decode('latin-1')

# ── 1. handleFileSelect: loop through all files ──────────────────────────────
old_sel = "handleFileSelect(e) { const file=e.target.files[0]; if(file) procesarArchivo(file); }"
new_sel = "handleFileSelect(e) { Array.from(e.target.files).forEach(f=>procesarArchivo(f)); e.target.value=''; }"
if old_sel in js:
    js = js.replace(old_sel, new_sel, 1)
    print('handleFileSelect OK')
else:
    print('handleFileSelect not found exactly')

# ── 2. procesarArchivo: THIS is the actual file reader function.
#    It currently has inline XLSX reading. We need it to accumulate rows.
#    Find the reader.onload block and patch it.
old_proc = """  reader.onload = ev => {
    try {
      const workbook = XLSX.read(new Uint8Array(ev.target.result), {type:'array'});
      const json = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], {defval:''});
      if (!json.length) { toast('El archivo est\xe1 vac\xedo.','error'); return; }
      if (!excelRows.length) { excelHeaders = Object.keys(json[0]); }
      excelRows = [...excelRows, ...json];
      archivosImportados.push({ nombre: file.name, filas: json.length });
      mostrarMapeo(archivosImportados.map(a=>a.nombre).join(' + '), excelRows.length);
      toast('"'+file.name+'" cargado ('+json.length+' filas). Total: '+excelRows.length+'.','success');
    } catch(err) { toast('Error al leer: '+err.message,'error'); }
  };"""

# This was already patched in patch_appjs2. Let's verify it's there
if 'archivosImportados.push' in js:
    print('archivosImportados accumulation already in place OK')
else:
    print('WARNING: archivosImportados not found in procesarArchivo')
    # Patch by finding and replacing the original onload
    idx = js.find('excelRows    = json;')
    if idx == -1: idx = js.find('excelRows = [...excelRows')
    print(f'excelRows line at {idx}:', js[max(0,idx-10):idx+120] if idx != -1 else 'NOT FOUND')

# ── 3. Also show loaded files list in UI via mostrarMapeo ───────────────────
# Find mostrarMapeo and add file list display
idx_mm = js.find('function mostrarMapeo(')
if idx_mm != -1:
    end_mm = js.find('\n}', idx_mm) + 2
    old_mm = js[idx_mm:end_mm]
    if 'archivos-cargados-lista' not in old_mm:
        # Insert file list UI at start of function body
        body_start = js.find('{', idx_mm) + 1
        insert = """
  // Show list of loaded files
  const listaEl = document.getElementById('archivos-cargados-lista');
  if (listaEl && archivosImportados.length) {
    listaEl.style.display = '';
    listaEl.innerHTML = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;">' +
      archivosImportados.map(a =>
        '<span style="background:rgba(16,185,129,0.12);color:#065f46;border:1px solid #6ee7b7;border-radius:20px;padding:3px 10px;font-size:12px;font-weight:600;">'+
        '\u2705 '+a.nombre+' ('+a.filas+' filas)</span>'
      ).join('') +
      '<button onclick="resetImport()" style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;border-radius:20px;padding:3px 10px;font-size:12px;cursor:pointer;">\u00d7 Limpiar todo</button>' +
      '</div>';
  }"""
        js = js[:body_start] + insert + js[body_start:]
        print('mostrarMapeo file list UI OK')
    else:
        print('File list UI already in mostrarMapeo')
else:
    print('mostrarMapeo not found')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))
print('app.js saved.')
