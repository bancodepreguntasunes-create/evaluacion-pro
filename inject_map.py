import re

# Read the generated paths
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\map_paths.txt', 'r', encoding='utf-8') as f:
    map_paths = f.read()

# Read index.html
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the SVG content inside #venezuelaMap
# Find the SVG block
svg_start = html.find('<svg id="venezuelaMap"')
svg_end = html.find('</svg>', svg_start) + 6

if svg_start == -1:
    print("ERROR: Could not find venezuelaMap SVG")
else:
    new_svg = f'''<svg id="venezuelaMap" viewBox="0 0 600 527" xmlns="http://www.w3.org/2000/svg">
              {map_paths}
            </svg>'''
    
    html = html[:svg_start] + new_svg + html[svg_end:]
    
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated successfully!")
    print(f"SVG section replaced: chars {svg_start} to {svg_end}")
