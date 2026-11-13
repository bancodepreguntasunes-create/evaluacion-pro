import openpyxl
import json
import re
import unicodedata
import sys

excel_path = r'C:/Users/PC/.gemini/antigravity/brain/5b0b08a9-b938-4fc8-b006-63249b295d73/.user_uploaded/media_1794425644709_fe4a93e7.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active
headers = [str(c.value or '').strip() for c in ws[1]]

col_map = {}
for idx, h in enumerate(headers):
    hl = h.lower()
    if 'cédula' in hl or 'cedula' in hl: col_map['cedula'] = idx
    elif '1er nombre' in hl: col_map['nom1'] = idx
    elif '2do nombre' in hl: col_map['nom2'] = idx
    elif '1er apellido' in hl: col_map['ap1'] = idx
    elif '2do apellido' in hl: col_map['ap2'] = idx
    elif 'evaluaci' in hl: col_map['eval'] = idx
    elif 'carrera' in hl: col_map['carrera'] = idx
    elif 'token' in hl: col_map['token'] = idx
    elif 'pts' in hl: col_map['pts'] = idx
    elif 'aprobado' in hl: col_map['aprobado'] = idx

def normalizar_nucleo(raw_val):
    if not raw_val: return 'CARACAS'
    s = str(raw_val).strip()
    s = re.sub(r'\b(T[0-9I]+|SP|IPCR|IPCRI|IP|CF|PCAD|EPH|CP|MN|TOKEN)\b', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip()
    clean = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper().strip()
    
    if 'ANZOATEGUI' in clean or 'ANACO' in clean: return 'ANZOÁTEGUI'
    if 'POLICARACAS' in clean: return 'POLICARACAS'
    if 'POLISUCRE' in clean: return 'POLISUCRE'
    if 'CARACAS' in clean: return 'CARACAS'
    if 'CAFETAL' in clean: return 'CAFETAL'
    if 'PORTUGUESA' in clean: return 'PORTUGUESA'
    if 'BARINAS' in clean: return 'BARINAS'
    if 'TRUJILLO' in clean: return 'TRUJILLO'
    if 'CARABOBO' in clean: return 'CARABOBO'
    if 'BARLOVENTO' in clean: return 'BARLOVENTO'
    if 'VALLES DEL TUY' in clean or 'VALLE DEL TUY' in clean: return 'VALLES DEL TUY'
    if 'PT.O' in clean or 'PUERTO ORDAZ' in clean or 'PTO. ORDAZ' in clean: return 'BOLÍVAR - PTO. ORDAZ'
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
    if 'LARA' in clean: return 'LARA'
    if 'ARAGUA' in clean: return 'ARAGUA'
    if 'ZULIA' in clean: return 'ZULIA'
    if 'MERIDA' in clean: return 'MÉRIDA'
    if 'TACHIRA' in clean: return 'TÁCHIRA'
    if 'APURE' in clean: return 'APURE'
    if 'COJEDES' in clean: return 'COJEDES'
    if 'GUARICO' in clean: return 'GUÁRICO'
    if 'CARUPANO' in clean: return 'SUCRE - CARÚPANO'
    if 'CUMANA' in clean or 'SUCRE' in clean or 'POLICIA ESTADAL' in clean: return 'SUCRE - CUMANÁ'
    if 'AMAZONAS' in clean or 'AMAZONA' in clean: return 'AMAZONAS'
    if 'DELTA' in clean: return 'DELTA AMACURO'
    return s.upper()

def nucleo_to_estado(n):
    if n in ['CARACAS', 'POLICARACAS', 'SAN PEDRO', 'EL LLANITO', 'EL JUNQUITO', 'CAFETAL', 'POLISUCRE']:
        return 'CARACAS'
    if n in ['BARLOVENTO', 'VALLES DEL TUY', 'GUARENAS - GUATIRE', 'ALTOS MIRANDINOS', 'EJE METROPOLITANO']:
        return 'MIRANDA'
    if n in ['BOLÍVAR - ANGOSTURA', 'BOLÍVAR - PTO. ORDAZ']:
        return 'BOLÍVAR'
    if n in ['SUCRE - CUMANÁ', 'SUCRE - CARÚPANO', 'SUCRE', 'POLICIA ESTADAL']:
        return 'SUCRE'
    if n == 'LA GUAIRA': return 'LA GUAIRA'
    if n == 'ANZOÁTEGUI': return 'ANZOÁTEGUI'
    if n == 'PORTUGUESA': return 'PORTUGUESA'
    if n == 'BARINAS': return 'BARINAS'
    if n == 'MÉRIDA': return 'MÉRIDA'
    if n == 'ZULIA': return 'ZULIA'
    if n == 'MONAGAS': return 'MONAGAS'
    if n == 'FALCÓN': return 'FALCÓN'
    if n == 'TRUJILLO': return 'TRUJILLO'
    if n == 'CARABOBO': return 'CARABOBO'
    if n == 'NUEVA ESPARTA': return 'NUEVA ESPARTA'
    if n == 'APURE': return 'APURE'
    if n == 'AMAZONAS': return 'AMAZONAS'
    if n == 'TÁCHIRA': return 'TÁCHIRA'
    if n == 'DELTA AMACURO': return 'DELTA AMACURO'
    if n == 'YARACUY': return 'YARACUY'
    if n == 'COJEDES': return 'COJEDES'
    if n in ['LARA', 'PRUEBA LR']: return 'LARA'
    if n == 'ARAGUA': return 'ARAGUA'
    if n == 'GUÁRICO': return 'GUÁRICO'
    return 'CARACAS'

def detect_trayecto(eval_str):
    if not eval_str: return 'I'
    if re.search(r'\bTI\b', eval_str, re.I): return 'Inicial'
    if re.search(r'\bT2\b', eval_str, re.I): return 'II'
    if re.search(r'\bT3\b', eval_str, re.I): return 'III'
    if re.search(r'\bT4\b', eval_str, re.I): return 'IV'
    if re.search(r'\bT1\b', eval_str, re.I): return 'I'
    return 'I'

students = []
student_id = 1

for r in ws.iter_rows(min_row=2, values_only=True):
    ced = str(r[col_map['cedula']] or '').strip()
    if not ced: continue
    
    n1 = str(r[col_map['nom1']] or '').strip()
    n2 = str(r[col_map['nom2']] or '').strip()
    a1 = str(r[col_map['ap1']] or '').strip()
    a2 = str(r[col_map['ap2']] or '').strip()
    nombre = f"{n1} {n2} {a1} {a2}".strip()
    nombre = re.sub(r'\s+', ' ', nombre).title()
    if not nombre: nombre = "Estudiante " + ced
    
    ev = str(r[col_map['eval']] or '').strip()
    cr = str(r[col_map['carrera']] or '').strip()
    tok = str(r[col_map['token']] or '').strip()
    
    # PNF
    if not cr or cr == 'None' or cr == '' or re.search(r'\bCP\b', ev, re.I):
        pnf = 'Ciencias Policiales'
    else:
        pnf = cr
        if 'policial' in pnf.lower(): pnf = 'Servicio Policial'
        elif 'penitenciario' in pnf.lower(): pnf = 'Servicio Penitenciario'
        elif 'fuego' in pnf.lower() or 'bomber' in pnf.lower(): pnf = 'Ciencias del Fuego'
        elif 'civil' in pnf.lower(): pnf = 'Protección Civil'
        elif 'pre-hospitalaria' in pnf.lower() or 'prehospitalaria' in pnf.lower(): pnf = 'Emergencias Prehospitalarias'
        elif 'investigación penal y' in pnf.lower() or 'investigacion penal y' in pnf.lower(): pnf = 'Investigación Penal y Criminalística'
        elif 'investigación penal' in pnf.lower() or 'investigacion penal' in pnf.lower(): pnf = 'Investigación Penal'
        elif 'criminal' in pnf.lower(): pnf = 'Criminalística'

    nucleo = normalizar_nucleo(ev)
    estado = nucleo_to_estado(nucleo)
    trayecto = detect_trayecto(ev)
    
    pts_raw = r[col_map['pts']]
    pts = None
    try:
        if pts_raw is not None and str(pts_raw).strip() != '':
            pts = float(str(pts_raw).replace(',', '.'))
    except:
        pass

    raw_ap = str(r[col_map['aprobado']] or '').strip().lower()
    if raw_ap in ['true', '1', 'si', 'sí', 'aprobado']:
        estatus = 'Aprobado'
    elif raw_ap in ['false', '0', 'no', 'reprobado']:
        estatus = 'Reprobado'
    elif pts is not None:
        estatus = 'Aprobado' if pts >= 60 else 'Reprobado'
    else:
        estatus = 'Aprobado'

    students.append({
        'id': str(student_id),
        'cedula': ced,
        'nombre': nombre,
        'nucleo': nucleo,
        'estado': estado,
        'pnf': pnf,
        'trayecto': trayecto,
        'token': tok,
        'evaluacion': ev,
        'estatus': estatus,
        'puntaje': pts
    })
    student_id += 1

out_json = r'C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_importados.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'estudiantes': students, 'nextId': student_id}, f, ensure_ascii=False, indent=2)

ap_count = sum(1 for s in students if s['estatus'] == 'Aprobado')
rep_count = sum(1 for s in students if s['estatus'] == 'Reprobado')
print(f"Master dataset created successfully! Total: {len(students)} | Aprobados: {ap_count} ({round(ap_count/len(students)*100, 2)}%) | Reprobados: {rep_count}")
