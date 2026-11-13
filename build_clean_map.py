import re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\venezuela_real.svg', 'r', encoding='utf-8') as f:
    svg = f.read()

state_ids = ['VE-A','VE-B','VE-C','VE-D','VE-E','VE-F','VE-G','VE-H',
             'VE-I','VE-J','VE-K','VE-L','VE-M','VE-N','VE-O','VE-P',
             'VE-R','VE-S','VE-T','VE-U','VE-V','VE-X','VE-Y','VE-Z']

segments = svg.split('<path')
paths_data = {}
for seg in segments[1:]:
    id_match = re.search(r'id="([^"]+)"', seg)
    title_match = re.search(r'title="([^"]+)"', seg)
    d_match = re.search(r'd="([^"]+)"', seg)
    if id_match and title_match and d_match:
        pid = id_match.group(1)
        title = title_match.group(1).strip()
        d = d_match.group(1)
        if pid in state_ids:
            paths_data[pid] = {'title': title, 'd': d}

id_to_estado = {
    'VE-A': 'CARACAS',
    'VE-B': 'ANZOÁTEGUI',
    'VE-C': 'APURE',
    'VE-D': 'ARAGUA',
    'VE-E': 'BARINAS',
    'VE-F': 'BOLÍVAR',
    'VE-G': 'CARABOBO',
    'VE-H': 'COJEDES',
    'VE-I': 'FALCÓN',
    'VE-J': 'GUÁRICO',
    'VE-K': 'LARA',
    'VE-L': 'MÉRIDA',
    'VE-M': 'MIRANDA',
    'VE-N': 'MONAGAS',
    'VE-O': 'NUEVA ESPARTA',
    'VE-P': 'PORTUGUESA',
    'VE-R': 'SUCRE',
    'VE-S': 'TÁCHIRA',
    'VE-T': 'TRUJILLO',
    'VE-U': 'YARACUY',
    'VE-V': 'ZULIA',
    'VE-X': 'LA GUAIRA',
    'VE-Y': 'DELTA AMACURO',
    'VE-Z': 'AMAZONAS',
}

label_positions = {
    'VE-A': (291, 92),
    'VE-B': (478, 175),
    'VE-C': (198, 285),
    'VE-D': (259, 110),
    'VE-E': (176, 240),
    'VE-F': (430, 410),
    'VE-G': (251, 102),
    'VE-H': (300, 160),
    'VE-I': (168, 65),
    'VE-J': (352, 215),
    'VE-K': (175, 110),
    'VE-L': (133, 185),
    'VE-M': (326, 110),
    'VE-N': (534, 190),
    'VE-O': (540, 70),
    'VE-P': (212, 160),
    'VE-R': (532, 130),
    'VE-S': (111, 220),
    'VE-T': (161, 140),
    'VE-U': (240, 82),
    'VE-V': (88, 130),
    'VE-X': (302, 73),
    'VE-Y': (583, 260),
    'VE-Z': (310, 430),
}

short_labels = {
    'ANZOÁTEGUI': 'ANZ',
    'DELTA AMACURO': 'DEL',
    'NUEVA ESPARTA': 'N.E.',
    'LA GUAIRA': 'L.G.',
    'PORTUGUESA': 'POR',
    'COJEDES': 'COJ',
    'GUÁRICO': 'GUA',
    'MIRANDA': 'MIR',
    'BARINAS': 'BAR',
    'MONAGAS': 'MON',
    'TÁCHIRA': 'TAC',
    'TRUJILLO': 'TRU',
    'YARACUY': 'YAR',
    'CARABOBO': 'CAR',
    'MÉRIDA': 'MER',
    'ARAGUA': 'ARA',
    'BOLÍVAR': 'BOL',
    'AMAZONAS': 'AMA',
    'CARACAS': 'D.C.',
    'LARA': 'LAR',
    'APURE': 'APU',
    'FALCÓN': 'FAL',
    'ZULIA': 'ZUL',
    'SUCRE': 'SUC'
}

paths_html = []
for pid, data in paths_data.items():
    estado = id_to_estado.get(pid, pid)
    d = data['d']
    lx, ly = label_positions.get(pid, (0, 0))
    short = short_labels.get(estado, estado[:3])
    paths_html.append(
        f'<path id="map-{pid}" class="map-state" data-estado="{estado}" data-pid="{pid}" '
        f'onclick="seleccionarEstado(\'{estado}\')" onmouseenter="hoverEstado(\'{estado}\', event)" '
        f'onmouseleave="leaveEstado()" d="{d}"/>'
    )
    paths_html.append(f'<text class="map-label" x="{lx}" y="{ly}" onclick="seleccionarEstado(\'{estado}\')">{short}</text>')

clean_map_paths = '\n              '.join(paths_html)
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\map_paths.txt', 'w', encoding='utf-8') as f:
    f.write(clean_map_paths)

print("Generated clean UTF-8 map_paths.txt successfully! Total paths:", len(paths_data))
