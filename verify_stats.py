
import json

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

est = data['estudiantes']
pnf_stats = {}
for e in est:
    p = e['pnf']
    if p not in pnf_stats:
        pnf_stats[p] = {'tot': 0, 'ap': 0, 'rep': 0}
    pnf_stats[p]['tot'] += 1
    if e['estatus'] == 'Aprobado':
        pnf_stats[p]['ap'] += 1
    else:
        pnf_stats[p]['rep'] += 1

ap = sum(1 for e in est if e['estatus'] == 'Aprobado')
rep = sum(1 for e in est if e['estatus'] == 'Reprobado')
print('Total general:', len(est))
print('Total Aprobados (true):', ap)
print('Total Reprobados (false):', rep)
print('\nDesglose por PNF:')
for p, s in sorted(pnf_stats.items(), key=lambda x: x[1]['tot'], reverse=True):
    pct = round(s['ap'] / s['tot'] * 100)
    print(f"  {p[:40]:40s} | Tot: {s['tot']:4d} | Ap: {s['ap']:4d} | Rep: {s['rep']:3d} | {pct}%")
