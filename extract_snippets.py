
import json, re

transcript_path = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'

snippets = []
with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        # find any block with code or functions
        for fn in ['renderDashboard', 'filtrarTabla', 'renderRecientes', 'generarReporte', 'renderCalendario', 'guardarDB', 'cargarDB', 'toast', 'showView', 'ejecutarImportacion', 'CAMPOS_SISTEMA', 'construirMapaPNF', 'exportarCSV', 'toggleSidebar', 'sortPNF', 'filtrarPNF']:
            if fn in line:
                snippets.append((idx, fn))
                break

print(f'Total matches found: {len(snippets)}')
# show line indices
print(snippets[:50])
