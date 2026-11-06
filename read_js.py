
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f: d=f.read().decode('utf-8','replace')

idx = d.find('ejecutarImportacion')
print(d[idx:idx+2500])
print('\n\n===IMPORT FILE SECTION===')
idx2 = d.find('cargarArchivo')
if idx2 == -1: idx2 = d.find('FileReader')
print(d[max(0,idx2-50):idx2+600])
print('\n\n===ESTATUS PARSE===')
idx3 = d.find('Aprobado')
while idx3 != -1:
    snippet = d[max(0,idx3-100):idx3+120]
    if 'return' in snippet or 'parseE' in snippet.lower() or '>=' in snippet or '60' in snippet:
        print(f'[pos {idx3}]', snippet[:200])
        print()
    idx3 = d.find('Aprobado', idx3+1)
