
# 1. Update index.html
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<script src="app.js">', '<script src="app.js?v=4">')
html = html.replace('<script src="app.js?v=3">', '<script src="app.js?v=4">')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html cache buster v=4 OK')

# 2. Update app.js
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace cargarDB
start_c = js.find('function cargarDB() {')
end_c = js.find('\nfunction guardarDB()', start_c)
if start_c != -1 and end_c != -1:
    new_cargar = '''function cargarDB() {
  try {
    const saved = localStorage.getItem('unesDB');
    const parsed = saved ? JSON.parse(saved) : null;
    
    // Auto-healing: detectar y corregir si el navegador guardó el cálculo invertido
    let isBad = false;
    if (parsed && parsed.estudiantes) {
      const ap = parsed.estudiantes.filter(e => e.estatus === 'Aprobado').length;
      const rep = parsed.estudiantes.filter(e => e.estatus === 'Reprobado').length;
      // En los datos oficiales más del 90% son aprobados (true). Si rep > ap, es el error invertido
      if (rep > ap && parsed.estudiantes.length > 50) isBad = true;
      if (!parsed.version || parsed.version < 4) isBad = true;
    } else {
      isBad = true;
    }

    if (!isBad && parsed && parsed.estudiantes && parsed.estudiantes.length >= INITIAL_ESTUDIANTES.length) {
      DB = parsed;
    } else {
      console.log('Cargando dataset oficial corregido v4...');
      DB.estudiantes = INITIAL_ESTUDIANTES;
      DB.version = 4;
      guardarDB();
    }
  } catch (e) {
    console.warn('Error al cargar DB:', e);
    DB.estudiantes = INITIAL_ESTUDIANTES;
    DB.version = 4;
    guardarDB();
  }
}
'''
    js = js[:start_c] + new_cargar + js[end_c:]
    print('cargarDB replaced OK')
else:
    print('cargarDB start/end not found:', start_c, end_c)

# Replace ejecutarImportacion
start_i = js.find('function ejecutarImportacion() {')
end_i = js.find('\nfunction resetImport()', start_i)
if start_i != -1 and end_i != -1:
    new_imp = '''function ejecutarImportacion() {
  const mapeo = {};
  CAMPOS_SISTEMA.forEach(c => {
    const sel = document.getElementById('map_' + c.key);
    mapeo[c.key] = sel ? sel.value : '';
  });

  if (!mapeo.cedula) { toast('Debes seleccionar la columna de Cédula.', 'error'); return; }

  const importados = [];

  excelRows.forEach((row, idx) => {
    const cedula = String(row[mapeo.cedula] || '').trim();
    if (!cedula) return;

    // Nombre
    let nombre = mapeo.nombre ? String(row[mapeo.nombre] || '').trim() : '';
    if (!nombre || nombre === '') {
      const nom1 = String(row['1er Nombre'] || '').trim();
      const nom2 = String(row['2do Nombre'] || '').trim();
      const ap1  = String(row['1er Apellido'] || '').trim();
      const ap2  = String(row['2do Apellido'] || '').trim();
      if (nom1 || ap1) nombre = `${nom1} ${nom2} ${ap1} ${ap2}`.replace(/\\s+/g, ' ').trim();
    }
    if (!nombre) nombre = 'Estudiante ' + cedula;

    // Pts numérico
    let pts = null;
    let ptsSource = row['Pts'] !== undefined ? row['Pts'] : (mapeo.puntaje ? row[mapeo.puntaje] : null);
    if (ptsSource !== null && ptsSource !== undefined && String(ptsSource).trim() !== '') {
      const p = parseFloat(String(ptsSource).replace(',', '.'));
      if (!isNaN(p)) pts = p;
    }

    // ESTATUS: REGLA ESTRICTA OFICIAL
    // 1. Mirar columna 'Aprobado' o mapeo.estatus
    let rawAprobado = '';
    if (row['Aprobado'] !== undefined && row['Aprobado'] !== null) {
      rawAprobado = String(row['Aprobado']).trim().toLowerCase();
    } else if (mapeo.estatus && row[mapeo.estatus] !== undefined) {
      rawAprobado = String(row[mapeo.estatus]).trim().toLowerCase();
    }

    let estatus = 'Aprobado';
    // EXACT MATCH: true = Aprobado, false = Reprobado
    if (rawAprobado === 'true' || rawAprobado === '1' || rawAprobado === 'si' || rawAprobado === 'sí' || rawAprobado === 'aprobado' || rawAprobado === 'aprobada') {
      estatus = 'Aprobado';
    } else if (rawAprobado === 'false' || rawAprobado === '0' || rawAprobado === 'no' || rawAprobado === 'reprobado' || rawAprobado === 'reprobada') {
      estatus = 'Reprobado';
    } else if (pts !== null) {
      estatus = pts >= 60 ? 'Aprobado' : 'Reprobado';
    } else {
      estatus = 'Aprobado';
    }

    // Núcleo y PNF
    let evalStr = mapeo.nucleo ? String(row[mapeo.nucleo] || '').trim() : (row['Nombre de la Evaluación'] || '');
    let carrera = mapeo.pnf ? String(row[mapeo.pnf] || '').trim() : (row['Carrera'] || '');
    let trayecto = mapeo.trayecto ? String(row[mapeo.trayecto] || '').trim() : '';
    let token = mapeo.token ? String(row[mapeo.token] || '').trim() : (row['Token'] || '');

    // Si la carrera viene en blanco o la evaluación indica CP -> Ciencias Policiales
    let pnf = carrera;
    if (!pnf || pnf.trim() === '' || /\\bCP\\b/i.test(evalStr)) {
      pnf = 'Ciencias Policiales';
    }

    // Detección de trayecto desde evaluación si está vacío
    if (!trayecto || trayecto.trim() === '') {
      if (/\\bT1\\b/i.test(evalStr)) trayecto = 'I';
      else if (/\\bT2\\b/i.test(evalStr)) trayecto = 'II';
      else if (/\\bT3\\b/i.test(evalStr)) trayecto = 'III';
      else if (/\\bT4\\b/i.test(evalStr)) trayecto = 'IV';
      else if (/\\bTI\\b/i.test(evalStr)) trayecto = 'Inicial';
      else trayecto = 'I';
    }

    // Limpieza de nombre de núcleo
    let nucleo = evalStr
      .replace(/\\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN)\\b/gi, '')
      .replace(/\\s+/g, ' ')
      .trim();
    if (!nucleo) nucleo = 'Caracas';

    importados.push({
      id: String(DB.nextId++),
      cedula,
      nombre,
      nucleo,
      pnf,
      trayecto,
      token,
      estatus,
      puntaje: pts
    });
  });

  if (!importados.length) {
    toast('No se pudieron extraer registros válidos.', 'error');
    return;
  }

  DB.estudiantes = [...importados, ...DB.estudiantes];
  DB.version = 4;
  guardarDB();
  resetImport();
  poblarSelects();

  const apCount = importados.filter(e => e.estatus === 'Aprobado').length;
  const repCount = importados.filter(e => e.estatus === 'Reprobado').length;
  toast(`✅ ${importados.length} estudiantes importados: ${apCount} Aprobados (true) y ${repCount} Reprobados (false).`, 'success');
  showView('dashboard');
}
'''
    js = js[:start_i] + new_imp + js[end_i:]
    print('ejecutarImportacion replaced OK')
else:
    print('ejecutarImportacion start/end not found:', start_i, end_i)

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('app.js saved successfully!')
