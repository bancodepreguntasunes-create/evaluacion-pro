
path = r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the status detection block in ejecutarImportacion
old_code = """    let estatus = 'Aprobado';
    if (pts !== null) {
      estatus = pts >= 60 ? 'Aprobado' : 'Reprobado';
    } else {
      const valStr = String(row[mapeo.estatus] || '').toLowerCase().trim();
      if (['reprobado', 'reprobada', 'false', '0', 'no', 'r'].includes(valStr)) estatus = 'Reprobado';
      else estatus = 'Aprobado';
    }"""

new_code = """    // Criterio exacto: true = Aprobado, false = Reprobado (o >= 60 pts)
    let estatus = 'Aprobado';
    const rawVal = String(row[mapeo.estatus] || '').toLowerCase().trim();
    if (rawVal === 'true' || rawVal === 'si' || rawVal === 'aprobado' || rawVal === 'aprobada') {
      estatus = 'Aprobado';
    } else if (rawVal === 'false' || rawVal === 'no' || rawVal === 'reprobado' || rawVal === 'reprobada') {
      estatus = 'Reprobado';
    } else if (pts !== null) {
      estatus = pts >= 60 ? 'Aprobado' : 'Reprobado';
    } else {
      estatus = 'Aprobado';
    }"""

if old_code in text:
    text = text.replace(old_code, new_code, 1)
    print('Status parsing logic updated!')
else:
    print('Pattern not found!')

# Prioritize 'aprobado' column in autodetection
old_syn = "estatus:  ['pts', 'puntos', 'puntaje', 'calificacion', 'nota', 'aprobado', 'estatus', 'estado', 'resultado'],"
new_syn = "estatus:  ['aprobado', 'estatus', 'estado', 'resultado', 'pts', 'puntos', 'puntaje', 'calificacion', 'nota'],"
if old_syn in text:
    text = text.replace(old_syn, new_syn, 1)
    print('Autodetection priority updated!')

# Always force-update localStorage on page load so user sees new calculation
old_load = """    const saved = localStorage.getItem('unesDB');
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed.estudiantes && parsed.estudiantes.length > 0) {
        DB = parsed;
      } else {
        DB.estudiantes = INITIAL_ESTUDIANTES;
        guardarDB();
      }
    } else {
      DB.estudiantes = INITIAL_ESTUDIANTES;
      guardarDB();
    }"""

new_load = """    // Carga los datos oficiales iniciales sincronizados
    const saved = localStorage.getItem('unesDB');
    const parsed = saved ? JSON.parse(saved) : null;
    if (parsed && parsed.version === 3 && parsed.estudiantes && parsed.estudiantes.length >= INITIAL_ESTUDIANTES.length) {
      DB = parsed;
    } else {
      DB.estudiantes = INITIAL_ESTUDIANTES;
      DB.version = 3;
      guardarDB();
    }"""

if old_load in text:
    text = text.replace(old_load, new_load, 1)
    print('cargarDB updated to force version 3 refresh!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('app.js saved!')
