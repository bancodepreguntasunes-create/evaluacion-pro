import json
import re
import unicodedata

def normalizar_nucleo(raw_val):
    if not raw_val:
        return 'CARACAS'
    s = str(raw_val).strip()
    s = re.sub(r'\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN|TOKEN)\b', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip()
    clean = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper().strip()
    
    if 'ANZOATEGUI' in clean: return 'ANZOÁTEGUI'
    if 'POLICARACAS' in clean: return 'POLICARACAS'
    if 'CARACAS' in clean: return 'CARACAS'
    if 'PORTUGUESA' in clean: return 'PORTUGUESA'
    if 'BARINAS' in clean: return 'BARINAS'
    if 'TRUJILLO' in clean: return 'TRUJILLO'
    if 'CARABOBO' in clean: return 'CARABOBO'
    if 'BARLOVENTO' in clean: return 'BARLOVENTO'
    if 'VALLES DEL TUY' in clean or 'VALLE DEL TUY' in clean: return 'VALLES DEL TUY'
    if 'BOLIVAR' in clean or 'ANGOSTURA' in clean: return 'BOLÍVAR - ANGOSTURA'
    if 'LLANITO' in clean: return 'EL LLANITO'
    if 'JUNQUITO' in clean: return 'EL JUNQUITO'
    if 'GUAIRA' in clean: return 'LA GUAIRA'
    if 'MONAGAS' in clean: return 'MONAGAS'
    if 'GUARENAS' in clean or 'GUATIRE' in clean: return 'GUARENAS - GUATIRE'
    if 'NUEVA ESPARTA' in clean or 'MARGARITA' in clean: return 'NUEVA ESPARTA'
    if 'FALCON' in clean: return 'FALCÓN'
    if 'YARACUY' in clean: return 'YARACUY'
    if 'ALTOS MIRANDINOS' in clean or 'ALTO MIRANDINO' in clean: return 'ALTOS MIRANDINOS'
    if 'METROPOLITANO' in clean: return 'EJE METROPOLITANO'
    if 'SAN PEDRO' in clean: return 'SAN PEDRO'
    if 'POLISUCRE' in clean: return 'POLISUCRE'
    if 'LARA' in clean: return 'LARA'
    if 'ARAGUA' in clean: return 'ARAGUA'
    if 'ZULIA' in clean: return 'ZULIA'
    if 'MERIDA' in clean: return 'MÉRIDA'
    if 'TACHIRA' in clean: return 'TÁCHIRA'
    if 'APURE' in clean: return 'APURE'
    if 'COJEDES' in clean: return 'COJEDES'
    if 'GUARICO' in clean: return 'GUÁRICO'
    if 'SUCRE' in clean: return 'SUCRE'
    if 'AMAZONAS' in clean: return 'AMAZONAS'
    if 'DELTA' in clean: return 'DELTA AMACURO'
    return s.upper()

# 1. Actualizar datos_importados.json
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for e in data['estudiantes']:
    e['nucleo'] = normalizar_nucleo(e.get('nucleo', '') or e.get('evaluacion', ''))

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"datos_importados.json actualizado con núcleos unificados para {len(data['estudiantes'])} estudiantes.")

# 2. Actualizar data.js con codificación limpia y sin caracteres rotos
nuevo_data_js = '''// =============================================
// UNES - data.js  –  Datos maestros del sistema
// =============================================

const NUCLEOS = [
  "ALTOS MIRANDINOS",
  "AMAZONAS",
  "ANZOÁTEGUI",
  "APURE",
  "ARAGUA",
  "BARINAS",
  "BARLOVENTO",
  "BOLÍVAR - ANGOSTURA",
  "BOLÍVAR - PTO. ORDAZ",
  "CARABOBO",
  "CARACAS",
  "COJEDES",
  "DELTA AMACURO",
  "EJE GUARENAS - GUATIRE",
  "EJE METROPOLITANO",
  "EJE VALLES DEL TUY",
  "EL JUNQUITO",
  "EL LLANITO",
  "FALCÓN",
  "GUÁRICO",
  "LA GUAIRA",
  "LARA",
  "MÉRIDA",
  "MONAGAS",
  "NUEVA ESPARTA",
  "POLICARACAS",
  "POLISUCRE",
  "PORTUGUESA",
  "SAN PEDRO",
  "SUCRE",
  "TÁCHIRA",
  "TRUJILLO",
  "YARACUY",
  "ZULIA"
];

const PNF_LIST = [
  {
    id: "ciencias-policiales",
    nombre: "PNF en Ciencias Policiales",
    corto: "Ciencias Policiales",
    descripcion: "Formación técnica y operativa en Ciencias Policiales y seguridad ciudadana.",
    color: "#3b82f6"
  },
  {
    id: "servicio-policial",
    nombre: "PNF en Servicio Policial",
    corto: "Serv. Policial",
    descripcion: "Formación integral de funcionarios para el CPNB, policías estadales y municipales.",
    color: "#6366f1"
  },
  {
    id: "investigacion-penal",
    nombre: "PNF en Investigación Penal",
    corto: "Inv. Penal",
    descripcion: "Formación técnico-científica para la investigación de hechos delictivos y apoyo al CICPC.",
    color: "#8b5cf6"
  },
  {
    id: "criminalistica",
    nombre: "PNF en Criminalística",
    corto: "Criminalística",
    descripcion: "Capacitación en análisis de evidencias físicas, ciencias forenses y técnicas auxiliares de la justicia.",
    color: "#06b6d4"
  },
  {
    id: "ciencias-fuego",
    nombre: "PNF en Ciencias del Fuego y Seguridad Contra Incendios",
    corto: "Ciencias del Fuego",
    descripcion: "Dirigido a cuerpos de bomberos y especialistas en prevención y extinción de incendios.",
    color: "#ef4444"
  },
  {
    id: "proteccion-civil",
    nombre: "PNF en Protección Civil y Administración de Desastres",
    corto: "Protección Civil",
    descripcion: "Especialización en gestión del riesgo socio-natural y atención de emergencias y desastres.",
    color: "#f59e0b"
  },
  {
    id: "servicio-penitenciario",
    nombre: "PNF en Servicio Penitenciario",
    corto: "Serv. Penitenciario",
    descripcion: "Custodia, seguridad y garantía de los DDHH en el régimen penitenciario venezolano.",
    color: "#6b7280"
  },
  {
    id: "emergencias-prehospitalarias",
    nombre: "PNF en Emergencias Prehospitalarias",
    corto: "Emergencias Prehospitalarias",
    descripcion: "Atención médica inmediata y soporte vital básico y avanzado en situaciones de emergencia.",
    color: "#10b981"
  },
  {
    id: "seguridad-nacion",
    nombre: "PNF en Seguridad de la Nación",
    corto: "Seg. de la Nación",
    descripcion: "Estudio de las dinámicas estratégicas, geopolíticas y de defensa integral de la nación.",
    color: "#800020"
  }
];
'''

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/data.js', 'w', encoding='utf-8') as f:
    f.write(nuevo_data_js)
print("data.js actualizado.")

# 3. Actualizar unes_sistema_final.js y app.js
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_sistema_final.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Función de normalización en JavaScript
js_normalizar_nucleo = '''
// Función oficial de normalización y unificación de núcleos (ANZOATEGUI, anzoategui, ANZOÁTEGUI => ANZOÁTEGUI)
function normalizarNucleo(rawVal) {
  if (!rawVal) return 'CARACAS';
  let s = String(rawVal).trim();
  s = s.replace(/\\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN|TOKEN)\\b/gi, '').replace(/\\s+/g, ' ').trim();
  const clean = s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toUpperCase().trim();

  if (clean.includes('ANZOATEGUI')) return 'ANZOÁTEGUI';
  if (clean.includes('POLICARACAS')) return 'POLICARACAS';
  if (clean.includes('CARACAS')) return 'CARACAS';
  if (clean.includes('PORTUGUESA')) return 'PORTUGUESA';
  if (clean.includes('BARINAS')) return 'BARINAS';
  if (clean.includes('TRUJILLO')) return 'TRUJILLO';
  if (clean.includes('CARABOBO')) return 'CARABOBO';
  if (clean.includes('BARLOVENTO')) return 'BARLOVENTO';
  if (clean.includes('VALLES DEL TUY') || clean.includes('VALLE DEL TUY')) return 'VALLES DEL TUY';
  if (clean.includes('BOLIVAR') || clean.includes('ANGOSTURA')) return 'BOLÍVAR - ANGOSTURA';
  if (clean.includes('LLANITO')) return 'EL LLANITO';
  if (clean.includes('JUNQUITO')) return 'EL JUNQUITO';
  if (clean.includes('GUAIRA')) return 'LA GUAIRA';
  if (clean.includes('MONAGAS')) return 'MONAGAS';
  if (clean.includes('GUARENAS') || clean.includes('GUATIRE')) return 'GUARENAS - GUATIRE';
  if (clean.includes('NUEVA ESPARTA') || clean.includes('MARGARITA')) return 'NUEVA ESPARTA';
  if (clean.includes('FALCON')) return 'FALCÓN';
  if (clean.includes('YARACUY')) return 'YARACUY';
  if (clean.includes('ALTOS MIRANDINOS') || clean.includes('ALTO MIRANDINO')) return 'ALTOS MIRANDINOS';
  if (clean.includes('METROPOLITANO')) return 'EJE METROPOLITANO';
  if (clean.includes('SAN PEDRO')) return 'SAN PEDRO';
  if (clean.includes('POLISUCRE')) return 'POLISUCRE';
  if (clean.includes('LARA')) return 'LARA';
  if (clean.includes('ARAGUA')) return 'ARAGUA';
  if (clean.includes('ZULIA')) return 'ZULIA';
  if (clean.includes('MERIDA')) return 'MÉRIDA';
  if (clean.includes('TACHIRA')) return 'TÁCHIRA';
  if (clean.includes('APURE')) return 'APURE';
  if (clean.includes('COJEDES')) return 'COJEDES';
  if (clean.includes('GUARICO')) return 'GUÁRICO';
  if (clean.includes('SUCRE')) return 'SUCRE';
  if (clean.includes('AMAZONAS')) return 'AMAZONAS';
  if (clean.includes('DELTA')) return 'DELTA AMACURO';
  return s.toUpperCase();
}
'''

# Inyectar normalizarNucleo si no está
if 'function normalizarNucleo' not in code:
    idx_db = code.find('let DB =')
    code = code[:idx_db] + js_normalizar_nucleo + '\n' + code[idx_db:]

# Usar normalizarNucleo dentro de ejecutarImportacion
old_nucleo_logic = '''    // Limpieza de nombre de núcleo
    let nucleo = evalStr
      .replace(/\\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN|TOKEN)\\b/gi, '')
      .replace(/\\s+/g, ' ')
      .trim();
    if (!nucleo) nucleo = 'Caracas';'''

new_nucleo_logic = '''    // Limpieza y unificación oficial de núcleo
    let nucleo = normalizarNucleo(evalStr);'''

if old_nucleo_logic in code:
    code = code.replace(old_nucleo_logic, new_nucleo_logic)

# Normalizar núcleos también al cargar la base de datos
old_cargar_logic = "if (!isBad && parsed && parsed.estudiantes && parsed.estudiantes.length >= 50) {\n      DB = parsed;"
new_cargar_logic = """if (!isBad && parsed && parsed.estudiantes && parsed.estudiantes.length >= 50) {
      // Unificar núcleos existentes en caso de variaciones
      parsed.estudiantes.forEach(e => { e.nucleo = normalizarNucleo(e.nucleo || e.evaluacion); });
      DB = parsed;"""
if old_cargar_logic in code:
    code = code.replace(old_cargar_logic, new_cargar_logic)

# Actualizar INITIAL_ESTUDIANTES con los datos unificados
start_idx = code.find('const INITIAL_ESTUDIANTES =')
end_idx = code.find('const CAMPOS_SISTEMA =')
new_init = 'const INITIAL_ESTUDIANTES = ' + json.dumps(data['estudiantes'], ensure_ascii=False) + ';\n\n// CAMPOS RECONOCIDOS\n'
code = code[:start_idx] + new_init + code[end_idx:]

# Incrementar versión de DB a 7 para invalidar cualquier caché anterior con nombres desunificados
code = code.replace("version < 6", "version < 7")
code = code.replace("DB.version = 6", "DB.version = 7")
code = code.replace("dataset oficial UNES v6", "dataset oficial UNES v7 (Núcleos Unificados)")

# Guardar en ambos archivos
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/unes_sistema_final.js', 'w', encoding='utf-8') as f:
    f.write(code)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("unes_sistema_final.js y app.js actualizados con normalizarNucleo.")

# 4. Actualizar index.html con auto-purge version < 7
with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("_db.version < 6", "_db.version < 7")
html = html.replace("_db.version < 5", "_db.version < 7")

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html actualizado a versión 7.")
