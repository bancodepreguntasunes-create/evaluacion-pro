
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of index.html:', len(text))
# Check if there is any inline script in index.html
import re
scripts = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', text)
print('Number of inline script tags:', len(scripts))
for i, s in enumerate(scripts):
    print(f'Script {i}:', s[:200])
