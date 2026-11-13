import re

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/map_paths.txt', 'r', encoding='utf-8') as f:
    c = f.read()

states = re.findall(r'data-estado="([^"]+)"', c)
print('States in map_paths.txt:', states)
print('Count of states:', len(states))
