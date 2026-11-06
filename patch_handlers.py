
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    js = f.read().decode('latin-1')

# Find and replace the fileInput change handler to loop through all selected files
old_handler = "document.getElementById('fileInput').addEventListener('change', ev => { cargarArchivo(ev.target.files[0]); });"
new_handler = """document.getElementById('fileInput').addEventListener('change', ev => {
  Array.from(ev.target.files).forEach(file => cargarArchivo(file));
  ev.target.value = ''; // allow re-selecting same file
});"""

if old_handler in js:
    js = js.replace(old_handler, new_handler, 1)
    print('fileInput change handler OK')
else:
    # Try searching
    idx = js.find("ev.target.files[0]")
    if idx != -1:
        line_start = js.rfind('\n', 0, idx) + 1
        line_end = js.find('\n', idx) + 1
        old_line = js[line_start:line_end]
        new_line = "  Array.from(ev.target.files).forEach(file => cargarArchivo(file));\n  ev.target.value = '';\n"
        # Replace just inside the listener
        handler_start = js.rfind("'change'", 0, idx)
        cb_start = js.find('{', handler_start) + 1
        cb_end = js.find('});', cb_start) 
        old_cb = js[cb_start:cb_end]
        new_cb = '\n  Array.from(ev.target.files).forEach(file => cargarArchivo(file));\n  ev.target.value = \'\';\n'
        js = js[:cb_start] + new_cb + js[cb_end:]
        print('fileInput handler patched via position OK')
    else:
        print('WARNING: fileInput handler not found')

# Also patch the drag-and-drop handler (ondrop) if it uses files[0]
old_drop = "cargarArchivo(ev.dataTransfer.files[0]);"
new_drop = "Array.from(ev.dataTransfer.files).forEach(file => cargarArchivo(file));"
if old_drop in js:
    js = js.replace(old_drop, new_drop, 1)
    print('drag-and-drop handler OK')
else:
    idx2 = js.find('dataTransfer.files')
    if idx2 != -1:
        print('dataTransfer.files context:', js[max(0,idx2-20):idx2+80])

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))
print('app.js saved.')
