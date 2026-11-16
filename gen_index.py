#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

# ── Datos ─────────────────────────────────────────────────────────────────────
raw       = json.load(open(os.path.join(BASE,"datos_importados.json"),encoding="utf-8"))
est_all   = raw["estudiantes"]
ve_paths  = json.load(open(os.path.join(BASE,"ve_paths.json"),encoding="utf-8"))

total     = len(est_all)
aprobados = sum(1 for e in est_all if e.get("estatus")=="Aprobado")
reprobados= total - aprobados
pct_apr   = round(aprobados/total*100,1)

# Por núcleo
nd={}
for e in est_all:
    n=e.get("nucleo",""); s=e.get("estado","")
    if n not in nd: nd[n]={"nucleo":n,"estado":s,"total":0,"aprobados":0}
    nd[n]["total"]+=1
    if e.get("estatus")=="Aprobado": nd[n]["aprobados"]+=1
for v in nd.values(): v["pct"]=round(v["aprobados"]/v["total"]*100,1) if v["total"] else 0
nucleos_list=sorted(nd.values(),key=lambda x:-x["total"])

# Por PNF
pd={}
for e in est_all:
    p=e.get("pnf","")
    if p not in pd: pd[p]={"pnf":p,"total":0,"aprobados":0}
    pd[p]["total"]+=1
    if e.get("estatus")=="Aprobado": pd[p]["aprobados"]+=1
for v in pd.values(): v["pct"]=round(v["aprobados"]/v["total"]*100,1) if v["total"] else 0
pnf_list=sorted(pd.values(),key=lambda x:-x["total"])

# Por trayecto
td={}
for e in est_all:
    t=e.get("trayecto","")
    td[t]=td.get(t,0)+1
trayecto_list=sorted(td.items(),key=lambda x:-x[1])

# Por estado
sdmap={}
for e in est_all:
    s=e.get("estado","")
    if s not in sdmap: sdmap[s]={"estado":s,"total":0,"aprobados":0}
    sdmap[s]["total"]+=1
    if e.get("estatus")=="Aprobado": sdmap[s]["aprobados"]+=1
for v in sdmap.values(): v["pct"]=round(v["aprobados"]/v["total"]*100,1) if v["total"] else 0

# ── Mapa SVG ──────────────────────────────────────────────────────────────────
state_id_map={
    "VE-A":"CARACAS","VE-B":"ANZOATEGUI","VE-C":"APURE","VE-D":"ARAGUA",
    "VE-E":"BARINAS","VE-F":"BOLIVAR","VE-G":"CARABOBO","VE-H":"COJEDES",
    "VE-I":"FALCON","VE-J":"GUARICO","VE-K":"LARA","VE-L":"MERIDA",
    "VE-M":"MIRANDA","VE-N":"MONAGAS","VE-O":"NUEVA ESPARTA","VE-P":"PORTUGUESA",
    "VE-R":"SUCRE","VE-S":"TACHIRA","VE-T":"TRUJILLO","VE-U":"YARACUY",
    "VE-V":"ZULIA","VE-W":"VARGAS","VE-X":"DELTA AMACURO","VE-Y":"AMAZONAS",
    "VE-Z":"CARACAS",
}
def pct_color(p):
    if p>=98: return "#059669"
    if p>=95: return "#10b981"
    if p>=90: return "#f59e0b"
    if p>0:   return "#ef4444"
    return "#1e3a5f"

svg_paths=[]
for vid,d in ve_paths.items():
    sname=state_id_map.get(vid,"")
    ed=sdmap.get(sname,{})
    p=ed.get("pct",0); t=ed.get("total",0)
    col=pct_color(p) if t>0 else "#1e3a5f"
    svg_paths.append(
        f'<path id="{vid}" class="ms" d="{d}" fill="{col}" stroke="#0f172a" stroke-width="0.8"'
        f' data-s="{sname}" data-p="{p}" data-t="{t}"'
        f' onmouseenter="hs(this,event)" onmouseleave="hu(this)" onclick="cs(this)"><title>{sname}: {p}% ({t})</title></path>'
    )

# Núcleo pins
coords={
    "CARACAS":(283,185),"SAN PEDRO":(279,192),"LOS TEQUES":(278,181),
    "GUARENAS":(294,181),"VALLES DEL TUY":(283,197),"MARACAY":(263,181),
    "MARACAY II":(266,185),"VALENCIA":(247,174),"BARQUISIMETO":(217,159),
    "SUCRE-CUMANÁ":(394,148),"CUMANÁ":(396,150),"SUCRE-CARÚPANO":(414,142),
    "MÉRIDA":(209,197),"MARACAIBO":(185,127),"MARACAIBO II":(188,133),
    "SAN CRISTÓBAL":(199,214),"MATURÍN":(430,167),"CIUDAD BOLÍVAR":(394,224),
    "BOLÍVAR-PTO.ORDAZ":(409,239),"PUERTO ORDAZ":(410,241),
    "BARCELONA":(379,154),"BARINAS":(236,195),"GUANARE":(229,169),
    "SAN JUAN DE LOS MORROS":(307,209),"CALABOZO":(314,219),
    "ACARIGUA":(231,164),"CORO":(206,142),"PUNTO FIJO":(199,137),
    "SAN FELIPE":(224,157),"TURMERO":(266,176),"GUARICO":(314,220),
    "TRUJILLO":(212,164),"VALERA":(213,166),"LA GUAIRA":(282,171),
    "VARGAS":(282,171),"TUCUPITA":(454,219),"PRUEBA LR":(217,159),
}
nucleo_pins=[]
for n in nucleos_list:
    name=n["nucleo"]
    coord=None
    for k,v in coords.items():
        if k in name or name in k:
            coord=v; break
    if not coord: coord=(300,250)
    x,y=coord
    col=pct_color(n["pct"])
    nucleo_pins.append(
        f'<circle class="np" cx="{x}" cy="{y}" r="4.5" fill="{col}" stroke="#fff" stroke-width="1.2"'
        f' data-n="{name}" data-p="{n["pct"]}" data-t="{n["total"]}"'
        f' onmouseenter="hn(this,event)" onmouseleave="hu(this)" onclick="cn(this)"><title>{name}: {n["pct"]}% ({n["total"]})</title></circle>'
    )

svg_str="\n".join(svg_paths)
pins_str="\n".join(nucleo_pins)

# ── JSON para JS ───────────────────────────────────────────────────────────────
est_json     = json.dumps(est_all,         ensure_ascii=False)
nucleos_json = json.dumps(nucleos_list,    ensure_ascii=False)
pnf_json     = json.dumps(pnf_list,        ensure_ascii=False)
tray_json    = json.dumps(trayecto_list,   ensure_ascii=False)
estado_json  = json.dumps(list(sdmap.values()), ensure_ascii=False)

# ── HTML ───────────────────────────────────────────────────────────────────────
html=f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UNES · EPA 2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0f172a;--sur:#1e293b;--sur2:#263347;--brd:#334155;
  --tx:#f1f5f9;--tx2:#94a3b8;--tx3:#64748b;
  --acc:#3b82f6;--acc2:#1d4ed8;
  --grn:#059669;--grn2:#10b981;--amb:#f59e0b;--red:#ef4444;
  --sw:240px;
}}
html,body{{height:100%;background:var(--bg);color:var(--tx);font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;line-height:1.5;overflow:hidden}}
#app{{display:flex;height:100vh}}

/* SIDEBAR */
#sb{{width:var(--sw);min-width:var(--sw);background:#09111e;border-right:1px solid var(--brd);display:flex;flex-direction:column}}
.sb-logo{{padding:18px 16px;border-bottom:1px solid var(--brd);display:flex;align-items:center;gap:10px}}
.sb-icon{{width:34px;height:34px;background:var(--red);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:15px;color:#fff;flex-shrink:0}}
.sb-name{{font-weight:800;font-size:14px}}.sb-sub{{font-size:10px;color:var(--tx3)}}
nav{{flex:1;padding:10px 8px;overflow-y:auto}}
.ni{{display:flex;align-items:center;gap:9px;padding:9px 10px;border-radius:8px;cursor:pointer;color:var(--tx2);font-size:13px;transition:all .15s;user-select:none}}
.ni:hover{{background:var(--sur2);color:var(--tx)}}
.ni.active{{background:var(--acc2);color:#fff;font-weight:600}}
.ni svg{{width:17px;height:17px;flex-shrink:0}}
.sb-foot{{padding:14px 16px;border-top:1px solid var(--brd);font-size:11px;color:var(--tx3)}}

/* MAIN */
#main{{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}}
#topbar{{display:flex;align-items:center;gap:10px;padding:0 18px;height:52px;min-height:52px;background:var(--sur);border-bottom:1px solid var(--brd);flex-shrink:0}}
#topbar h1{{font-size:16px;font-weight:700;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.chip{{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600;white-space:nowrap}}
.chip-g{{background:#065f46;color:#6ee7b7}}.chip-b{{background:#1e3a5f;color:#93c5fd}}
.btn-exp{{display:flex;align-items:center;gap:5px;padding:5px 12px;background:transparent;border:1px solid var(--brd);border-radius:7px;color:var(--tx2);font-size:12px;font-weight:600;cursor:pointer;transition:all .2s}}
.btn-exp:hover{{border-color:var(--acc);color:var(--tx)}}
#content{{flex:1;overflow-y:auto;padding:18px}}
.view{{display:none}}.view.active{{display:flex;flex-direction:column;gap:16px}}

/* KPI ROW */
.kpi-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;flex-shrink:0}}
.kc{{background:var(--sur);border:1px solid var(--brd);border-radius:11px;overflow:hidden}}
.kc-top{{height:3px}}.kc-body{{padding:14px 16px}}
.kc-lbl{{font-size:10px;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px}}
.kc-val{{font-size:28px;font-weight:800;line-height:1;margin-bottom:3px}}
.kc-sub{{font-size:11px;color:var(--tx3)}}

/* MAPA CARD */
.map-card{{background:var(--sur);border:1px solid var(--brd);border-radius:11px;overflow:hidden;display:flex;flex-direction:column;flex:1;min-height:0}}
.map-card-hdr{{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--brd);flex-shrink:0}}
.mc-title{{font-size:13px;font-weight:700}}.mc-sub{{font-size:10px;color:var(--tx3);margin-top:1px}}
.map-toggle{{display:flex;border:1px solid var(--brd);border-radius:7px;overflow:hidden}}
.map-toggle button{{padding:5px 12px;font-size:11px;font-weight:600;color:var(--tx3);background:transparent;border:none;cursor:pointer;transition:all .15s}}
.map-toggle button.active{{background:var(--acc);color:#fff}}
.map-body{{display:grid;grid-template-columns:1fr 280px;flex:1;min-height:0;overflow:hidden}}
.map-svg-wrap{{position:relative;padding:12px;background:#0a1829;overflow:hidden;display:flex;align-items:center;justify-content:center}}
.ve-map{{width:100%;height:100%;object-fit:contain}}
.ms{{cursor:pointer;transition:filter .15s}}.ms:hover{{filter:brightness(1.4)}}
.np{{cursor:pointer;transition:all .15s}}.np:hover{{r:7;filter:brightness(1.3)}}
.map-legend{{display:flex;flex-wrap:wrap;gap:10px;padding:10px 16px;border-top:1px solid var(--brd);font-size:10px;flex-shrink:0}}
.li{{display:flex;align-items:center;gap:5px}}.ld{{width:9px;height:9px;border-radius:50%}}

/* DETALLE PANEL */
.det-panel{{background:var(--sur2);border-left:1px solid var(--brd);display:flex;flex-direction:column;overflow:hidden}}
.det-hdr{{padding:12px 14px;border-bottom:1px solid var(--brd);flex-shrink:0}}
.det-title{{font-size:13px;font-weight:700;margin-bottom:1px}}.det-sub{{font-size:10px;color:var(--tx3)}}
.det-body{{flex:1;overflow-y:auto;padding:12px 14px}}
.det-empty{{color:var(--tx3);font-size:12px;text-align:center;padding:24px 0}}
.srow{{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--brd);font-size:12px}}
.srow:last-of-type{{border-bottom:none}}
.srow-l{{color:var(--tx2)}}.srow-v{{font-weight:700;font-size:13px}}
.det-list-title{{font-size:9px;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.07em;margin:10px 0 5px}}
.dnitem{{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;margin:3px 0;background:var(--sur);border-radius:5px;font-size:11px}}
.dnpct{{font-weight:700;display:flex;align-items:center;gap:6px}}
.dnpct small{{color:var(--tx3);font-weight:400}}

/* REPORTES */
.rep-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.card{{background:var(--sur);border:1px solid var(--brd);border-radius:11px;overflow:hidden}}
.ch{{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--brd)}}
.ct{{font-size:13px;font-weight:700}}.cs{{font-size:10px;color:var(--tx3);margin-top:1px}}
.cb{{padding:14px}}
.chart-box{{position:relative;height:260px}}

/* TABLA */
.tbl-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
thead th{{padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid var(--brd);white-space:nowrap}}
tbody td{{padding:10px 12px;border-bottom:1px solid var(--brd)}}
tbody tr:hover{{background:var(--sur2)}}
tbody tr:last-child td{{border-bottom:none}}
.pbar{{height:18px;background:var(--brd);border-radius:4px;position:relative;overflow:hidden;min-width:60px}}
.pbar-fill{{position:absolute;top:0;left:0;height:100%;border-radius:4px}}
.pbar-lbl{{position:absolute;right:5px;top:50%;transform:translateY(-50%);font-size:10px;font-weight:700;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.6)}}
.rk{{display:inline-block;width:18px;height:18px;background:var(--sur2);border-radius:3px;text-align:center;line-height:18px;font-size:9px;font-weight:700;color:var(--tx3);margin-right:4px}}

/* ESTUDIANTES */
.fbar{{display:flex;flex-wrap:wrap;gap:8px;flex-shrink:0}}
.si{{flex:1;min-width:180px;padding:8px 12px;background:var(--sur);border:1px solid var(--brd);border-radius:7px;color:var(--tx);outline:none;font:inherit;font-size:12px}}
.si:focus{{border-color:var(--acc)}}
.sf{{padding:8px 12px;background:var(--sur);border:1px solid var(--brd);border-radius:7px;color:var(--tx);outline:none;font:inherit;font-size:12px}}
.pag{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;font-size:11px;color:var(--tx3);flex-shrink:0}}
.pbts{{display:flex;gap:5px}}
.pbt{{width:30px;height:30px;border-radius:6px;border:1px solid var(--brd);background:transparent;color:var(--tx2);font-size:11px;font-weight:600;cursor:pointer;transition:all .15s}}
.pbt:hover,.pbt.active{{background:var(--acc);border-color:var(--acc);color:#fff}}
.sb2{{display:inline-block;padding:3px 7px;border-radius:4px;font-size:10px;font-weight:700}}
.sa{{background:#065f46;color:#6ee7b7}}.sr{{background:#7f1d1d;color:#fca5a5}}

/* TOOLTIP */
#tt{{position:fixed;background:#1e293b;border:1px solid var(--brd);border-radius:8px;padding:9px 13px;font-size:11px;pointer-events:none;opacity:0;transition:opacity .12s;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.5);max-width:190px}}
#tt.show{{opacity:1}}
#tt b{{font-size:12px;display:block;margin-bottom:3px}}
#tt span{{color:var(--tx2)}}

/* SCROLLBAR */
::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-thumb{{background:var(--brd);border-radius:3px}}

/* NÚCLEOS CARDS */
.ng{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}}
.ncard{{background:var(--sur);border:1px solid var(--brd);border-radius:9px;padding:12px;transition:border-color .15s}}
.ncard:hover{{border-color:var(--acc)}}
.nh{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:7px}}
.nn{{font-size:12px;font-weight:700}}.ne{{font-size:10px;color:var(--tx3);margin-top:1px}}
.npct{{font-size:20px;font-weight:800}}
.nbar{{height:4px;background:var(--brd);border-radius:2px;margin-bottom:7px;overflow:hidden}}
.nbar-f{{height:100%;border-radius:2px}}
.nst{{display:flex;gap:10px;font-size:10px;color:var(--tx3)}}
.nst span{{color:var(--tx2);font-weight:600}}

@media(max-width:1000px){{
  .kpi-row{{grid-template-columns:1fr 1fr}}
  .map-body{{grid-template-columns:1fr}}
  .det-panel{{display:none}}
  .rep-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div id="tt"><b id="tt-t"></b><div><span id="tt-l"></span> <span id="tt-v" style="font-weight:700;color:var(--tx)"></span></div></div>
<div id="app">

<!-- SIDEBAR -->
<aside id="sb">
  <div class="sb-logo">
    <div class="sb-icon">U</div>
    <div><div class="sb-name">UNES · EPA</div><div class="sb-sub">Sistema de Evaluación 2026</div></div>
  </div>
  <nav>
    <div class="ni active" onclick="sv('dash')" data-v="dash">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Dashboard
    </div>
    <div class="ni" onclick="sv('nucleos')" data-v="nucleos">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.3 7 13 7 13s7-7.7 7-13c0-3.9-3.1-7-7-7zm0 9.5c-1.4 0-2.5-1.1-2.5-2.5S10.6 6.5 12 6.5s2.5 1.1 2.5 2.5S13.4 11.5 12 11.5z"/></svg>Núcleos
    </div>
    <div class="ni" onclick="sv('est')" data-v="est">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>Estudiantes
    </div>
    <div class="ni" onclick="sv('rep')" data-v="rep">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>Reportes
    </div>
  </nav>
  <div class="sb-foot">{total:,} estudiantes · {len(nd)} núcleos · {len(pd)} PNF</div>
</aside>

<!-- MAIN -->
<div id="main">
  <div id="topbar">
    <h1 id="tbtitle">Dashboard</h1>
    <span class="chip chip-g">● {total:,} Estudiantes</span>
    <span class="chip chip-b">Cohorte 2026</span>
    <button class="btn-exp" onclick="doExport()">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Exportar CSV
    </button>
  </div>

  <div id="content">

  <!-- ══ DASHBOARD ══════════════════════════════════════════════════════════ -->
  <div id="v-dash" class="view active">

    <!-- KPIs -->
    <div class="kpi-row">
      <div class="kc"><div class="kc-top" style="background:var(--acc)"></div><div class="kc-body">
        <div class="kc-lbl">Total Matriculados</div>
        <div class="kc-val" style="color:var(--acc)">{total:,}</div>
        <div class="kc-sub">EPA · Cohorte 2026</div>
      </div></div>
      <div class="kc"><div class="kc-top" style="background:var(--grn)"></div><div class="kc-body">
        <div class="kc-lbl">Aprobados</div>
        <div class="kc-val" style="color:var(--grn)">{aprobados:,}</div>
        <div class="kc-sub">{pct_apr}% del total</div>
      </div></div>
      <div class="kc"><div class="kc-top" style="background:var(--red)"></div><div class="kc-body">
        <div class="kc-lbl">Reprobados</div>
        <div class="kc-val" style="color:var(--red)">{reprobados:,}</div>
        <div class="kc-sub">{round(100-pct_apr,1)}% del total</div>
      </div></div>
      <div class="kc"><div class="kc-top" style="background:var(--amb)"></div><div class="kc-body">
        <div class="kc-lbl">Núcleos Activos</div>
        <div class="kc-val" style="color:var(--amb)">{len(nd)}</div>
        <div class="kc-sub">{len(pd)} PNF registrados</div>
      </div></div>
    </div>

    <!-- MAPA -->
    <div class="map-card">
      <div class="map-card-hdr">
        <div>
          <div class="mc-title">🗺️ Mapa Coroplético Vectorial — Núcleos UNES por Estado</div>
          <div class="mc-sub">Haz clic en un estado o pin para ver detalle</div>
        </div>
        <div class="map-toggle">
          <button class="active" id="btn-pct" onclick="setMode('pct')">% Éxito</button>
          <button id="btn-vol" onclick="setMode('vol')">Matrícula</button>
        </div>
      </div>
      <div class="map-body">
        <div class="map-svg-wrap">
          <svg class="ve-map" viewBox="0 0 600 527" xmlns="http://www.w3.org/2000/svg">
            <g id="states-g">
{svg_str}
            </g>
            <g id="pins-g">
{pins_str}
            </g>
          </svg>
        </div>
        <div class="det-panel">
          <div class="det-hdr">
            <div class="det-title" id="det-t">Selecciona un estado</div>
            <div class="det-sub" id="det-s">Clic en el mapa para ver información</div>
          </div>
          <div class="det-body" id="det-b">
            <div class="det-empty">Haz clic en cualquier estado o pin de núcleo para ver el detalle aquí.</div>
          </div>
        </div>
      </div>
      <div class="map-legend">
        <div class="li"><div class="ld" style="background:#059669"></div> ≥ 98%</div>
        <div class="li"><div class="ld" style="background:#10b981"></div> 95–97%</div>
        <div class="li"><div class="ld" style="background:#f59e0b"></div> 90–94%</div>
        <div class="li"><div class="ld" style="background:#ef4444"></div> &lt; 90%</div>
        <div class="li"><div class="ld" style="background:#1e3a5f"></div> Sin datos</div>
        <div class="li"><div class="ld" style="background:white;border:1px solid #334155"></div> Pin núcleo</div>
      </div>
    </div>
  </div>

  <!-- ══ NÚCLEOS ════════════════════════════════════════════════════════════ -->
  <div id="v-nucleos" class="view">
    <div class="card">
      <div class="ch"><div><div class="ct">📍 Todos los Núcleos UNES</div><div class="cs">{len(nd)} centros de formación · Cohorte 2026</div></div></div>
      <div class="cb">
        <div class="fbar" style="margin-bottom:12px">
          <input class="si" id="ns" placeholder="🔍 Buscar núcleo..." oninput="fNuc()">
          <select class="sf" id="nef" onchange="fNuc()"><option value="">Todos los estados</option></select>
        </div>
        <div class="ng" id="ng"></div>
      </div>
    </div>
  </div>

  <!-- ══ ESTUDIANTES ════════════════════════════════════════════════════════ -->
  <div id="v-est" class="view">
    <div class="card" style="flex:1;min-height:0;display:flex;flex-direction:column">
      <div class="ch"><div><div class="ct">👥 Estudiantes</div><div class="cs" id="eslbl">{total:,} registros</div></div></div>
      <div class="cb" style="display:flex;flex-direction:column;gap:10px;flex:1;min-height:0">
        <div class="fbar">
          <input class="si" id="esq" placeholder="🔍 Nombre, cédula o núcleo..." oninput="fEst()" style="flex:2;min-width:200px">
          <select class="sf" id="ese" onchange="fEst()"><option value="">Todos los estatus</option><option value="Aprobado">Aprobados</option><option value="Reprobado">Reprobados</option></select>
          <select class="sf" id="esp" onchange="fEst()"><option value="">Todos los PNF</option></select>
          <select class="sf" id="esn" onchange="fEst()"><option value="">Todos los núcleos</option></select>
        </div>
        <div class="tbl-wrap" style="flex:1;overflow-y:auto">
          <table>
            <thead><tr><th>#</th><th>Nombre</th><th>Cédula</th><th>Núcleo</th><th>PNF</th><th>Trayecto</th><th>Puntaje</th><th>Estatus</th></tr></thead>
            <tbody id="estb"></tbody>
          </table>
        </div>
        <div class="pag">
          <span id="pi">—</span>
          <div class="pbts" id="pb"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- ══ REPORTES ═══════════════════════════════════════════════════════════ -->
  <div id="v-rep" class="view">

    <div class="rep-grid">
      <!-- PNF Gráfica -->
      <div class="card">
        <div class="ch"><div><div class="ct">📊 Distribución por PNF</div><div class="cs">Programas Nacionales de Formación</div></div></div>
        <div class="cb"><div class="chart-box"><canvas id="cpnf"></canvas></div></div>
      </div>
      <!-- Trayecto -->
      <div class="card">
        <div class="ch"><div><div class="ct">🎓 Distribución por Trayecto</div><div class="cs">Cohorte 2026</div></div></div>
        <div class="cb"><div class="chart-box"><canvas id="ctray"></canvas></div></div>
      </div>
    </div>

    <!-- Tabla PNF -->
    <div class="card">
      <div class="ch"><div><div class="ct">📋 Resultados por PNF</div><div class="cs">{len(pnf_list)} programas</div></div></div>
      <div class="cb">
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>PNF</th><th style="text-align:center">Total</th><th style="text-align:center">Aprobados</th><th style="text-align:center">Reprobados</th><th style="min-width:100px">% Éxito</th></tr></thead>
            <tbody id="pnftb"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Tabla Núcleos -->
    <div class="card">
      <div class="ch">
        <div><div class="ct">🏫 Resultados por Núcleo</div><div class="cs">{len(nucleos_list)} núcleos · ordenados por matrícula</div></div>
        <div style="display:flex;gap:8px;align-items:center">
          <input class="si" id="nrep-s" placeholder="Buscar..." oninput="fRepNuc()" style="width:140px;padding:5px 10px;font-size:11px">
          <select class="sf" id="nrep-ord" onchange="fRepNuc()" style="font-size:11px;padding:5px 8px">
            <option value="total">Por matrícula</option>
            <option value="pct">Por % éxito</option>
            <option value="az">A → Z</option>
          </select>
        </div>
      </div>
      <div class="cb">
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>#</th><th>Núcleo</th><th>Estado</th><th style="text-align:center">Total</th><th style="text-align:center">Aprobados</th><th style="text-align:center">Reprobados</th><th style="min-width:100px">% Éxito</th></tr></thead>
            <tbody id="nucreptb"></tbody>
          </table>
        </div>
      </div>
    </div>

  </div><!-- /reportes -->

  </div><!-- /content -->
</div><!-- /main -->
</div><!-- /app -->

<script>
// DATA
const EST   = {est_json};
const NUCS  = {nucleos_json};
const PNFS  = {pnf_json};
const TRAYS = {tray_json};
const ESTDS = {estado_json};

// UTILS
const $ = id => document.getElementById(id);
const pc = p => p>=98?'#059669':p>=95?'#10b981':p>=90?'#f59e0b':p>0?'#ef4444':'#1e3a5f';
const fmt = n => n.toLocaleString('es-VE');

// TOOLTIP
const tt = $('tt');
document.addEventListener('mousemove', e => {{
  tt.style.left = (e.clientX+12)+'px';
  tt.style.top  = (e.clientY+12)+'px';
}});
function showTT(title,label,val) {{
  $('tt-t').textContent = title;
  $('tt-l').textContent = label+':';
  $('tt-v').textContent = val;
  tt.classList.add('show');
}}
function hideTT() {{ tt.classList.remove('show'); }}

// NAVIGATION
const TITLES = {{dash:'Dashboard',nucleos:'Núcleos UNES',est:'Estudiantes',rep:'Reportes'}};
let repInited=false;
function sv(id) {{
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.ni').forEach(n=>n.classList.remove('active'));
  $('v-'+id).classList.add('active');
  document.querySelectorAll(`[data-v="${{id}}"]`).forEach(n=>n.classList.add('active'));
  $('tbtitle').textContent = TITLES[id]||id;
  if(id==='nucleos') initNucs();
  if(id==='est')     initEst();
  if(id==='rep')     initRep();
}}

// MAPA
let mapMode='pct';
const eMap={{}};
ESTDS.forEach(e=>eMap[e.estado]=e);
const maxV=Math.max(...ESTDS.map(e=>e.total));
function vc(t){{const r=t/maxV;return r>.7?'#1d4ed8':r>.4?'#3b82f6':r>.15?'#60a5fa':r>0?'#bfdbfe':'#1e3a5f'}}
function setMode(m){{
  mapMode=m;
  $('btn-pct').classList.toggle('active',m==='pct');
  $('btn-vol').classList.toggle('active',m==='vol');
  document.querySelectorAll('.ms').forEach(el=>{{
    const ed=eMap[el.dataset.s]||{{}};
    const t=ed.total||0, p=ed.pct||0;
    el.setAttribute('fill',t===0?'#1e3a5f':(m==='pct'?pc(p):vc(t)));
  }});
}}
function hs(el,e){{
  el.style.filter='brightness(1.4)';
  const ed=eMap[el.dataset.s]||{{}};
  showTT(el.dataset.s||'Sin datos','Matrícula '+fmt(ed.total||0),+(ed.pct||0)+'% éxito');
}}
function hu(el){{el.style.filter='';hideTT()}}
function cs(el){{
  const s=el.dataset.s, ed=eMap[s]||{{}};
  $('det-t').textContent='📍 '+(s||'Sin datos');
  $('det-s').textContent='Estado';
  const nucls=NUCS.filter(n=>n.estado===s);
  let h=`
    <div class="srow"><span class="srow-l">Matrícula</span><span class="srow-v" style="color:var(--acc)">${{fmt(ed.total||0)}}</span></div>
    <div class="srow"><span class="srow-l">Aprobados</span><span class="srow-v" style="color:var(--grn)">${{fmt(ed.aprobados||0)}}</span></div>
    <div class="srow"><span class="srow-l">Reprobados</span><span class="srow-v" style="color:var(--red)">${{fmt((ed.total||0)-(ed.aprobados||0))}}</span></div>
    <div class="srow"><span class="srow-l">% Éxito</span><span class="srow-v" style="color:${{pc(ed.pct||0)}}">${{ed.pct||0}}%</span></div>
    <div class="det-list-title">Núcleos (${{nucls.length}})</div>
  `;
  nucls.forEach(n=>{{
    h+=`<div class="dnitem"><span>${{n.nucleo}}</span><span class="dnpct" style="color:${{pc(n.pct)}}">${{n.pct}}%<small>${{n.total}}</small></span></div>`;
  }});
  $('det-b').innerHTML=h;
}}
function hn(el,e){{
  el.setAttribute('r','7');
  showTT(el.dataset.n,'Matrícula '+el.dataset.t,el.dataset.p+'% éxito');
}}
function cn(el){{
  const nd=NUCS.find(n=>n.nucleo===el.dataset.n)||{{}};
  $('det-t').textContent='📌 '+el.dataset.n;
  $('det-s').textContent='Núcleo · '+(nd.estado||'');
  $('det-b').innerHTML=`
    <div class="srow"><span class="srow-l">Matrícula</span><span class="srow-v" style="color:var(--acc)">${{fmt(nd.total||0)}}</span></div>
    <div class="srow"><span class="srow-l">Aprobados</span><span class="srow-v" style="color:var(--grn)">${{fmt(nd.aprobados||0)}}</span></div>
    <div class="srow"><span class="srow-l">Reprobados</span><span class="srow-v" style="color:var(--red)">${{fmt((nd.total||0)-(nd.aprobados||0))}}</span></div>
    <div class="srow"><span class="srow-l">% Éxito</span><span class="srow-v" style="color:${{pc(nd.pct||0)}}">${{nd.pct||0}}%</span></div>
  `;
}}

// NÚCLEOS VIEW
let nucsInited=false;
function initNucs(){{
  if(nucsInited)return; nucsInited=true;
  const ests=[...new Set(NUCS.map(n=>n.estado))].sort();
  const sel=$('nef');
  ests.forEach(e=>sel.appendChild(new Option(e,e)));
  renderNucs(NUCS);
}}
function fNuc(){{
  const q=$('ns').value.toLowerCase(), e=$('nef').value;
  renderNucs(NUCS.filter(n=>(!q||n.nucleo.toLowerCase().includes(q))&&(!e||n.estado===e)));
}}
function renderNucs(list){{
  $('ng').innerHTML=list.length?list.map(n=>`
    <div class="ncard">
      <div class="nh">
        <div><div class="nn">${{n.nucleo}}</div><div class="ne">${{n.estado}}</div></div>
        <div class="npct" style="color:${{pc(n.pct)}}">${{n.pct}}%</div>
      </div>
      <div class="nbar"><div class="nbar-f" style="width:${{n.pct}}%;background:${{pc(n.pct)}}"></div></div>
      <div class="nst">
        <div>Total: <span>${{fmt(n.total)}}</span></div>
        <div>✅ <span>${{n.aprobados}}</span></div>
        <div>❌ <span>${{n.total-n.aprobados}}</span></div>
      </div>
    </div>`).join(''):'<p style="color:var(--tx3)">Sin resultados</p>';
}}

// ESTUDIANTES VIEW
let estInited=false, ePage=1, eFiltered=EST;
const PS=50;
function initEst(){{
  if(estInited)return; estInited=true;
  const pnfs=[...new Set(EST.map(e=>e.pnf))].sort(), sp=$('esp');
  pnfs.forEach(p=>sp.appendChild(new Option(p,p)));
  const nucs=[...new Set(EST.map(e=>e.nucleo))].sort(), sn=$('esn');
  nucs.forEach(n=>sn.appendChild(new Option(n,n)));
  renderEst();
}}
function fEst(){{
  const q=$('esq').value.toLowerCase(), est=$('ese').value, pnf=$('esp').value, nuc=$('esn').value;
  eFiltered=EST.filter(e=>
    (!q||e.nombre.toLowerCase().includes(q)||(e.cedula||'').toLowerCase().includes(q)||(e.nucleo||'').toLowerCase().includes(q))&&
    (!est||e.estatus===est)&&(!pnf||e.pnf===pnf)&&(!nuc||e.nucleo===nuc)
  );
  ePage=1; renderEst();
}}
function renderEst(){{
  const s=(ePage-1)*PS, sl=eFiltered.slice(s,s+PS);
  $('estb').innerHTML=sl.map((e,i)=>`
    <tr>
      <td style="color:var(--tx3)">${{s+i+1}}</td>
      <td>${{e.nombre}}</td><td style="color:var(--tx3)">${{e.cedula}}</td>
      <td>${{e.nucleo}}</td><td style="font-size:11px">${{e.pnf}}</td>
      <td>${{e.trayecto}}</td>
      <td style="text-align:right">${{e.puntaje??'—'}}</td>
      <td><span class="sb2 ${{e.estatus==='Aprobado'?'sa':'sr'}}">${{e.estatus}}</span></td>
    </tr>`).join('');
  $('eslbl').textContent=fmt(eFiltered.length)+' registros';
  $('pi').textContent='Mostrando '+(s+1)+'–'+Math.min(s+PS,eFiltered.length)+' de '+fmt(eFiltered.length);
  const tp=Math.ceil(eFiltered.length/PS);
  let pg=[]; if(tp<=7){{for(let i=1;i<=tp;i++)pg.push(i)}}else{{pg=[1];if(ePage>3)pg.push('…');for(let i=Math.max(2,ePage-1);i<=Math.min(tp-1,ePage+1);i++)pg.push(i);if(ePage<tp-2)pg.push('…');pg.push(tp)}}
  $('pb').innerHTML=pg.map(p=>p==='…'?'<span style="padding:0 3px;color:var(--tx3)">…</span>':`<button class="pbt ${{p===ePage?'active':''}}" onclick="gp(${{p}})">${{p}}</button>`).join('');
}}
function gp(p){{ePage=p;renderEst();}}

// REPORTES
const COLS=['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316'];
function initRep(){{
  if(repInited)return; repInited=true;
  // PNF Chart
  new Chart($('cpnf'),{{
    type:'bar',
    data:{{labels:PNFS.map(p=>p.pnf),datasets:[{{label:'Estudiantes',data:PNFS.map(p=>p.total),backgroundColor:COLS,borderRadius:5,borderSkipped:false}}]}},
    options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
      scales:{{x:{{grid:{{color:'#1e293b'}},ticks:{{color:'#94a3b8'}}}},y:{{grid:{{display:false}},ticks:{{color:'#e2e8f0',font:{{size:11}}}}}}}}
    }}
  }});
  // Trayecto Chart
  new Chart($('ctray'),{{
    type:'doughnut',
    data:{{labels:TRAYS.map(t=>t[0]),datasets:[{{data:TRAYS.map(t=>t[1]),backgroundColor:COLS,borderColor:'#0f172a',borderWidth:3,hoverOffset:8}}]}},
    options:{{responsive:true,maintainAspectRatio:false,cutout:'62%',
      plugins:{{legend:{{position:'right',labels:{{color:'#94a3b8',boxWidth:10,font:{{size:11}}}}}}}}
    }}
  }});
  // Tabla PNF
  $('pnftb').innerHTML=PNFS.map((p,i)=>`
    <tr>
      <td><span class="rk">${{i+1}}</span>${{p.pnf}}</td>
      <td style="text-align:center;font-weight:700">${{fmt(p.total)}}</td>
      <td style="text-align:center;color:var(--grn2)">${{fmt(p.aprobados)}}</td>
      <td style="text-align:center;color:var(--red)">${{p.total-p.aprobados}}</td>
      <td><div class="pbar"><div class="pbar-fill" style="width:${{p.pct}}%;background:${{pc(p.pct)}}"></div><span class="pbar-lbl">${{p.pct}}%</span></div></td>
    </tr>`).join('');
  renderRepNuc(NUCS);
}}
function fRepNuc(){{
  const q=$('nrep-s').value.toLowerCase(), ord=$('nrep-ord').value;
  let list=NUCS.filter(n=>!q||n.nucleo.toLowerCase().includes(q)||n.estado.toLowerCase().includes(q));
  if(ord==='pct') list=[...list].sort((a,b)=>b.pct-a.pct);
  else if(ord==='az') list=[...list].sort((a,b)=>a.nucleo.localeCompare(b.nucleo));
  renderRepNuc(list);
}}
function renderRepNuc(list){{
  $('nucreptb').innerHTML=list.map((n,i)=>`
    <tr>
      <td style="color:var(--tx3)">${{i+1}}</td>
      <td style="font-weight:600">${{n.nucleo}}</td>
      <td style="color:var(--tx2)">${{n.estado}}</td>
      <td style="text-align:center;font-weight:700">${{fmt(n.total)}}</td>
      <td style="text-align:center;color:var(--grn2)">${{n.aprobados}}</td>
      <td style="text-align:center;color:var(--red)">${{n.total-n.aprobados}}</td>
      <td><div class="pbar"><div class="pbar-fill" style="width:${{n.pct}}%;background:${{pc(n.pct)}}"></div><span class="pbar-lbl">${{n.pct}}%</span></div></td>
    </tr>`).join('');
}}

// EXPORT
function doExport(){{
  const rows=[['Nombre','Cedula','Nucleo','Estado','PNF','Trayecto','Puntaje','Estatus']];
  eFiltered.forEach(e=>rows.push([e.nombre,e.cedula,e.nucleo,e.estado,e.pnf,e.trayecto,e.puntaje??'',e.estatus]));
  const csv=rows.map(r=>r.map(v=>'"'+(v??'')+'"').join(',')).join('\\n');
  const a=document.createElement('a');
  a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);
  a.download='unes_epa_2026.csv'; a.click();
}}

document.addEventListener('DOMContentLoaded',()=>{{ /* charts lazy */ }});
</script>
</body>
</html>"""

out=os.path.join(BASE,"index.html")
with open(out,"w",encoding="utf-8") as f:
    f.write(html)
size=os.path.getsize(out)
print(f"OK index.html: {size:,} bytes ({size//1024} KB)")
print(f"Estudiantes: {total} | Aprobados: {aprobados} ({pct_apr}%) | Reprobados: {reprobados}")
print(f"Nucleos: {len(nd)} | PNF: {len(pd)} | Estados SVG: {len(ve_paths)}")
