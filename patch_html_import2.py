
# -*- coding: utf-8 -*-
# Patch by byte position - add multiple to file input and update labels
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','rb') as f:
    html = f.read()

# 1. Add multiple to file input
old_input = b'id="fileInput" accept=".xlsx,.xls,.csv"'
new_input = b'id="fileInput" accept=".xlsx,.xls,.csv" multiple'
if old_input in html:
    html = html.replace(old_input, new_input, 1)
    print('file input multiple OK')
else:
    idx = html.find(b'fileInput')
    print(f'fileInput context:', html[max(0,idx-5):idx+120])

# 2. Update dropzone text
old_lbl = 'Arrastra tu archivo Excel aqu\u00ed'.encode('utf-8')
new_lbl = 'Arrastra uno o m\u00e1s archivos Excel aqu\u00ed'.encode('utf-8')
if old_lbl in html:
    html = html.replace(old_lbl, new_lbl, 1)
    print('dropzone label OK')
else:
    # Try latin-1
    old_lbl2 = b'Arrastra tu archivo Excel aqu\xed'
    new_lbl2 = b'Arrastra uno o m\xe1s archivos Excel aqu\xed'
    if old_lbl2 in html:
        html = html.replace(old_lbl2, new_lbl2, 1)
        print('dropzone label OK (latin-1)')
    else:
        print('WARNING: drop label not found')

# 3. Update "o haz clic" subtext
old_sub = b'o haz clic para seleccionar'
new_sub = b'o haz clic para seleccionar (m\xfaltiples archivos)'
if old_sub in html:
    html = html.replace(old_sub, new_sub, 1)
    print('subtext OK')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','wb') as f:
    f.write(html)
print('index.html saved.')
