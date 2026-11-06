
import os

target = 'Tokens Registrados'
found = []

for root, dirs, files in os.walk(r'C:\Users\PC'):
    # skip system/hidden dirs
    if any(p in root for p in ['AppData', 'node_modules', '.git', 'Local', 'Roaming']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.php', '.txt')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    if target in fp.read():
                        found.append(p)
            except:
                pass

print('Found matches outside appdata:')
for p in found:
    print(' ', p)
