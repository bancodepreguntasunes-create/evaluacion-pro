import csv
import json
import re

# 1. Leer datos existentes
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

existentes_map = {e['cedula']: e for e in existing['estudiantes']}
next_id = int(existing.get('nextId', len(existing['estudiantes']) + 1))

def clean_nucleo(eval_str):
    if not eval_str: return 'Caracas'
    s = eval_str
    s = re.sub(r'\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN|TOKEN)\b', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else 'Caracas'

def detect_trayecto(eval_str):
    if not eval_str: return 'I'
    if re.search(r'\bTI\b', eval_str, re.I): return 'Inicial'
    if re.search(r'\bT2\b', eval_str, re.I): return 'II'
    if re.search(r'\bT3\b', eval_str, re.I): return 'III'
    if re.search(r'\bT4\b', eval_str, re.I): return 'IV'
    if re.search(r'\bT1\b', eval_str, re.I): return 'I'
    return 'I'

nuevos_agregados = 0
actualizados = 0

# 2. Procesar CSV de datos diarios
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/nuevos_datos_20261106.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        cedula = (r.get('Cédula') or r.get('Cedula') or '').strip()
        if not cedula: continue
        
        n1 = (r.get('1er Nombre') or '').strip()
        n2 = (r.get('2do Nombre') or '').strip()
        a1 = (r.get('1er Apellido') or '').strip()
        a2 = (r.get('2do Apellido') or '').strip()
        nombre = f'{n1} {n2} {a1} {a2}'.strip()
        nombre = re.sub(r'\s+', ' ', nombre).title()

        ev = (r.get('Nombre de la Evaluación') or r.get('Nombre de la Evaluacion') or '').strip()
        carrera = (r.get('Carrera') or '').strip()
        tok = (r.get('Token') or '').strip()

        if not carrera or carrera == 'None' or carrera == '' or re.search(r'\bCP\b', ev, re.I):
            pnf = 'Ciencias Policiales'
        else:
            pnf = carrera
            if 'policial' in pnf.lower(): pnf = 'Servicio Policial'
            elif 'penitenciario' in pnf.lower(): pnf = 'Servicio Penitenciario'
            elif 'fuego' in pnf.lower() or 'bomber' in pnf.lower(): pnf = 'Ciencias del Fuego'
            elif 'civil' in pnf.lower(): pnf = 'Protección Civil'
            elif 'pre-hospitalaria' in pnf.lower() or 'prehospitalaria' in pnf.lower(): pnf = 'Emergencias Prehospitalarias'
            elif 'investigación penal y' in pnf.lower() or 'investigacion penal y' in pnf.lower(): pnf = 'Investigación Penal y Criminalística'
            elif 'investigación penal' in pnf.lower() or 'investigacion penal' in pnf.lower(): pnf = 'Investigación Penal'
            elif 'criminal' in pnf.lower(): pnf = 'Criminalística'

        nucleo = clean_nucleo(ev)
        trayecto = detect_trayecto(ev)

        pts_raw = r.get('Pts')
        pts = None
        try:
            if pts_raw is not None and str(pts_raw).strip() != '':
                pts = float(str(pts_raw).replace(',', '.'))
        except:
            pass

        raw_ap = str(r.get('Aprobado') or '').strip().lower()
        if raw_ap == 'true' or raw_ap == '1' or raw_ap == 'si' or raw_ap == 'sí' or raw_ap == 'aprobado':
            estatus = 'Aprobado'
        elif raw_ap == 'false' or raw_ap == '0' or raw_ap == 'no' or raw_ap == 'reprobado':
            estatus = 'Reprobado'
        elif pts is not None:
            estatus = 'Aprobado' if pts >= 60 else 'Reprobado'
        else:
            estatus = 'Aprobado'

        item = {
            'cedula': cedula,
            'nombre': nombre,
            'nucleo': nucleo,
            'pnf': pnf,
            'trayecto': trayecto,
            'token': tok,
            'evaluacion': ev,
            'estatus': estatus,
            'puntaje': pts
        }

        if cedula in existentes_map:
            item['id'] = existentes_map[cedula]['id']
            existentes_map[cedula] = item
            actualizados += 1
        else:
            item['id'] = str(next_id)
            next_id += 1
            existentes_map[cedula] = item
            nuevos_agregados += 1

todos = list(existentes_map.values())
# Re-index ids from 1 to N for cleanliness
for i, s in enumerate(todos, start=1):
    s['id'] = str(i)

# Guardar en datos_importados.json
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json', 'w', encoding='utf-8') as f:
    json.dump({'estudiantes': todos, 'nextId': len(todos) + 1}, f, ensure_ascii=False, indent=2)

print(f"datos_importados.json actualizado: {len(todos)} registros ({nuevos_agregados} nuevos agregados, {actualizados} actualizados).")

# 3. Actualizar unes_sistema_final.js y app.js
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_sistema_final.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Actualizar INITIAL_ESTUDIANTES
start_idx = code.find('const INITIAL_ESTUDIANTES =')
end_idx = code.find('const CAMPOS_SISTEMA =')
new_init = 'const INITIAL_ESTUDIANTES = ' + json.dumps(todos, ensure_ascii=False) + ';\n\n// CAMPOS RECONOCIDOS\n'
code = code[:start_idx] + new_init + code[end_idx:]

# Actualizar versión de DB a 6 para forzar auto-update en navegador
code = code.replace("version < 5", "version < 6")
code = code.replace("DB.version = 5", "DB.version = 6")
code = code.replace("dataset oficial UNES v5", "dataset oficial UNES v6 (2.443 registros)")
code = code.replace("2.092 estudiantes: 2.014 Aprobados y 78 Reprobados", f"{len(todos):,} estudiantes")

# Mejorar ejecutarImportacion para soportar "modoCarga" (Acumulativo vs Reemplazar)
old_replace_code = "DB.estudiantes = importados;\n  DB.version = 6;\n  guardarDB();"
new_replace_code = """// Modo de carga diario / acumulativo o reemplazo total
  const modoAcumular = document.getElementById('modoCargaAcumular') ? document.getElementById('modoCargaAcumular').checked : true;
  if (modoAcumular) {
    const mapa = new Map();
    DB.estudiantes.forEach(e => mapa.set(e.cedula, e));
    importados.forEach(e => {
      if (mapa.has(e.cedula)) e.id = mapa.get(e.cedula).id;
      mapa.set(e.cedula, e);
    });
    DB.estudiantes = Array.from(mapa.values());
  } else {
    DB.estudiantes = importados;
  }
  DB.version = 6;
  guardarDB();"""

if old_replace_code in code:
    code = code.replace(old_replace_code, new_replace_code)
else:
    # Buscar el punto de reemplazo
    idx_imp = code.find("DB.estudiantes = importados;")
    if idx_imp != -1:
        idx_imp_end = code.find("guardarDB();", idx_imp) + len("guardarDB();")
        code = code[:idx_imp] + new_replace_code + code[idx_imp_end:]

# Guardar archivos JS
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_sistema_final.js', 'w', encoding='utf-8') as f:
    f.write(code)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("unes_sistema_final.js y app.js actualizados con los 2.443 estudiantes y modo diario.")

# 4. Actualizar index.html con el selector de modo de carga
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Actualizar versión en auto-purge
html = html.replace("_db.version < 5", "_db.version < 6")

# Inyectar selector de Modo de Carga en view-importar si no existe
if 'modoCargaAcumular' not in html:
    selector_html = """
        <!-- Opciones de Carga Diaria / Acumulativa -->
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin-bottom:20px;">
          <h4 style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;color:#6366f1"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            Modo de Carga de Archivos:
          </h4>
          <div style="display:flex;gap:20px;font-size:13px;color:#334155;">
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="radio" name="modoCarga" id="modoCargaAcumular" value="acumular" checked style="accent-color:#6366f1;">
              <strong>Carga Diaria / Acumulativa (Recomendado)</strong> <span style="color:#64748b;">— Agrega los nuevos registros y actualiza los existentes sin borrar los días anteriores.</span>
            </label>
          </div>
          <div style="margin-top:8px;font-size:13px;color:#334155;">
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="radio" name="modoCarga" id="modoCargaReemplazar" value="reemplazar" style="accent-color:#6366f1;">
              <span>Reemplazar todo</span> <span style="color:#64748b;">— Limpia la base de datos y deja solo este archivo.</span>
            </label>
          </div>
        </div>

        <div class="col-mapper" id="colMapper"></div>"""
    html = html.replace('<div class="col-mapper" id="colMapper"></div>', selector_html)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html actualizado con el selector de carga diaria!")
