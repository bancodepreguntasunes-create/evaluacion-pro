
path = r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

old_cond = "if (parsed.estudiantes && parsed.estudiantes.length > 0) {"
new_cond = "if (parsed.estudiantes && parsed.estudiantes.length >= INITIAL_ESTUDIANTES.length) {"

if old_cond in text:
    text = text.replace(old_cond, new_cond, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated cargarDB condition!')
