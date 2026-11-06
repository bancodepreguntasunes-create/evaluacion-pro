import re

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_sistema_final.js', 'w', encoding='utf-8') as f:
    f.write(c)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

h = re.sub(r'<script\s+src=["\'](app|unes_core_v5)\.js.*?["\']\s*></script>', '<script src="unes_sistema_final.js"></script>', h)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("unes_sistema_final.js created and index.html linked successfully!")
