
import re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    html = f.read().decode('utf-8', errors='replace')

views = re.findall(r'<section class="view[^"]*" id="([^"]+)">', html)
print('Views found in index.html:', views)

# Check select IDs in each view
selects = re.findall(r'<select[^>]*id="([^"]+)"', html)
print('Select IDs:', selects)

# Check input IDs
inputs = re.findall(r'<input[^>]*id="([^"]+)"', html)
print('Input IDs:', inputs)
