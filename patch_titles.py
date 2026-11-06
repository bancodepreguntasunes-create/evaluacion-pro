
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f: d=f.read()
old = b"    importar:   'Importar desde Excel'"
new_val = b"    importar:   'Importar desde Excel',\n    instructivo: 'Instructivo del Sistema EPA'"
if old in d:
    d = d.replace(old, new_val, 1)
    print('titles map updated')
else:
    print('NOT FOUND, trying alternate...')
    print(repr(d[d.find(b'importar'):d.find(b'importar')+60]))
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f: f.write(d)
print('saved')
