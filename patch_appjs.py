
# -*- coding: utf-8 -*-
# Read with latin-1 to avoid decode errors, then work in that encoding
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    raw = f.read()

js = raw.decode('latin-1')

# ── 1. normalizarEstatus: add numeric score logic ────────────────────────────
idx_est = js.find('function normalizarEstatus(val)')
if idx_est != -1:
    end_est = js.find('\n}', idx_est) + 2
    new_estatus = """function normalizarEstatus(val) {
  if (val === null || val === undefined) return '';
  const str = String(val).trim();
  const num = parseFloat(str.replace(',', '.'));
  if (!isNaN(num) && str !== '') {
    return num >= 60 ? 'Aprobado' : 'Reprobado';
  }
  const v = str.toUpperCase();
  if (['APROBADO','APROBADA','AP','A','1','SI','APRO'].some(x=>v.includes(x))) return 'Aprobado';
  if (['REPROBADO','REPROBADA','REP','R','0','NO'].some(x=>v.includes(x))) return 'Reprobado';
  return '';
}

function resolverEstatus(estatusRaw, puntajeRaw) {
  if (puntajeRaw !== undefined && puntajeRaw !== null && String(puntajeRaw).trim() !== '') {
    const num = parseFloat(String(puntajeRaw).replace(',', '.'));
    if (!isNaN(num)) return num >= 60 ? 'Aprobado' : 'Reprobado';
  }
  return normalizarEstatus(String(estatusRaw || ''));
}"""
    js = js[:idx_est] + new_estatus + js[end_est:]
    print('normalizarEstatus patched OK')
else:
    print('ERROR: normalizarEstatus not found')

# ── 2. ejecutarImportacion: use resolverEstatus ──────────────────────────────
old_line = "    const estatus  = normalizarEstatus(String(row[mapeo.estatus] ||'').trim());"
new_line = """    const puntajeRaw = mapeo.puntaje ? row[mapeo.puntaje] : undefined;
    const estatus  = resolverEstatus(row[mapeo.estatus], puntajeRaw);
    const puntaje  = (() => {
      if (puntajeRaw !== undefined && puntajeRaw !== null && String(puntajeRaw).trim() !== '') {
        const n = parseFloat(String(puntajeRaw).replace(',','.'));
        return isNaN(n) ? undefined : n;
      }
      const n2 = parseFloat(String(row[mapeo.estatus]||'').replace(',','.'));
      return isNaN(n2) ? undefined : n2;
    })();"""

if old_line in js:
    js = js.replace(old_line, new_line, 1)
    print('import estatus line patched OK')
else:
    print('WARNING: import estatus line not found exactly')

# ── 3. Add puntaje to importados.push ───────────────────────────────────────
old_push = "      estatus: estatus||String(row[mapeo.estatus]||'').trim()\n    });"
new_push = "      estatus: estatus||String(row[mapeo.estatus]||'').trim(),\n      puntaje: puntaje\n    });"
if old_push in js:
    js = js.replace(old_push, new_push, 1)
    print('push puntaje OK')
else:
    print('WARNING: push not found')

# ── 4. CAMPOS_SISTEMA: add puntaje optional field ───────────────────────────
old_campos = "  { key:'estatus',  label:'Estado (Aprobado/Reprobado)', req:true  },"
new_campos = "  { key:'estatus',  label:'Estado / Puntaje (si es num\u00e9rico: >=60=Aprobado)', req:true  },\n  { key:'puntaje',  label:'Puntaje (Opcional, columna separada)',   req:false },"
if old_campos in js:
    js = js.replace(old_campos, new_campos, 1)
    print('CAMPOS_SISTEMA OK')
else:
    idx = js.find("key:'estatus'")
    print(f'estatus campo not found exactly, at {idx}')

# ── 5. archivosImportados variable ──────────────────────────────────────────
old_vars = "let excelRows=[], excelHeaders=[];"
new_vars = "let excelRows=[], excelHeaders=[], archivosImportados=[];"
if old_vars in js:
    js = js.replace(old_vars, new_vars, 1)
    print('archivosImportados var OK')
else:
    print('WARNING: excelRows var not found')

# ── 6. resetImport: also clear archivosImportados ───────────────────────────
old_reset = "  excelRows=[]; excelHeaders=[];"
new_reset = "  excelRows=[]; excelHeaders=[]; archivosImportados=[];"
if old_reset in js:
    js = js.replace(old_reset, new_reset, 1)
    print('resetImport OK')
else:
    print('WARNING: resetImport body not found')

# ── 7. FileReader: accumulate rows from multiple files ───────────────────────
old_reader = """      const json = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], {defval:''});
      if (!json.length) { toast('El archivo est\u00e1 vac\u00edo.','error'); return; }
      excelRows    = json;
      excelHeaders = Object.keys(json[0]);
      mostrarMapeo(file.name, json.length);"""

new_reader = """      const json = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], {defval:''});
      if (!json.length) { toast('El archivo "'+file.name+'" est\u00e1 vac\u00edo.','error'); return; }
      if (!excelRows.length) { excelHeaders = Object.keys(json[0]); }
      excelRows = [...excelRows, ...json];
      archivosImportados.push({ nombre: file.name, filas: json.length });
      mostrarMapeo(archivosImportados.map(a=>a.nombre).join(' + '), excelRows.length);
      toast('"'+file.name+'" cargado ('+json.length+' filas). Total: '+excelRows.length+'.','success');"""

if old_reader in js:
    js = js.replace(old_reader, new_reader, 1)
    print('FileReader multi-file OK')
else:
    # Try latin-1 encoded version
    print('WARNING: FileReader block not matched - searching...')
    idx = js.find('excelRows    = json;')
    if idx == -1: idx = js.find('excelRows = json;')
    print(f'  excelRows=json at {idx}')
    if idx != -1:
        snippet = js[max(0,idx-200):idx+300]
        print(repr(snippet))

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))

print('\nDone. app.js saved.')
