import openpyxl, json, re, unicodedata, sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r'C:/Users/PC/.gemini/antigravity/brain/5b0b08a9-b938-4fc8-b006-63249b295d73/.user_uploaded/media_1794425644709_fe4a93e7.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active
headers = [c.value for c in ws[1]]

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
    if n in ['SUCRE - CUMANÁ', 'SUCRE - CARÚPANO', 'SUCRE']:
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

estado_stats = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    d = dict(zip(headers, r))
    ev = str(d.get('Nombre de la Evaluación') or '').strip()
    n = normalizar_nucleo(ev)
    est = nucleo_to_estado(n)
    
    apr = str(d.get('Aprobado') or '').strip().lower()
    pts = d.get('Pts')
    try: pts = float(str(pts).replace(',', '.'))
    except: pts = None
    
    is_ap = False
    if apr in ['true', '1', 'si', 'sí', 'aprobado']: is_ap = True
    elif apr in ['false', '0', 'no', 'reprobado']: is_ap = False
    elif pts is not None: is_ap = (pts >= 60)
    else: is_ap = True
    
    if est not in estado_stats:
        estado_stats[est] = {'ap': 0, 'rep': 0, 'tot': 0, 'nucleos': {}}
    estado_stats[est]['tot'] += 1
    if is_ap: estado_stats[est]['ap'] += 1
    else: estado_stats[est]['rep'] += 1
    
    # Track nucleos within state
    if n not in estado_stats[est]['nucleos']:
        estado_stats[est]['nucleos'][n] = {'ap': 0, 'rep': 0, 'tot': 0}
    estado_stats[est]['nucleos'][n]['tot'] += 1
    if is_ap: estado_stats[est]['nucleos'][n]['ap'] += 1
    else: estado_stats[est]['nucleos'][n]['rep'] += 1

print('ESTADÍSTICAS POR ESTADO EN VENEZUELA:')
for k, v in sorted(estado_stats.items(), key=lambda x: -x[1]['tot']):
    pct = round(v['ap'] / v['tot'] * 100, 1)
    tot = v['tot']
    ap = v['ap']
    rep = v['rep']
    print(f"  {k:18}: Total={tot:4} | Aprobados={ap:4} ({pct:5.1f}%) | Reprobados={rep:3}")
