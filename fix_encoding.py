
# -*- coding: utf-8 -*-
# Save with utf-8 since we now have emoji characters
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f:
    js = f.read().decode('latin-1')

# Replace emoji chars with ASCII equivalents in the new code we inserted
js = js.replace('\u2705', '[OK]')   # checkmark emoji -> [OK]
js = js.replace('\u00d7', 'X')      # multiplication sign

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','wb') as f:
    f.write(js.encode('latin-1'))
print('Emoji replaced, app.js saved.')
