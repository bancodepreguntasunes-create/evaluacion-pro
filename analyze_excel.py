
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Analyze "Nombre de la Evaluación" to understand nucleo+trayecto patterns
import openpyxl, re
from collections import Counter

files = [
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_48799fb4.xlsx',
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_ccf5c018.xlsx',
]

all_evaluaciones = []
all_carreras = []
all_pts = []

for path in files:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(h) for h in rows[0]]
    h_eval = headers.index('Nombre de la Evaluación')
    h_car  = headers.index('Carrera')
    h_pts  = headers.index('Pts')
    
    for row in rows[1:]:
        all_evaluaciones.append(str(row[h_eval] or '').strip())
        all_carreras.append(str(row[h_car] or '').strip())
        all_pts.append(row[h_pts])
    wb.close()

print('=== Nombre de la Evaluación (unique samples) ===')
for v, c in Counter(all_evaluaciones).most_common(30):
    print(f'  {c:4d}x  {v!r}')

print('\n=== Carreras (unique) ===')
for v, c in Counter(all_carreras).most_common(20):
    print(f'  {c:4d}x  {v!r}')

print('\n=== Pts distribution ===')
pts_nums = [p for p in all_pts if isinstance(p, (int,float))]
aprobados = sum(1 for p in pts_nums if p >= 60)
reprobados = sum(1 for p in pts_nums if p < 60)
print(f'  Total: {len(pts_nums)}')
print(f'  >= 60 (Aprobado): {aprobados}')
print(f'  < 60  (Reprobado): {reprobados}')
print(f'  Min: {min(pts_nums)}, Max: {max(pts_nums)}, Avg: {sum(pts_nums)/len(pts_nums):.1f}')
