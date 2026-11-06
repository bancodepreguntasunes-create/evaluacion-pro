
# Let's inspect app.js line by line to see what happens when it runs
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's check if there are any undefined functions or errors
print('Size of app.js:', len(code))
print('First 10 lines of app.js:')
for l in code.split('\n')[:10]:
    print(' ', l[:100])
