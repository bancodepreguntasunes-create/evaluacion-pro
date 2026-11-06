
import re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    text = f.read().decode('utf-8', errors='replace')

pattern = r'<div class="import-config"\s+<div id="archivos-cargados-lista"[^>]*></div>\s+id="importConfig"\s+style="display:none">'
replacement = '<div id="archivos-cargados-lista" style="display:none;margin-bottom:12px;"></div>\r\n      <div class="import-config" id="importConfig" style="display:none">'

text, count = re.subn(pattern, replacement, text)
print(f'Replaced {count} instances')
if count > 0:
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Cleaned!')
