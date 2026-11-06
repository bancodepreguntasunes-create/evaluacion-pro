
import re, json

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    html = f.read().decode('utf-8', errors='replace')

onclicks = set(re.findall(r'onclick="([^"]+)"', html))
print('=== ONCLICKS ===')
for o in sorted(onclicks):
    print(' ', o)

onkeyups = set(re.findall(r'onkeyup="([^"]+)"', html))
print('\n=== ONKEYUPS ===')
for o in sorted(onkeyups):
    print(' ', o)

onchanges = set(re.findall(r'onchange="([^"]+)"', html))
print('\n=== ONCHANGES ===')
for o in sorted(onchanges):
    print(' ', o)

ids = set(re.findall(r'id="([^"]+)"', html))
print('\n=== KEY DOM IDs ===')
for i in sorted(ids):
    print(' ', i)
