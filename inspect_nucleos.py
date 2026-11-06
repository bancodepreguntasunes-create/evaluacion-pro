
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    html = f.read().decode('utf-8', errors='replace')

start = html.find('id="view-nucleos"')
end = html.find('id="view-estudiantes"')
print(html[start:end])
