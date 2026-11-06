with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_core_v5.js', 'r', encoding='utf-8') as f:
    c = f.read()

print('Length of unes_core_v5.js:', len(c))
idx = c.find('function renderDashboard')
print('Found renderDashboard at:', idx)
idx2 = c.find('function ejecutarImportacion')
print('Found ejecutarImportacion at:', idx2)
idx3 = c.find('function restablecerDatos')
print('Found restablecerDatos at:', idx3)
