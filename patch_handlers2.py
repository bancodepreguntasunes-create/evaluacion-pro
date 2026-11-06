
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    js = f.read().decode('latin-1')

# ── Patch drag-and-drop ──────────────────────────────────────────────────────
old_drop = "const file = e.dataTransfer.files[0]; if (file) procesarArchivo(file);"
new_drop = "Array.from(e.dataTransfer.files).forEach(f => procesarArchivo(f));"
if old_drop in js:
    js = js.replace(old_drop, new_drop, 1)
    print('drag-drop OK')
else:
    print('drag-drop not found, searching procesarArchivo...')
    idx = js.find('procesarArchivo')
    print(js[max(0,idx-50):idx+120])

# ── Patch handleFileSelect / file input handler ──────────────────────────────
# Look for handleFileSelect or similar
old_sel = "const file = this.files[0]; if (file) procesarArchivo(file);"
new_sel = "Array.from(this.files).forEach(f => procesarArchivo(f)); this.value='';"
if old_sel in js:
    js = js.replace(old_sel, new_sel, 1)
    print('file select OK')
else:
    idx2 = js.find('handleFileSel')
    if idx2 != -1:
        print('handleFileSelect context:', js[idx2:idx2+300])

# ── Patch procesarArchivo to route to cargarArchivo ─────────────────────────
# If procesarArchivo exists and calls cargarArchivo, make it call cargarArchivo
idx3 = js.find('function procesarArchivo')
if idx3 != -1:
    end3 = js.find('\n}', idx3) + 2
    fn_body = js[idx3:end3]
    print('procesarArchivo:', fn_body[:300])

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))
print('app.js saved.')
