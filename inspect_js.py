
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js','rb') as f: d=f.read().decode('utf-8','replace')

keywords = ['aprobado','Aprobado','reprobado','60','80','estado','puntaje','nota','pts','score','importar','ejecutarIm','FileReader','multiple','files']
seen = set()
for kw in keywords:
    lo = d.lower()
    start = 0
    while True:
        idx = lo.find(kw.lower(), start)
        if idx == -1: break
        key = (idx//200)  # group nearby
        if key not in seen:
            seen.add(key)
            snippet = d[max(0,idx-40):idx+120]
            print(f'--- [{kw}] pos={idx} ---')
            print(snippet)
            print()
        start = idx + len(kw)

