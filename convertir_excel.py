
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import openpyxl, json, re
from collections import Counter

files = [
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_48799fb4.xlsx',
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_ccf5c018.xlsx',
]

# PNF sigla -> nombre completo
PNF_MAP = {
    'SP':   'Servicio Policial',
    'IPCR': 'Investigación Penal y Criminalística',
    'IP':   'Investigación Penal',
    'CF':   'Ciencias del Fuego y Seguridad Contra Incendios',
    'PCAD': 'Protección Civil y Administración de Desastres',
    'EPH':  'Emergencia Pre-Hospitalaria',
    'CP':   'Criminalística y Policía',
    'MN':   'Medicina Natural',
    'SS':   'Seguridad Social',
}

# Trayecto normalization
TRAYECTO_MAP = {
    'T1': 'I', 'T2': 'II', 'T3': 'III', 'T4': 'IV',
    'TI': 'Inicial', 'T0': 'Inicial',
}

def parse_evaluacion(nombre_eval):
    """Extract nucleo, pnf_sigla, trayecto from e.g. 'LLANITO SP T2'"""
    nombre_eval = nombre_eval.strip()
    # Find trayecto pattern at end
    t_match = re.search(r'\bT([0-9I]+)\b', nombre_eval.upper())
    trayecto_raw = ''
    if t_match:
        trayecto_raw = 'T' + t_match.group(1).upper()
    trayecto = TRAYECTO_MAP.get(trayecto_raw, trayecto_raw)
    
    # Remove trayecto from string to find PNF
    without_t = re.sub(r'\bT[0-9I]+\b', '', nombre_eval, flags=re.IGNORECASE).strip()
    
    # Try to find known PNF siglas
    pnf_found = ''
    pnf_full  = ''
    for sigla, full in PNF_MAP.items():
        if re.search(r'\b' + sigla + r'\b', without_t, re.IGNORECASE):
            pnf_found = sigla
            pnf_full  = full
            break
    
    # Nucleo = everything that's not the PNF sigla
    nucleo = re.sub(r'\b' + (pnf_found or 'XXXXXX') + r'\b', '', without_t, flags=re.IGNORECASE).strip()
    nucleo = re.sub(r'\s+', ' ', nucleo).strip().title()
    
    return nucleo, pnf_full or without_t, trayecto

estudiantes = []
next_id = 1
errores = []

for path in files:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(h).strip() for h in rows[0]]

    # Map header names
    def col(name):
        candidates = [h for h in headers if name.lower() in h.lower()]
        return headers.index(candidates[0]) if candidates else -1

    h_fecha   = col('Fecha')
    h_cedula  = col('Cédula')
    h_nom1    = col('1er Nombre')
    h_nom2    = col('2do Nombre')
    h_ap1     = col('1er Apellido')
    h_ap2     = col('2do Apellido')
    h_eval    = col('Nombre de la Evaluación')
    h_carrera = col('Carrera')
    h_token   = col('Token')
    h_pts     = col('Pts')

    print(f'\n{path.split(chr(92))[-1]} — {len(rows)-1} filas')

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

        if not cedula:
            errores.append(f'Fila {idx}: sin cédula')
            continue

        # Parse pts
        try:
            pts = float(str(pts_raw).replace(',','.'))
        except:
            pts = None
            errores.append(f'Fila {idx} ({cedula}): Pts inválido = {pts_raw!r}')

        # Determine estatus
        estatus = ('Aprobado' if pts is not None and pts >= 60 else 'Reprobado') if pts is not None else ''

        # Parse nucleo, pnf, trayecto from eval string
        nucleo, pnf, trayecto = parse_evaluacion(eval_str)

        # Use carrera column as PNF if available and meaningful
        if carrera and len(carrera) > 2:
            pnf = carrera

        estudiantes.append({
            'id': str(next_id),
            'cedula': cedula,
            'nombre': nombre,
            'nucleo': nucleo,
            'pnf': pnf,
            'trayecto': trayecto,
            'token': token,
            'estatus': estatus,
            'puntaje': pts,
        })
        next_id += 1

    wb.close()

print(f'\nTotal estudiantes procesados: {len(estudiantes)}')
print(f'Aprobados: {sum(1 for e in estudiantes if e["estatus"]=="Aprobado")}')
print(f'Reprobados: {sum(1 for e in estudiantes if e["estatus"]=="Reprobado")}')
print(f'Errores: {len(errores)}')
if errores[:5]:
    print('Primeros errores:', errores[:5])

# Sample output
print('\nMuestra (primeros 3):')
for e in estudiantes[:3]:
    print(' ', e)

# Save as JSON for the sistema
out = {
    'estudiantes': estudiantes,
    'nextId': next_id
}
out_path = r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'\nGuardado en: {out_path}')
