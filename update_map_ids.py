import re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'rb') as f:
    content = f.read().decode('latin-1')

# Replace estadoToSvgId function
old_func_start = content.find('function estadoToSvgId(estado) {')
old_func_end = content.find('\n}', old_func_start) + 2

new_func = """function estadoToSvgId(estado) {
  const map = {
    'LA GUAIRA':     'map-VE-X',
    'CARACAS':       'map-VE-A',
    'MIRANDA':       'map-VE-M',
    'ARAGUA':        'map-VE-D',
    'CARABOBO':      'map-VE-G',
    'YARACUY':       'map-VE-U',
    'FALCÓN':        'map-VE-I',
    'LARA':          'map-VE-K',
    'ZULIA':         'map-VE-V',
    'APURE':         'map-VE-C',
    'BARINAS':       'map-VE-E',
    'COJEDES':       'map-VE-H',
    'GUÁRICO':       'map-VE-J',
    'PORTUGUESA':    'map-VE-P',
    'MÉRIDA':        'map-VE-L',
    'TÁCHIRA':       'map-VE-S',
    'TRUJILLO':      'map-VE-T',
    'ANZOÁTEGUI':    'map-VE-B',
    'MONAGAS':       'map-VE-N',
    'NUEVA ESPARTA': 'map-VE-O',
    'SUCRE':         'map-VE-R',
    'AMAZONAS':      'map-VE-Z',
    'BOLÍVAR':       'map-VE-F',
    'DELTA AMACURO': 'map-VE-Y',
  };
  return map[estado] || '';
}"""

if old_func_start != -1:
    content = content[:old_func_start] + new_func + content[old_func_end:]
    print("estadoToSvgId updated successfully")
else:
    print("ERROR: function not found")

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'wb') as f:
    f.write(content.encode('latin-1'))

print("app.js saved")
