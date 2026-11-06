
import re

path = r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\data.js'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

if 'ciencias-policiales' not in text:
    new_pnf = '''  {
    id: "ciencias-policiales",
    nombre: "PNF en Ciencias Policiales",
    corto: "Ciencias Policiales",
    descripcion: "Formación técnica y operativa en Ciencias Policiales y seguridad ciudadana.",
    color: "#3b82f6"
  },
'''
    insert_pos = text.find('const PNF_LIST = [') + len('const PNF_LIST = [\n')
    text = text[:insert_pos] + new_pnf + text[insert_pos:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('data.js updated with Ciencias Policiales!')
else:
    print('Already present in data.js')
