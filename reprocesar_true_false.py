
import sys, io, json, re, openpyxl
from collections import Counter

files = [
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_48799fb4.xlsx',
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_ccf5c018.xlsx',
]

PNF_MAP = {
    'CP':   'Ciencias Policiales',
    'SP':   'Servicio Policial',
    'IPCR': 'Investigación Penal y Criminalística',
    'IP':   'Investigación Penal',
    'CF':   'Ciencias del Fuego y Seguridad Contra Incendios',
    'PCAD': 'Protección Civil y Administración de Desastres',
    'EPH':  'Emergencia Pre-Hospitalaria',
    'CR':   'Criminalística',
    'MN':   'Medicina Natural',
    'SS':   'Seguridad Social',
}

TRAYECTO_MAP = {
    'T1': 'I', 'T2': 'II', 'T3': 'III', 'T4': 'IV',
    'TI': 'Inicial', 'T0': 'Inicial',
}

def parse_eval(eval_str):
    s = eval_str.strip()
    t_match = re.search(r'\bT([0-9I]+)\b', s.upper())
    trayecto = ''
    if t_match:
        t_raw = 'T' + t_match.group(1).upper()
        trayecto = TRAYECTO_MAP.get(t_raw, t_raw)
    
    without_t = re.sub(r'\bT[0-9I]+\b', '', s, flags=re.IGNORECASE).strip()
    pnf_full = ''
    pnf_sigla = ''
    for sigla in ['IPCR', 'PCAD', 'EPH', 'SP', 'CF', 'CP', 'CR', 'IP']:
        if re.search(r'\b' + sigla + r'\b', without_t, re.IGNORECASE):
            pnf_sigla = sigla
            pnf_full = PNF_MAP.get(sigla, sigla)
            break
            
    nucleo = re.sub(r'\b' + (pnf_sigla or 'ZZZZ') + r'\b', '', without_t, flags=re.IGNORECASE)
    nucleo = re.sub(r'\bMN\b', '', nucleo, flags=re.IGNORECASE)
    nucleo = re.sub(r'\s+', ' ', nucleo).strip().title()
    
    return nucleo, pnf_full, trayecto

estudiantes = []
next_id = 1

for path in files:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(h).strip() for h in rows[0]]

    def col(name):
        candidates = [h for h in headers if name.lower() in h.lower()]
        return headers.index(candidates[0]) if candidates else -1

    h_cedula   = col('Cédula')
    h_nom1     = col('1er Nombre')
    h_nom2     = col('2do Nombre')
    h_ap1      = col('1er Apellido')
    h_ap2      = col('2do Apellido')
    h_eval     = col('Nombre de la Evaluación')
    h_carrera  = col('Carrera')
    h_token    = col('Token')
    h_pts      = col('Pts')
    h_aprobado = col('Aprobado')

    for idx, row in enumerate(rows[1:], 2):
        cedula   = str(row[h_cedula] or '').strip()
        nom1     = str(row[h_nom1]   or '').strip().title()
        nom2     = str(row[h_nom2]   or '').strip().title()
        ap1      = str(row[h_ap1]    or '').strip().title()
        ap2      = str(row[h_ap2]    or '').strip().title()
        nombre   = f'{nom1} {nom2} {ap1} {ap2}'.strip()
        nombre   = re.sub(r'\s+', ' ', nombre)

        eval_str = str(row[h_eval]    or '').strip()
        carrera  = str(row[h_carrera] or '').strip()
        token    = str(row[h_token]   or '').strip()
        pts_raw  = row[h_pts]
        ap_raw   = str(row[h_aprobado] if h_aprobado != -1 else '').strip().lower()

        if not cedula:
            continue

        try:
            pts = float(str(pts_raw).replace(',','.'))
        except:
            pts = 0.0

        # CRITERIO DEL USUARIO: "lo que dice true es aprobado false reprobado"
        if ap_raw in ['true', '1', 'si', 'sí', 'aprobado']:
            estatus = 'Aprobado'
        elif ap_raw in ['false', '0', 'no', 'reprobado']:
            estatus = 'Reprobado'
        else:
            estatus = 'Aprobado' if pts >= 60 else 'Reprobado'

        nucleo, pnf_from_eval, trayecto = parse_eval(eval_str)

        if not carrera or carrera.strip() == '' or 'CP' in eval_str.upper().split():
            pnf = 'Ciencias Policiales'
        else:
            pnf = carrera.strip()

        if not nucleo or nucleo.strip() == '':
            nucleo = 'Caracas'
        if nucleo.lower() in ['el llanito', 'llanito']:
            nucleo = 'El Llanito'
        elif 'bolivar' in nucleo.lower():
            nucleo = 'Bolívar - Angostura'
        elif 'san pedro' in nucleo.lower():
            nucleo = 'San Pedro'
        elif 'guarenas' in nucleo.lower():
            nucleo = 'Eje Guarenas - Guatire'
        elif 'barlovento' in nucleo.lower():
            nucleo = 'Eje Barlovento'
        elif 'valles del tuy' in nucleo.lower():
            nucleo = 'Eje Valles del Tuy'
        elif 'altos mirandinos' in nucleo.lower():
            nucleo = 'Eje Altos Mirandinos'
        elif 'metropolitano' in nucleo.lower():
            nucleo = 'Eje Metropolitano'
        elif 'guaira' in nucleo.lower():
            nucleo = 'La Guaira'
        elif 'junquito' in nucleo.lower():
            nucleo = 'Junquito'
        elif 'policaracas' in nucleo.lower() or 'caracas' in nucleo.lower() or 'polisucre' in nucleo.lower():
            nucleo = 'Caracas'
        elif 'portuguesa' in nucleo.lower():
            nucleo = 'Portuguesa'
        elif 'barinas' in nucleo.lower():
            nucleo = 'Barinas'
        elif 'nueva esparta' in nucleo.lower():
            nucleo = 'Nueva Esparta'

        estudiantes.append({
            'id': str(next_id),
            'cedula': cedula,
            'nombre': nombre,
            'nucleo': nucleo,
            'pnf': pnf,
            'trayecto': trayecto or 'I',
            'token': token,
            'estatus': estatus,
            'puntaje': pts
        })
        next_id += 1

print(f'Total procesados: {len(estudiantes)}')
ap = sum(1 for e in estudiantes if e['estatus'] == 'Aprobado')
rep = sum(1 for e in estudiantes if e['estatus'] == 'Reprobado')
print(f'Aprobados (true): {ap}')
print(f'Reprobados (false): {rep}')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json', 'w', encoding='utf-8') as f:
    json.dump({'estudiantes': estudiantes, 'nextId': next_id}, f, ensure_ascii=False, indent=2)
print('datos_importados.json re-saved!')
