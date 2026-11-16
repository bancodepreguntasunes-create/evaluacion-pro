# -*- coding: utf-8 -*-
import json
with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json", "r", encoding="utf-8") as f:
    d = json.load(f)
est = d["estudiantes"]
print("Total:", len(est))
print("Keys:", list(est[0].keys()))
ap = sum(1 for e in est if e.get("estatus")=="Aprobado")
rep = sum(1 for e in est if e.get("estatus")=="Reprobado")
print("Ap:", ap, "Rep:", rep)

nucleos = {}
for e in est:
    n = e.get("nucleo") or "Sin Nucleo"
    if n not in nucleos:
        nucleos[n] = {"ap":0,"rep":0,"tot":0,"estado":e.get("estado","")}
    nucleos[n]["tot"]+=1
    if e.get("estatus")=="Aprobado":
        nucleos[n]["ap"]+=1
    else:
        nucleos[n]["rep"]+=1
print("Nucleos:", len(nucleos))
for n,v in sorted(nucleos.items(), key=lambda x: x[1]["tot"], reverse=True)[:5]:
    pct = round(v["ap"]/v["tot"]*100,1)
    tot = v["tot"]
    print(f"  {n}: {tot} ({pct}%)")

# PNF
pnfs = {}
for e in est:
    p = e.get("pnf") or "Sin PNF"
    if p not in pnfs:
        pnfs[p] = {"ap":0,"rep":0,"tot":0}
    pnfs[p]["tot"]+=1
    if e.get("estatus")=="Aprobado":
        pnfs[p]["ap"]+=1
    else:
        pnfs[p]["rep"]+=1
print("PNFs:", len(pnfs))
for n,v in sorted(pnfs.items(), key=lambda x: x[1]["tot"], reverse=True)[:5]:
    pct = round(v["ap"]/v["tot"]*100,1)
    print(f"  {n}: {v['tot']} ({pct}%)")
