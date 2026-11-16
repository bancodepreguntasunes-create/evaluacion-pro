# -*- coding: utf-8 -*-
"""
Genera el sistema UNES completo en UN SOLO ARCHIVO HTML autocontenido.
Dashboard limpio, funcional, con mapa coroplético real, gráficos y tabla.
"""
import json, os, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

# ── Cargar datos ────────────────────────────────────────────────────────────
with open(os.path.join(BASE_DIR, "datos_importados.json"), "r", encoding="utf-8") as f:
    raw = json.load(f)
est_data = raw["estudiantes"]

with open(os.path.join(BASE_DIR, "ve_paths.json"), "r", encoding="utf-8") as f:
    ve_paths = json.load(f)

# ── Centroides de etiquetas ─────────────────────────────────────────────────
CENTROIDES = {
    "VE-A": (291, 92,  "D.C."),
    "VE-B": (395, 175, "Anzoátegui"),
    "VE-C": (220, 295, "Apure"),
    "VE-D": (265, 118, "Aragua"),
    "VE-E": (170, 230, "Barinas"),
    "VE-F": (430, 320, "Bolívar"),
    "VE-G": (242, 110, "Carabobo"),
    "VE-H": (230, 178, "Cojedes"),
    "VE-I": (192, 72,  "Falcón"),
    "VE-J": (308, 208, "Guárico"),
    "VE-K": (175, 142, "Lara"),
    "VE-L": (130, 218, "Mérida"),
    "VE-M": (318, 110, "Miranda"),
    "VE-N": (452, 185, "Monagas"),
    "VE-O": (533, 95,  "Nva. Esparta"),
    "VE-P": (196, 185, "Portuguesa"),
    "VE-R": (460, 140, "Sucre"),
    "VE-S": (93,  252, "Táchira"),
    "VE-T": (148, 178, "Trujillo"),
    "VE-U": (220, 118, "Yaracuy"),
    "VE-V": (88,  132, "Zulia"),
    "VE-W": (280, 420, "Amazonas"),
    "VE-X": (288, 82,  "La Guaira"),
    "VE-Y": (533, 215, "Delta Amacuro"),
}

# ── Coordenadas de núcleos en el SVG ────────────────────────────────────────
NUCLEOS_GEO = {
    "SUCRE - CUMANÁ":    (425, 138),
    "SUCRE - CARÚPANO":  (452, 128),
    "CARACAS":           (288, 92),
    "MÉRIDA":            (130, 212),
    "BOLÍVAR - PTO. ORDAZ": (458, 240),
    "BOLÍVAR - ANGOSTURA":  (408, 230),
    "PORTUGUESA":        (196, 182),
    "BARLOVENTO":        (328, 112),
    "VALLES DEL TUY":    (300, 118),
    "GUARENAS - GUATIRE":(308, 100),
    "ALTOS MIRANDINOS":  (282, 104),
    "EJE METROPOLITANO": (294, 94),
    "ZULIA":             (88, 128),
    "MONAGAS":           (448, 180),
    "BARINAS":           (168, 228),
    "FALCÓN":            (192, 68),
    "AMAZONAS":          (268, 415),
    "ANZOÁTEGUI":        (382, 172),
    "TRUJILLO":          (148, 172),
    "EL LLANITO":        (294, 90),
    "CAFETAL":           (292, 96),
    "CARABOBO":          (242, 108),
    "APURE":             (218, 268),
    "LA GUAIRA":         (288, 80),
    "NUEVA ESPARTA":     (530, 92),
    "TÁCHIRA":           (93, 248),
    "DELTA AMACURO":     (520, 198),
    "POLICARACAS":       (285, 94),
    "SAN PEDRO":         (287, 88),
    "POLISUCRE":         (291, 88),
    "YARACUY":           (218, 116),
    "EL JUNQUITO":       (280, 93),
    "COJEDES":           (228, 174),
    "LARA":              (175, 138),
}

# ── Serializar datos en JSON para embeber en JS ─────────────────────────────
est_json = json.dumps(est_data, ensure_ascii=False, separators=(',', ':'))
nucleos_geo_json = json.dumps(NUCLEOS_GEO, ensure_ascii=False, separators=(',', ':'))

# ── Construir SVG de Venezuela ──────────────────────────────────────────────
svg_paths_parts = []
for pid, pdata in ve_paths.items():
    estado = pdata["estado"]
    d = pdata["d"]
    cx, cy, label = CENTROIDES.get(pid, (300, 250, estado[:8]))
    svg_paths_parts.append(
        f'<path id="map-{pid}" class="map-state" data-estado="{estado}" '
        f'd="{d}" onclick="clickEstado(\'{estado}\')" '
        f'onmouseenter="hoverEstado(\'{estado}\',event)" onmouseleave="hideTooltip()"/>'
    )
    svg_paths_parts.append(
        f'<text class="map-lbl" x="{cx}" y="{cy}" onclick="clickEstado(\'{estado}\')">'
        f'{label}</text>'
    )
svg_paths_str = "\n".join(svg_paths_parts)

print("SVG paths generated:", len(ve_paths))
print("Building HTML...")

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UNES · Sistema EPA 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
/* ── RESET & BASE ─────────────────────────────────────────── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;background:#f1f5f9;color:#1e293b;min-height:100vh;display:flex}}

/* ── SIDEBAR ─────────────────────────────────────────────── */
.sidebar{{width:220px;background:#0f172a;display:flex;flex-direction:column;flex-shrink:0;position:fixed;top:0;left:0;height:100vh;z-index:200}}
.sidebar-logo{{padding:20px 18px 14px;border-bottom:1px solid rgba(255,255,255,0.08)}}
.sidebar-logo img{{height:32px;filter:brightness(0) invert(1)}}
.sidebar-logo span{{font-size:11px;color:#94a3b8;display:block;margin-top:4px;letter-spacing:0.5px}}
.nav-links{{padding:12px 0;flex:1;overflow-y:auto}}
.nav-item{{display:flex;align-items:center;gap:10px;padding:10px 18px;cursor:pointer;color:#94a3b8;font-size:13.5px;font-weight:500;transition:all 0.15s;border-left:3px solid transparent;text-decoration:none}}
.nav-item:hover{{background:rgba(255,255,255,0.06);color:#e2e8f0}}
.nav-item.active{{background:rgba(220,38,38,0.15);color:#fca5a5;border-left-color:#dc2626;font-weight:700}}
.nav-item svg{{width:17px;height:17px;flex-shrink:0}}
.sidebar-footer{{padding:14px 18px;border-top:1px solid rgba(255,255,255,0.08);font-size:11px;color:#475569}}

/* ── MAIN ────────────────────────────────────────────────── */
.main{{margin-left:220px;flex:1;display:flex;flex-direction:column;min-height:100vh}}

/* ── TOPBAR ──────────────────────────────────────────────── */
.topbar{{background:#ffffff;border-bottom:1px solid #e2e8f0;padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 1px 3px rgba(0,0,0,0.05)}}
.topbar-title{{font-size:16px;font-weight:700;color:#0f172a}}
.topbar-right{{display:flex;align-items:center;gap:10px}}
.badge-live{{display:flex;align-items:center;gap:6px;background:#ecfdf5;border:1px solid #bbf7d0;border-radius:20px;padding:5px 12px;font-size:12px;font-weight:700;color:#15803d}}
.dot-green{{width:7px;height:7px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 2s ease-in-out infinite}}
@keyframes blink{{0%,100%{{opacity:1}} 50%{{opacity:0.4}}}}
.btn-sync{{background:#dc2626;color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:12.5px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;font-family:'Inter',sans-serif;transition:background 0.2s}}
.btn-sync:hover{{background:#b91c1c}}
.logo-img{{height:28px}}

/* ── CONTENT ─────────────────────────────────────────────── */
.content{{padding:20px 24px;flex:1;overflow-y:auto}}

/* ── VIEWS ───────────────────────────────────────────────── */
.view{{display:none}}
.view.active{{display:block}}

/* ── KPI CARDS ───────────────────────────────────────────── */
.kpi-row{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:20px}}
@media(max-width:1280px){{.kpi-row{{grid-template-columns:repeat(3,1fr)}}}}
@media(max-width:768px){{.kpi-row{{grid-template-columns:repeat(2,1fr)}}}}

.kpi-card{{background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;position:relative;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.04);transition:transform 0.2s,box-shadow 0.2s}}
.kpi-card:hover{{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,0.08)}}
.kpi-top-bar{{position:absolute;top:0;left:0;right:0;height:3px;border-radius:12px 12px 0 0}}
.kpi-icon{{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;margin-bottom:12px}}
.kpi-icon svg{{width:19px;height:19px}}
.kpi-value{{font-size:26px;font-weight:800;line-height:1;margin-bottom:4px}}
.kpi-label{{font-size:12px;font-weight:600;color:#64748b}}
.kpi-sub{{font-size:11px;color:#94a3b8;margin-top:3px}}
.kpi-bar-bg{{height:4px;background:#f1f5f9;border-radius:4px;margin-top:10px;overflow:hidden}}
.kpi-bar-fill{{height:4px;border-radius:4px;transition:width 0.8s ease}}

/* ── SECTION CARD ────────────────────────────────────────── */
.section-card{{background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.04);margin-bottom:20px}}
.section-header{{padding:14px 20px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;justify-content:space-between}}
.section-header h2{{font-size:14px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:8px}}
.section-header p{{font-size:11.5px;color:#94a3b8;margin-top:1px}}
.section-body{{padding:16px 20px}}

/* ── MAP + PANEL ──────────────────────────────────────────── */
.map-grid{{display:grid;grid-template-columns:1fr 280px;gap:16px}}
@media(max-width:1024px){{.map-grid{{grid-template-columns:1fr}}}}

.map-wrap{{background:#d6eaf8;border-radius:10px;overflow:hidden;position:relative;min-height:340px}}
.map-wrap svg{{display:block;width:100%;height:auto}}

.map-state{{fill:#93c5fd;stroke:#fff;stroke-width:0.8;cursor:pointer;transition:fill 0.3s,stroke 0.2s,stroke-width 0.2s}}
.map-state:hover{{stroke:#1e3a8a;stroke-width:1.8;filter:brightness(1.08)}}
.map-state.state-selected{{stroke:#0f172a;stroke-width:2.5;filter:drop-shadow(0 0 6px rgba(0,0,0,0.3))}}
.map-state.state-dimmed{{opacity:0.45}}
.map-lbl{{font-family:'Inter',sans-serif;font-size:7px;font-weight:700;fill:#1e3a8a;pointer-events:none;text-anchor:middle;dominant-baseline:middle;user-select:none}}

/* Escala coroplética */
.c-none{{fill:#dbeafe}}
.c-low{{fill:#fca5a5}}
.c-warn{{fill:#fcd34d}}
.c-ok{{fill:#6ee7b7}}
.c-hi{{fill:#059669}}

/* Pines de núcleos */
.nucleo-pin{{cursor:pointer;transition:transform 0.2s}}
.nucleo-pin:hover{{transform:scale(1.5)}}
.nucleo-pin circle.ring{{transform-origin:center;transform-box:fill-box;animation:pin-pulse 2s ease-out infinite;fill:#800020;opacity:0.3}}
@keyframes pin-pulse{{0%{{r:6;opacity:0.4}} 70%{{r:14;opacity:0}} 100%{{r:14;opacity:0}}}}
.nucleo-pin circle.dot{{fill:#800020;stroke:#fff;stroke-width:1.5}}

/* Panel lateral del mapa */
.map-panel{{border:1px solid #e2e8f0;border-radius:10px;padding:16px;min-height:340px;background:#ffffff}}
.map-panel-placeholder{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;color:#94a3b8;gap:10px}}
.map-panel-placeholder svg{{width:40px;height:40px;opacity:0.4}}
.map-panel-placeholder p{{font-size:12.5px;line-height:1.5}}

.panel-nucleo-title{{font-size:16px;font-weight:800;color:#0f172a;margin-bottom:3px}}
.panel-nucleo-sub{{font-size:12px;color:#64748b;margin-bottom:14px}}
.panel-stat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px}}
.panel-stat{{border-radius:9px;padding:10px;text-align:center}}
.panel-stat-val{{font-size:20px;font-weight:800}}
.panel-stat-lbl{{font-size:11px;font-weight:600;margin-top:2px}}
.panel-pbar-bg{{height:5px;background:#f1f5f9;border-radius:5px;margin:10px 0}}
.panel-pbar-fill{{height:5px;border-radius:5px}}
.pnf-row{{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px dashed #f1f5f9;font-size:12px}}
.pnf-row:last-child{{border-bottom:none}}
.btn-filtrar{{width:100%;margin-top:14px;background:#0f172a;color:#fff;border:none;border-radius:8px;padding:9px;font-size:12.5px;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif;transition:background 0.2s}}
.btn-filtrar:hover{{background:#1e293b}}
.btn-cerrar-panel{{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:11px;font-family:'Inter',sans-serif}}

/* ── MAP LEGEND ───────────────────────────────────────────── */
.map-legend{{display:flex;align-items:center;gap:14px;padding:10px 20px;border-top:1px solid #f1f5f9;flex-wrap:wrap}}
.legend-item{{display:flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#475569}}
.legend-swatch{{width:14px;height:14px;border-radius:3px;border:1px solid rgba(0,0,0,0.1)}}
.legend-pin{{width:9px;height:9px;border-radius:50%;background:#800020;border:2px solid #fff;box-shadow:0 0 0 1px #800020}}

/* ── CHARTS GRID ──────────────────────────────────────────── */
.charts-row{{display:grid;grid-template-columns:1.6fr 1fr;gap:14px;margin-bottom:20px}}
@media(max-width:1024px){{.charts-row{{grid-template-columns:1fr}}}}
.chart-wrap{{position:relative;height:260px}}

/* ── MAP CONTROLS ─────────────────────────────────────────── */
.mode-toggle{{display:flex;background:#f8fafc;border:1px solid #e2e8f0;border-radius:7px;padding:2px}}
.mode-btn{{border:none;background:transparent;padding:5px 11px;font-size:11.5px;font-weight:600;color:#64748b;border-radius:5px;cursor:pointer;font-family:'Inter',sans-serif;transition:all 0.2s}}
.mode-btn.active{{background:#ffffff;color:#dc2626;box-shadow:0 1px 3px rgba(0,0,0,0.1)}}
.map-select{{border:1px solid #e2e8f0;border-radius:7px;padding:5px 10px;font-size:12px;font-family:'Inter',sans-serif;color:#334155;background:#fff;cursor:pointer;outline:none}}
.map-select:focus{{border-color:#94a3b8}}

/* ── TABLE ────────────────────────────────────────────────── */
.data-table{{width:100%;border-collapse:collapse;font-size:13px}}
.data-table th{{background:#f8fafc;padding:10px 14px;text-align:left;font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.4px;border-bottom:1px solid #e2e8f0;white-space:nowrap;cursor:pointer}}
.data-table th:hover{{background:#f1f5f9;color:#334155}}
.data-table td{{padding:10px 14px;border-bottom:1px solid #f8fafc;color:#334155}}
.data-table tr:hover td{{background:#fafafa}}
.pct-bar{{display:flex;align-items:center;gap:8px}}
.pct-bar-bg{{flex:1;height:5px;background:#f1f5f9;border-radius:5px;overflow:hidden}}
.pct-bar-fill{{height:5px;border-radius:5px}}
.badge{{display:inline-flex;align-items:center;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:700}}
.badge-green{{background:#ecfdf5;color:#15803d}}
.badge-red{{background:#fef2f2;color:#b91c1c}}

/* ── FILTER BAR ───────────────────────────────────────────── */
.filter-bar{{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}}
.filter-bar input, .filter-bar select{{border:1px solid #e2e8f0;border-radius:8px;padding:8px 12px;font-size:13px;font-family:'Inter',sans-serif;color:#334155;outline:none;background:#fff;transition:border-color 0.2s}}
.filter-bar input:focus, .filter-bar select:focus{{border-color:#94a3b8}}
.filter-bar input{{flex:1;min-width:200px}}

/* ── PAGINATION ───────────────────────────────────────────── */
.pagination{{display:flex;align-items:center;gap:8px;justify-content:center;margin-top:14px}}
.page-btn{{border:1px solid #e2e8f0;background:#fff;border-radius:7px;padding:6px 12px;font-size:13px;font-weight:600;color:#334155;cursor:pointer;font-family:'Inter',sans-serif;transition:all 0.2s}}
.page-btn:hover{{background:#f8fafc}}
.page-btn.active{{background:#0f172a;color:#fff;border-color:#0f172a}}
.page-info{{font-size:12px;color:#64748b}}

/* ── TOOLTIP ──────────────────────────────────────────────── */
#tip{{display:none;position:fixed;background:#0f172a;color:#fff;font-family:'Inter',sans-serif;font-size:12px;line-height:1.6;padding:9px 13px;border-radius:9px;pointer-events:none;z-index:9999;max-width:200px;box-shadow:0 8px 20px rgba(0,0,0,0.3)}}

/* ── TOAST ────────────────────────────────────────────────── */
#toast{{position:fixed;bottom:24px;right:24px;background:#0f172a;color:#fff;padding:12px 20px;border-radius:10px;font-size:13px;font-weight:600;box-shadow:0 10px 25px rgba(0,0,0,0.3);z-index:99999;opacity:0;transform:translateY(20px);transition:all 0.3s;pointer-events:none}}
#toast.show{{opacity:1;transform:translateY(0)}}

/* ── MOBILE ───────────────────────────────────────────────── */
@media(max-width:768px){{
  .sidebar{{transform:translateX(-220px);transition:transform 0.3s}}
  .sidebar.open{{transform:translateX(0)}}
  .main{{margin-left:0}}
  .topbar{{padding:0 14px}}
  .content{{padding:14px}}
  .charts-row{{grid-template-columns:1fr}}
  .map-grid{{grid-template-columns:1fr}}
  .kpi-row{{grid-template-columns:repeat(2,1fr)}}
  .menu-btn{{display:flex}}
  .topbar-title{{font-size:14px}}
}}
.menu-btn{{display:none;background:none;border:none;cursor:pointer;padding:6px;color:#334155;align-items:center}}
.menu-btn svg{{width:22px;height:22px}}
</style>
</head>
<body>

<!-- Sidebar -->
<nav class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <img src="descarga.png" alt="UNES" onerror="this.style.display='none';document.getElementById('logoTxt').style.display='block'">
    <span id="logoTxt" style="display:none;font-size:18px;font-weight:800;color:#fff;margin-top:0">UNES</span>
    <span>Sistema EPA 2026</span>
  </div>
  <div class="nav-links">
    <a class="nav-item active" id="nav-dashboard" onclick="showView('dashboard')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
      Dashboard
    </a>
    <a class="nav-item" id="nav-nucleos" onclick="showView('nucleos')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Núcleos
    </a>
    <a class="nav-item" id="nav-estudiantes" onclick="showView('estudiantes')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
      Estudiantes
    </a>
  </div>
  <div class="sidebar-footer">v10.5 · 6.070 registros</div>
</nav>

<!-- Main -->
<div class="main">
  <!-- Topbar -->
  <header class="topbar">
    <div style="display:flex;align-items:center;gap:12px">
      <button class="menu-btn" onclick="document.getElementById('sidebar').classList.toggle('open')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <span class="topbar-title" id="topbarTitle">Dashboard General</span>
    </div>
    <div class="topbar-right">
      <div class="badge-live"><span class="dot-green"></span><span id="badgeTotal">6.070 Estudiantes</span></div>
      <button class="btn-sync" onclick="sincronizar()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0118.8-4.3M22 12.5a10 10 0 01-18.8 4.2"/></svg>
        Sincronizar
      </button>
      <img src="descarga.png" class="logo-img" onerror="this.style.display='none'">
    </div>
  </header>

  <!-- Content -->
  <div class="content">

    <!-- ===== DASHBOARD ===== -->
    <div class="view active" id="view-dashboard">

      <!-- KPI Cards -->
      <div class="kpi-row" id="kpiRow"></div>

      <!-- Mapa + Panel -->
      <div class="section-card">
        <div class="section-header">
          <div>
            <h2>🗺️ Mapa Coroplético Nacional · Resultados por Estado y Núcleo UNES</h2>
            <p>Haz clic en un estado o en un núcleo para ver su detalle</p>
          </div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
            <select class="map-select" id="selNucleo" onchange="clickNucleo(this.value)">
              <option value="">Todos los Núcleos (34)</option>
            </select>
            <div class="mode-toggle">
              <button class="mode-btn active" id="btnPct" onclick="setMode('pct')">% Éxito</button>
              <button class="mode-btn" id="btnVol" onclick="setMode('vol')">Matrícula</button>
            </div>
            <button class="mode-btn" onclick="resetMapa()" style="border:1px solid #e2e8f0;border-radius:7px;padding:5px 11px;background:#fff;font-size:11.5px;font-weight:600;color:#334155;cursor:pointer;font-family:Inter,sans-serif">🔄 Ver País</button>
          </div>
        </div>
        <div class="section-body" style="padding:16px">
          <div class="map-grid">
            <!-- SVG Map -->
            <div>
              <div class="map-wrap">
                <svg id="venezuelaMap" viewBox="0 0 600 527" xmlns="http://www.w3.org/2000/svg">
                  {svg_paths_str}
                  <g id="nucleosLayer"></g>
                </svg>
              </div>
              <div class="map-legend">
                <span class="legend-item"><span class="legend-swatch" style="background:#059669"></span> ≥98% Sobresaliente</span>
                <span class="legend-item"><span class="legend-swatch" style="background:#6ee7b7"></span> 95-97.9% Esperado</span>
                <span class="legend-item"><span class="legend-swatch" style="background:#fcd34d"></span> 90-94.9% Atención</span>
                <span class="legend-item"><span class="legend-swatch" style="background:#fca5a5"></span> &lt;90% Crítico</span>
                <span class="legend-item"><span class="legend-pin"></span> Núcleo UNES</span>
              </div>
            </div>
            <!-- Panel -->
            <div class="map-panel" id="mapPanel">
              <div class="map-panel-placeholder" id="mapPlaceholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <p>Selecciona un <strong>estado</strong> o <strong>núcleo</strong><br>en el mapa para ver su detalle académico</p>
              </div>
              <div id="mapPanelContent" style="display:none"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-row">
        <div class="section-card" style="margin-bottom:0">
          <div class="section-header">
            <div><h2>📊 Aprobados vs Reprobados por Carrera / PNF</h2></div>
          </div>
          <div class="section-body"><div class="chart-wrap"><canvas id="chartPNF"></canvas></div></div>
        </div>
        <div class="section-card" style="margin-bottom:0">
          <div class="section-header">
            <div><h2>🎯 Distribución por Trayecto</h2></div>
          </div>
          <div class="section-body"><div class="chart-wrap"><canvas id="chartTray"></canvas></div></div>
        </div>
      </div>
      <div class="section-card">
        <div class="section-header">
          <div><h2>🏛️ Top 10 Núcleos por Matrícula</h2></div>
        </div>
        <div class="section-body"><div class="chart-wrap" style="height:300px"><canvas id="chartNuc"></canvas></div></div>
      </div>

      <!-- PNF Table -->
      <div class="section-card">
        <div class="section-header">
          <div><h2>📋 Tabla de Programas de Formación (PNF)</h2></div>
        </div>
        <div class="section-body" style="padding-top:0">
          <table class="data-table">
            <thead>
              <tr>
                <th onclick="sortPNF(0)">Carrera / PNF ↕</th>
                <th onclick="sortPNF(1)">Total ↕</th>
                <th onclick="sortPNF(2)">Aprobados ↕</th>
                <th onclick="sortPNF(3)">Reprobados ↕</th>
                <th onclick="sortPNF(4)">% Éxito ↕</th>
              </tr>
            </thead>
            <tbody id="pnfTbody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ===== NÚCLEOS ===== -->
    <div class="view" id="view-nucleos">
      <div class="section-card">
        <div class="section-header">
          <div><h2>📍 Listado por Núcleo UNES</h2></div>
        </div>
        <div class="section-body">
          <div class="filter-bar">
            <input type="text" id="searchNucleo" placeholder="Buscar núcleo..." oninput="renderNucleos()">
            <select id="filtroEstadoNucleo" onchange="renderNucleos()">
              <option value="">Todos los Estados</option>
            </select>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Núcleo</th>
                <th>Estado</th>
                <th>Total</th>
                <th>Aprobados</th>
                <th>Reprobados</th>
                <th>% Éxito</th>
              </tr>
            </thead>
            <tbody id="nucleosTbody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ===== ESTUDIANTES ===== -->
    <div class="view" id="view-estudiantes">
      <div class="section-card">
        <div class="section-header">
          <div><h2>👤 Registro de Estudiantes</h2></div>
          <div id="estudiantesCount" style="font-size:12px;color:#64748b;font-weight:600"></div>
        </div>
        <div class="section-body">
          <div class="filter-bar">
            <input type="text" id="searchEst" placeholder="Buscar por nombre, cédula..." oninput="renderEstudiantes()">
            <select id="filtroNucleoEst" onchange="renderEstudiantes()">
              <option value="">Todos los Núcleos</option>
            </select>
            <select id="filtroEstatusEst" onchange="renderEstudiantes()">
              <option value="">Todos los Estatus</option>
              <option value="Aprobado">✅ Aprobados</option>
              <option value="Reprobado">❌ Reprobados</option>
            </select>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Cédula</th>
                <th>Nombre</th>
                <th>Núcleo</th>
                <th>PNF</th>
                <th>Trayecto</th>
                <th>Estatus</th>
              </tr>
            </thead>
            <tbody id="estTbody"></tbody>
          </table>
          <div class="pagination" id="pagination"></div>
        </div>
      </div>
    </div>

  </div><!-- /content -->
</div><!-- /main -->

<div id="tip"></div>
<div id="toast"></div>

<script>
// ═══════════════════════════════════════════════════════════════
// DATOS OFICIALES UNES - 6.070 ESTUDIANTES
// ═══════════════════════════════════════════════════════════════
const ESTUDIANTES = {est_json};
const NUCLEOS_GEO = {nucleos_geo_json};

// ═══════════════════════════════════════════════════════════════
// ESTADO GLOBAL
// ═══════════════════════════════════════════════════════════════
let modoMapa = 'pct'; // 'pct' | 'vol'
let estadoSel = null;
let nucleoSel = null;
let pnfSort = {{col:1, asc:false}};
let estPage = 1;
const EST_PER_PAGE = 60;
let chartPNF, chartTray, chartNuc;

// ═══════════════════════════════════════════════════════════════
// INICIALIZACIÓN
// ═══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {{
  poblarFiltros();
  showView('dashboard');
}});

function sincronizar() {{
  toast('✅ 6.070 registros oficiales cargados correctamente');
}}

function showView(id) {{
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('view-' + id).classList.add('active');
  document.getElementById('nav-' + id).classList.add('active');
  const titles = {{
    dashboard: 'Dashboard General',
    nucleos: 'Listado por Núcleo',
    estudiantes: 'Registro de Estudiantes'
  }};
  document.getElementById('topbarTitle').textContent = titles[id] || '';

  if (id === 'dashboard') renderDashboard();
  if (id === 'nucleos')   renderNucleos();
  if (id === 'estudiantes') renderEstudiantes();
  window.scrollTo({{top:0}});
}}

// ═══════════════════════════════════════════════════════════════
// ESTADÍSTICAS BASE
// ═══════════════════════════════════════════════════════════════
function getStats() {{
  const ap = ESTUDIANTES.filter(e => e.estatus === 'Aprobado').length;
  const rep = ESTUDIANTES.length - ap;
  const pct = ((ap / ESTUDIANTES.length) * 100).toFixed(1);

  const estadosMap = {{}};
  const nucleosMap = {{}};
  const pnfMap = {{}};
  const trayMap = {{}};

  ESTUDIANTES.forEach(e => {{
    const edo = e.estado || 'Sin Estado';
    const nuc = e.nucleo || 'Sin Núcleo';
    const pnf = e.pnf || 'Sin PNF';
    const tray = e.trayecto || 'I';

    if (!estadosMap[edo]) estadosMap[edo] = {{ap:0,rep:0,tot:0,nucleos:{{}}}};
    estadosMap[edo].tot++;
    if (e.estatus==='Aprobado') estadosMap[edo].ap++; else estadosMap[edo].rep++;
    if (!estadosMap[edo].nucleos[nuc]) estadosMap[edo].nucleos[nuc]={{ap:0,rep:0,tot:0}};
    estadosMap[edo].nucleos[nuc].tot++;
    if (e.estatus==='Aprobado') estadosMap[edo].nucleos[nuc].ap++; else estadosMap[edo].nucleos[nuc].rep++;

    if (!nucleosMap[nuc]) nucleosMap[nuc] = {{ap:0,rep:0,tot:0,estado:edo,pnf:{{}}}};
    nucleosMap[nuc].tot++;
    if (e.estatus==='Aprobado') nucleosMap[nuc].ap++; else nucleosMap[nuc].rep++;
    nucleosMap[nuc].pnf[pnf] = (nucleosMap[nuc].pnf[pnf]||0) + 1;

    if (!pnfMap[pnf]) pnfMap[pnf] = {{ap:0,rep:0,tot:0}};
    pnfMap[pnf].tot++;
    if (e.estatus==='Aprobado') pnfMap[pnf].ap++; else pnfMap[pnf].rep++;

    const tk = tray.toString().includes('IV')||tray==='4' ? 'IV' :
               tray.toString().includes('III')||tray==='3' ? 'III' :
               tray.toString().includes('II')||tray==='2' ? 'II' :
               tray.toString().includes('nicial')||tray==='0' ? 'Inicial' : 'I';
    trayMap[tk] = (trayMap[tk]||0)+1;
  }});

  return {{ap,rep,pct,estadosMap,nucleosMap,pnfMap,trayMap}};
}}

// ═══════════════════════════════════════════════════════════════
// DASHBOARD
// ═══════════════════════════════════════════════════════════════
function renderDashboard() {{
  const {{ap,rep,pct,estadosMap,nucleosMap,pnfMap,trayMap}} = getStats();
  const tot = ESTUDIANTES.length;
  const pctRep = ((rep/tot)*100).toFixed(1);
  const nNucleos = Object.keys(nucleosMap).length;
  const nTokens = new Set(ESTUDIANTES.map(e=>e.evaluacion||e.token).filter(Boolean)).size;

  document.getElementById('badgeTotal').textContent = tot.toLocaleString('es-VE') + ' Estudiantes';

  // ── KPI Cards ──
  const kpi = [
    {{icon:'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2 M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75M9 7m-4 0a4 4 0 108 0 4 4 0 00-8 0',
      ic:'#2563eb',ib:'#eff6ff',val:tot.toLocaleString('es-VE'),label:'Total Estudiantes',sub:'Matrícula 2026',
      bar:100,bc:'#2563eb',badge:'Oficial 100%',bp:'pill-blue'}},
    {{icon:'M20 6L9 17l-5-5',
      ic:'#059669',ib:'#ecfdf5',val:ap.toLocaleString('es-VE'),label:'Aprobados',sub:'Aptos evaluación final',
      bar:parseFloat(pct),bc:'#10b981',badge:'↑'+pct+'% Éxito',bp:'pill-green'}},
    {{icon:'M12 2a10 10 0 100 20 10 10 0 000-20M15 9l-6 6M9 9l6 6',
      ic:'#dc2626',ib:'#fef2f2',val:rep.toLocaleString('es-VE'),label:'Reprobados',sub:'Para recuperación',
      bar:parseFloat(pctRep),bc:'#ef4444',badge:pctRep+'% Pendiente',bp:'pill-red'}},
    {{icon:'M18 20v-10M12 20V4M6 20v-6',
      ic:'#d97706',ib:'#fffbeb',val:pct+'%',label:'Tasa de Aprobación',sub:'Meta ≥85% superada',
      bar:parseFloat(pct),bc:'#f59e0b',badge:'Meta OK',bp:'pill-amber'}},
    {{icon:'M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0M12 10m-3 0a3 3 0 106 0 3 3 0 00-6 0',
      ic:'#4f46e5',ib:'#eef2ff',val:nNucleos,label:'Núcleos Activos',sub:'24 Estados del país',
      bar:100,bc:'#6366f1',badge:'Nacional',bp:'pill-indigo'}},
    {{icon:'M7.5 15.5m-4.5 0a4.5 4.5 0 109 0 4.5 4.5 0 00-9 0M21 3l-9.5 9.5M15.5 7.5l3 3M14 11l2 2',
      ic:'#9f1239',ib:'#fff1f2',val:nTokens,label:'Tokens EPA',sub:'Evaluaciones culminadas',
      bar:100,bc:'#9f1239',badge:'167 EPA',bp:'pill-crimson'}}
  ];

  document.getElementById('kpiRow').innerHTML = kpi.map(k=>`
    <div class="kpi-card">
      <div class="kpi-top-bar" style="background:${{k.bc}}"></div>
      <div class="kpi-icon" style="background:${{k.ib}};color:${{k.ic}}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="${{k.icon}}"/></svg>
      </div>
      <div class="kpi-value" style="color:${{k.ic}}">${{k.val}}</div>
      <div class="kpi-label">${{k.label}}</div>
      <div class="kpi-sub">${{k.sub}}</div>
      <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:${{Math.min(k.bar,100)}}%;background:${{k.bc}}"></div></div>
    </div>
  `).join('');

  // ── Selector de Núcleos ──
  const sel = document.getElementById('selNucleo');
  if (sel.options.length <= 1) {{
    Object.keys(nucleosMap).sort().forEach(n => {{
      const o = document.createElement('option');
      o.value = n;
      o.textContent = n + ' (' + nucleosMap[n].tot + ')';
      sel.appendChild(o);
    }});
  }}

  // ── Mapa ──
  renderMapa(estadosMap, nucleosMap);

  // ── Gráficos ──
  renderCharts(pnfMap, trayMap, nucleosMap);

  // ── PNF Table ──
  renderPNFTable(pnfMap);
}}

// ═══════════════════════════════════════════════════════════════
// MAPA COROPLÉTICO
// ═══════════════════════════════════════════════════════════════
function getColor(pct, tot) {{
  if (modoMapa === 'vol') {{
    if (tot >= 500) return '#1e3a8a';
    if (tot >= 200) return '#3b82f6';
    if (tot >= 50)  return '#93c5fd';
    if (tot > 0)    return '#dbeafe';
    return '#e8edf5';
  }}
  if (pct >= 98) return '#059669';
  if (pct >= 95) return '#6ee7b7';
  if (pct >= 90) return '#fcd34d';
  if (pct > 0)   return '#fca5a5';
  return '#e8edf5';
}}

function renderMapa(estadosMap, nucleosMap) {{
  const svg = document.getElementById('venezuelaMap');
  if (!svg) return;

  svg.querySelectorAll('.map-state').forEach(p => {{
    const edo = p.getAttribute('data-estado');
    const d = estadosMap[edo];
    p.classList.remove('state-selected', 'state-dimmed');
    if (estadoSel && estadoSel !== edo) p.classList.add('state-dimmed');
    if (estadoSel && estadoSel === edo) p.classList.add('state-selected');

    if (d && d.tot > 0) {{
      const pct = (d.ap/d.tot)*100;
      p.style.fill = getColor(pct, d.tot);
      p.setAttribute('data-tooltip', edo + ': ' + d.ap + ' Aprobados / ' + d.rep + ' Reprobados (' + pct.toFixed(1) + '%)');
    }} else {{
      p.style.fill = '#e8edf5';
      p.setAttribute('data-tooltip', edo + ': Sin evaluaciones');
    }}
  }});

  // Pines de núcleos
  let layer = document.getElementById('nucleosLayer');
  if (!layer) {{ layer = document.createElementNS('http://www.w3.org/2000/svg','g'); layer.id='nucleosLayer'; svg.appendChild(layer); }}
  layer.innerHTML = '';

  Object.entries(NUCLEOS_GEO).forEach(([name, [x,y]]) => {{
    const nd = nucleosMap[name];
    if (!nd) return;
    const isActive = nucleoSel === name;
    const pct = nd.tot ? (nd.ap/nd.tot*100).toFixed(1) : 0;
    let pinColor = '#800020';
    if (parseFloat(pct) >= 98) pinColor = '#059669';
    else if (parseFloat(pct) < 90) pinColor = '#dc2626';

    const g = document.createElementNS('http://www.w3.org/2000/svg','g');
    g.setAttribute('class','nucleo-pin' + (isActive?' pin-active':''));
    g.setAttribute('transform','translate('+x+','+y+')');
    g.setAttribute('data-nucleo', name);

    const ring = document.createElementNS('http://www.w3.org/2000/svg','circle');
    ring.setAttribute('class','ring'); ring.setAttribute('r','6');
    ring.style.fill = pinColor;

    const dot = document.createElementNS('http://www.w3.org/2000/svg','circle');
    dot.setAttribute('class','dot'); dot.setAttribute('r','4');
    dot.style.fill = pinColor;

    g.appendChild(ring); g.appendChild(dot);
    g.addEventListener('click', ev => {{ ev.stopPropagation(); clickNucleo(name); }});
    g.addEventListener('mouseenter', ev => showTip('📍 ' + name + '\\n' + nd.tot + ' est. · ' + pct + '% aprobación', ev));
    g.addEventListener('mouseleave', hideTooltip);
    layer.appendChild(g);
  }});
}}

function clickEstado(nombre) {{
  if (estadoSel === nombre) {{ estadoSel = null; nucleoSel = null; }}
  else {{ estadoSel = nombre; nucleoSel = null; }}
  document.getElementById('selNucleo').value = '';
  renderDashboard();
}}

function clickNucleo(nombre) {{
  if (!nombre) {{ nucleoSel = null; estadoSel = null; renderDashboard(); return; }}
  nucleoSel = nombre;
  document.getElementById('selNucleo').value = nombre;

  const {{nucleosMap}} = getStats();
  const nd = nucleosMap[nombre];
  if (!nd) return;
  estadoSel = nd.estado;

  mostrarPanelNucleo(nombre, nd);
  renderDashboard();
}}

function setMode(m) {{
  modoMapa = m;
  document.getElementById('btnPct').classList.toggle('active', m==='pct');
  document.getElementById('btnVol').classList.toggle('active', m==='vol');
  renderDashboard();
}}

function resetMapa() {{
  estadoSel = null; nucleoSel = null;
  document.getElementById('selNucleo').value = '';
  document.getElementById('mapPlaceholder').style.display = 'flex';
  document.getElementById('mapPanelContent').style.display = 'none';
  renderDashboard();
}}

function hoverEstado(nombre, ev) {{
  const {{estadosMap}} = getStats();
  const d = estadosMap[nombre];
  if (d && d.tot > 0) {{
    const pct = (d.ap/d.tot*100).toFixed(1);
    const nNucleos = Object.keys(d.nucleos||{{}}).length;
    showTip('🏛️ ' + nombre + '\\n' + d.tot + ' evaluados · ' + pct + '% aprobación\\n' + nNucleos + ' núcleo(s)', ev);
  }} else {{
    showTip('🏛️ ' + nombre + '\\nSin evaluaciones', ev);
  }}
}}

function hideTooltip() {{
  document.getElementById('tip').style.display = 'none';
}}

function showTip(txt, ev) {{
  const t = document.getElementById('tip');
  t.innerHTML = txt.replace(/\\n/g, '<br>');
  t.style.display = 'block';
  t.style.left = (ev.pageX+14)+'px';
  t.style.top = (ev.pageY-35)+'px';
}}

function mostrarPanelNucleo(nombre, nd) {{
  const ph = document.getElementById('mapPlaceholder');
  const ct = document.getElementById('mapPanelContent');
  ph.style.display = 'none';
  ct.style.display = 'block';
  const pct = nd.tot ? ((nd.ap/nd.tot)*100).toFixed(1) : 0;
  const pctRep = nd.tot ? ((nd.rep/nd.tot)*100).toFixed(1) : 0;

  const pnfRows = Object.entries(nd.pnf||{{}})
    .sort((a,b)=>b[1]-a[1])
    .map(([p,c])=>`<div class="pnf-row"><span style="color:#334155;font-size:12px">${{p}}</span><strong style="color:#0f172a">${{c}}</strong></div>`)
    .join('');

  ct.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <div>
        <div class="panel-nucleo-title">📍 ${{nombre}}</div>
        <div class="panel-nucleo-sub">Estado: <strong>${{nd.estado}}</strong></div>
      </div>
      <button class="btn-cerrar-panel" onclick="resetMapa()">✕ Cerrar</button>
    </div>
    <div class="panel-stat-grid">
      <div class="panel-stat" style="background:#ecfdf5;border:1px solid #bbf7d0">
        <div class="panel-stat-val" style="color:#059669">${{nd.ap.toLocaleString('es-VE')}}</div>
        <div class="panel-stat-lbl" style="color:#065f46">Aprobados<br>${{pct}}%</div>
      </div>
      <div class="panel-stat" style="background:#fef2f2;border:1px solid #fecaca">
        <div class="panel-stat-val" style="color:#dc2626">${{nd.rep.toLocaleString('es-VE')}}</div>
        <div class="panel-stat-lbl" style="color:#991b1b">Reprobados<br>${{pctRep}}%</div>
      </div>
    </div>
    <div style="font-size:12px;color:#64748b;margin-bottom:6px">Total evaluados: <strong style="color:#0f172a">${{nd.tot.toLocaleString('es-VE')}}</strong></div>
    <div class="panel-pbar-bg"><div class="panel-pbar-fill" style="width:${{pct}}%;background:#10b981"></div></div>
    <div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.3px">Carreras activas:</div>
    <div style="max-height:160px;overflow-y:auto">${{pnfRows}}</div>
    <button class="btn-filtrar" onclick="filtrarPorNucleo('${{nombre}}')">🔍 Ver estudiantes de este núcleo</button>
  `;
}}

function filtrarPorNucleo(nombre) {{
  showView('estudiantes');
  document.getElementById('filtroNucleoEst').value = nombre;
  renderEstudiantes();
}}

// ═══════════════════════════════════════════════════════════════
// GRÁFICOS
// ═══════════════════════════════════════════════════════════════
function renderCharts(pnfMap, trayMap, nucleosMap) {{
  // 1. PNF Chart
  const pnfTop = Object.entries(pnfMap).sort((a,b)=>b[1].tot-a[1].tot).slice(0,8);
  const ctx1 = document.getElementById('chartPNF');
  if (ctx1) {{
    if (chartPNF) chartPNF.destroy();
    chartPNF = new Chart(ctx1, {{
      type:'bar',
      data:{{
        labels: pnfTop.map(([l])=>l.length>22?l.slice(0,20)+'…':l),
        datasets:[
          {{label:'Aprobados', data:pnfTop.map(([,v])=>v.ap), backgroundColor:'#10b981', borderRadius:5, borderSkipped:false}},
          {{label:'Reprobados', data:pnfTop.map(([,v])=>v.rep), backgroundColor:'#f43f5e', borderRadius:5, borderSkipped:false}}
        ]
      }},
      options:{{
        responsive:true, maintainAspectRatio:false,
        plugins:{{
          legend:{{position:'top',labels:{{font:{{family:'Inter',size:12,weight:'600'}}}}}},
          tooltip:{{callbacks:{{label(c){{
            const name = pnfTop[c.dataIndex][0];
            const stat = pnfMap[name];
            const p = stat.tot ? ((c.raw/stat.tot)*100).toFixed(1) : 0;
            return ' '+c.dataset.label+': '+c.raw.toLocaleString('es-VE')+' ('+p+'%)';
          }}}}}}
        }},
        scales:{{
          x:{{grid:{{display:false}},ticks:{{font:{{family:'Inter',size:10}},color:'#64748b'}}}},
          y:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.04)'}},ticks:{{font:{{family:'Inter',size:10}},color:'#64748b'}}}}
        }}
      }}
    }});
  }}

  // 2. Trayecto Chart
  const trayOrder = ['Inicial','I','II','III','IV'];
  const ctx2 = document.getElementById('chartTray');
  if (ctx2) {{
    if (chartTray) chartTray.destroy();
    chartTray = new Chart(ctx2, {{
      type:'doughnut',
      data:{{
        labels: trayOrder.map(t=>t==='Inicial'?'Inicial':'Trayecto '+t),
        datasets:[{{
          data: trayOrder.map(t=>trayMap[t]||0),
          backgroundColor:['#6366f1','#06b6d4','#10b981','#f59e0b','#ec4899'],
          borderWidth:3, borderColor:'#ffffff'
        }}]
      }},
      options:{{
        responsive:true, maintainAspectRatio:false, cutout:'65%',
        plugins:{{
          legend:{{position:'bottom',labels:{{font:{{family:'Inter',size:11}},padding:10}}}},
          tooltip:{{callbacks:{{label(c){{
            const tot = ESTUDIANTES.length;
            const p = tot?((c.raw/tot)*100).toFixed(1):0;
            return ' '+c.label+': '+c.raw.toLocaleString('es-VE')+' ('+p+'%)';
          }}}}}}
        }}
      }}
    }});
  }}

  // 3. Top 10 Núcleos
  const topNuc = Object.entries(nucleosMap).sort((a,b)=>b[1].tot-a[1].tot).slice(0,10);
  const ctx3 = document.getElementById('chartNuc');
  if (ctx3) {{
    if (chartNuc) chartNuc.destroy();
    chartNuc = new Chart(ctx3, {{
      type:'bar',
      data:{{
        labels: topNuc.map(([n])=>n.length>26?n.slice(0,24)+'…':n),
        datasets:[{{
          label:'Estudiantes',
          data:topNuc.map(([,v])=>v.tot),
          backgroundColor:'#800020', hoverBackgroundColor:'#9f1239',
          borderRadius:5, borderSkipped:false
        }}]
      }},
      options:{{
        indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{{
          legend:{{display:false}},
          tooltip:{{callbacks:{{label(c){{
            const name = topNuc[c.dataIndex][0];
            const v = nucleosMap[name];
            const p = v.tot?((v.ap/v.tot)*100).toFixed(1):0;
            return ' '+v.tot.toLocaleString('es-VE')+' estudiantes · '+p+'% aprobación';
          }}}}}}
        }},
        scales:{{
          x:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.04)'}},ticks:{{font:{{family:'Inter',size:10}},color:'#64748b'}}}},
          y:{{grid:{{display:false}},ticks:{{font:{{family:'Inter',size:11,weight:'600'}},color:'#334155'}}}}
        }}
      }}
    }});
  }}
}}

// ═══════════════════════════════════════════════════════════════
// TABLA PNF
// ═══════════════════════════════════════════════════════════════
function renderPNFTable(pnfMap) {{
  if (!pnfMap) {{const stats=getStats(); pnfMap=stats.pnfMap;}}
  let rows = Object.entries(pnfMap).map(([p,v])=>{{
    const pct = v.tot?Math.round((v.ap/v.tot)*100):0;
    return {{pnf:p,...v,pct}};
  }});
  const col = pnfSort.col;
  rows.sort((a,b)=>{{
    let va = col===0?a.pnf:col===1?a.tot:col===2?a.ap:col===3?a.rep:a.pct;
    let vb = col===0?b.pnf:col===1?b.tot:col===2?b.ap:col===3?b.rep:b.pct;
    return pnfSort.asc?(typeof va==='string'?va.localeCompare(vb):va-vb):(typeof va==='string'?vb.localeCompare(va):vb-va);
  }});

  document.getElementById('pnfTbody').innerHTML = rows.map(r=>`
    <tr>
      <td><strong style="color:#0f172a">${{r.pnf}}</strong></td>
      <td><strong>${{r.tot.toLocaleString('es-VE')}}</strong></td>
      <td style="color:#059669;font-weight:700">${{r.ap.toLocaleString('es-VE')}}</td>
      <td style="color:#dc2626;font-weight:700">${{r.rep.toLocaleString('es-VE')}}</td>
      <td>
        <div class="pct-bar">
          <span style="font-weight:700;width:36px;color:${{r.pct>=90?'#059669':r.pct>=80?'#d97706':'#dc2626'}}">${{r.pct}}%</span>
          <div class="pct-bar-bg"><div class="pct-bar-fill" style="width:${{r.pct}}%;background:${{r.pct>=90?'#10b981':r.pct>=80?'#f59e0b':'#ef4444'}}"></div></div>
        </div>
      </td>
    </tr>
  `).join('');
}}

function sortPNF(col) {{
  if (pnfSort.col===col) pnfSort.asc=!pnfSort.asc; else {{pnfSort.col=col;pnfSort.asc=false;}}
  renderPNFTable();
}}

// ═══════════════════════════════════════════════════════════════
// VISTA NÚCLEOS
// ═══════════════════════════════════════════════════════════════
function renderNucleos() {{
  const {{nucleosMap}} = getStats();
  const q = (document.getElementById('searchNucleo').value||'').toLowerCase();
  const filtEdo = document.getElementById('filtroEstadoNucleo').value;

  let rows = Object.entries(nucleosMap)
    .filter(([n,v])=>(!q||n.toLowerCase().includes(q))&&(!filtEdo||v.estado===filtEdo))
    .sort((a,b)=>b[1].tot-a[1].tot);

  document.getElementById('nucleosTbody').innerHTML = rows.map(([name,v])=>{{
    const pct = v.tot?((v.ap/v.tot)*100).toFixed(1):0;
    const color = pct>=98?'#059669':pct>=95?'#10b981':pct>=90?'#d97706':'#dc2626';
    return `<tr>
      <td style="font-weight:700;color:#0f172a;cursor:pointer" onclick="clickNucleoDesdeTabla('${{name}}')">${{name}}</td>
      <td style="color:#64748b">${{v.estado}}</td>
      <td><strong>${{v.tot.toLocaleString('es-VE')}}</strong></td>
      <td style="color:#059669;font-weight:700">${{v.ap.toLocaleString('es-VE')}}</td>
      <td style="color:#dc2626;font-weight:700">${{v.rep.toLocaleString('es-VE')}}</td>
      <td>
        <div class="pct-bar">
          <span style="font-weight:800;width:40px;color:${{color}}">${{pct}}%</span>
          <div class="pct-bar-bg"><div class="pct-bar-fill" style="width:${{pct}}%;background:${{color}}"></div></div>
        </div>
      </td>
    </tr>`;
  }}).join('');
}}

function clickNucleoDesdeTabla(nombre) {{
  showView('dashboard');
  clickNucleo(nombre);
}}

// ═══════════════════════════════════════════════════════════════
// VISTA ESTUDIANTES
// ═══════════════════════════════════════════════════════════════
function getEstFiltered() {{
  const q = (document.getElementById('searchEst').value||'').toLowerCase();
  const nuc = document.getElementById('filtroNucleoEst').value;
  const est = document.getElementById('filtroEstatusEst').value;
  return ESTUDIANTES.filter(e=>
    (!q||(e.nombre||'').toLowerCase().includes(q)||(e.cedula||'').toLowerCase().includes(q))&&
    (!nuc||e.nucleo===nuc)&&
    (!est||e.estatus===est)
  );
}}

function renderEstudiantes() {{
  const filtered = getEstFiltered();
  const total = filtered.length;
  const pages = Math.ceil(total/EST_PER_PAGE);
  if (estPage > pages) estPage = 1;
  const slice = filtered.slice((estPage-1)*EST_PER_PAGE, estPage*EST_PER_PAGE);

  document.getElementById('estudiantesCount').textContent = total.toLocaleString('es-VE') + ' registros encontrados';

  document.getElementById('estTbody').innerHTML = slice.map(e=>`
    <tr>
      <td style="font-weight:600;color:#334155;white-space:nowrap">${{e.cedula||'-'}}</td>
      <td style="color:#0f172a">${{e.nombre||'-'}}</td>
      <td style="color:#64748b;font-size:12px">${{e.nucleo||'-'}}</td>
      <td style="color:#64748b;font-size:12px">${{(e.pnf||'-').slice(0,28)}}</td>
      <td style="color:#64748b;font-size:12px">${{e.trayecto||'-'}}</td>
      <td><span class="badge ${{e.estatus==='Aprobado'?'badge-green':'badge-red'}}">${{e.estatus==='Aprobado'?'✅ Aprobado':'❌ Reprobado'}}</span></td>
    </tr>
  `).join('');

  // Paginación
  let pgHtml = `<span class="page-info">Página ${{estPage}} de ${{pages}} · ${{total.toLocaleString('es-VE')}} registros</span>`;
  if (pages > 1) {{
    pgHtml += `<button class="page-btn" onclick="changePage(${{estPage-1}})" ${{estPage<=1?'disabled':''}}>&laquo;</button>`;
    for (let i=Math.max(1,estPage-2);i<=Math.min(pages,estPage+2);i++) {{
      pgHtml += `<button class="page-btn${{i===estPage?' active':''}}" onclick="changePage(${{i}})">${{i}}</button>`;
    }}
    pgHtml += `<button class="page-btn" onclick="changePage(${{estPage+1}})" ${{estPage>=pages?'disabled':''}}>&raquo;</button>`;
  }}
  document.getElementById('pagination').innerHTML = pgHtml;
}}

function changePage(p) {{
  estPage = p;
  renderEstudiantes();
  document.getElementById('view-estudiantes').scrollIntoView({{behavior:'smooth'}});
}}

// ═══════════════════════════════════════════════════════════════
// FILTROS
// ═══════════════════════════════════════════════════════════════
function poblarFiltros() {{
  const {{nucleosMap,estadosMap}} = getStats();

  // Selector de estado en núcleos
  const selEdo = document.getElementById('filtroEstadoNucleo');
  Object.keys(estadosMap).sort().forEach(edo=>{{
    const o = document.createElement('option'); o.value=edo; o.textContent=edo;
    selEdo.appendChild(o);
  }});

  // Selector de núcleo en estudiantes
  const selNucEst = document.getElementById('filtroNucleoEst');
  Object.keys(nucleosMap).sort().forEach(n=>{{
    const o = document.createElement('option'); o.value=n; o.textContent=n+' ('+nucleosMap[n].tot+')';
    selNucEst.appendChild(o);
  }});
}}

// ═══════════════════════════════════════════════════════════════
// TOAST
// ═══════════════════════════════════════════════════════════════
function toast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 3500);
}}
</script>
</body>
</html>"""

# Escribir el archivo final
out_path = os.path.join(BASE_DIR, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)

print("index.html generado:", len(HTML), "chars")
print("Archivo:", out_path)
