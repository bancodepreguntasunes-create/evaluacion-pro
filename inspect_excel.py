
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import openpyxl
except ImportError:
    import subprocess
    subprocess.run(['pip', 'install', 'openpyxl', '-q'])
    import openpyxl

files = [
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_48799fb4.xlsx',
    r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.user_uploaded\media_1793991619818_ccf5c018.xlsx',
]

for path in files:
    print(f'\n{"="*60}')
    print(f'FILE: {path.split(chr(92))[-1]}')
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f'\nHoja: "{sheet_name}"')
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            print('  (vacía)')
            continue
        headers = rows[0]
        print(f'  Columnas ({len(headers)}): {list(headers)}')
        print(f'  Total filas de datos: {len(rows)-1}')
        print('  Primeras 3 filas:')
        for i, r in enumerate(rows[1:4], 1):
            print(f'    Fila {i}: {list(r)}')
    wb.close()
