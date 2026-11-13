import json
import re
import os

print("Iniciando actualizacion integral...")

# 1. Leer datos importados (6.070 estudiantes)
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)

students = data_json['estudiantes']
print(f"Estudiantes cargados: {len(students)}")

# 2. Leer paths del mapa de Venezuela
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\map_paths.txt', 'r', encoding='utf-8') as f:
    map_paths = f.read()

# 3. Actualizar index.html
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Construir nuevo bloque de Dashboard que incluya las 6 tarjetas de métricas, los gráficos y el Mapa de Venezuela
dashboard_section = f'''<section class="view active" id="view-dashboard">

      <!-- Fila de 6 tarjetas de métricas principales -->
      <div class="stats-row" id="statsGrid"></div>

      <!-- SECCIÓN MAPA INTERACTIVO DE VENEZUELA Y DESGLOSE POR NÚCLEO -->
      <div class="map-section" id="mapSection" style="margin-bottom: 16px;">
        <!-- Panel izquierdo: Mapa SVG interactivo -->
        <div class="map-left">
          <div class="map-header">
            <div>
              <h3>🗺️ Mapa Nacional de Resultados Académicos por Núcleo</h3>
              <p>Haz clic o pasa el cursor sobre cualquier estado para ver los Aprobados y Reprobados</p>
            </div>
            <button class="btn-secondary" onclick="seleccionarEstado(null)" style="font-size:11px;padding:4px 10px;cursor:pointer;">Ver Todo el País</button>
          </div>
          <div class="map-container" style="position:relative;">
            <svg id="venezuelaMap" viewBox="0 0 600 527" xmlns="http://www.w3.org/2000/svg">
              {map_paths}
            </svg>
          </div>
          <div class="map-legend">
            <div class="map-legend-item"><span class="legend-dot" style="background:#059669"></span> Alto Rendimiento (&ge;90%)</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#d97706"></span> Rendimiento Medio (75% - 89%)</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#dc2626"></span> Bajo Rendimiento (&lt;75%)</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#e2e8f0"></span> Sin registros</div>
          </div>
        </div>

        <!-- Panel derecho: Desglose interactivo de Núcleos -->
        <div class="map-right" id="mapPanel">
          <div class="map-panel-placeholder" id="mapPanelPlaceholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <h4>Selecciona un Estado</h4>
            <p>Haz clic en cualquier estado del mapa para ver sus núcleos y resultados académicos detallados.</p>
          </div>
          <div id="mapPanelContent" style="display:none;padding:14px;"></div>
        </div>
      </div>

      <!-- Gráficas en grid 3 columnas -->
      <div class="dash-charts" id="dashCharts" style="margin-bottom: 16px;">
        <div class="chart-card dash-chart-main">
          <div class="chart-header">
            <h3>Aprobados vs Reprobados por PNF</h3>
          </div>
          <div class="chart-wrap"><canvas id="chartPNF"></canvas></div>
        </div>
        <div class="chart-card dash-chart-right">
          <div class="chart-header">
            <h3>Distribución por Trayecto</h3>
          </div>
          <div class="chart-wrap"><canvas id="chartTrayecto"></canvas></div>
        </div>
        <div class="chart-card dash-chart-bottom">
          <div class="chart-header">
            <h3>Top 10 Núcleos por Matrícula</h3>
          </div>
          <div class="chart-wrap"><canvas id="chartNucleos"></canvas></div>
        </div>
      </div>

      <!-- Tabla de PNFs -->
      <div class="dash-table-card">
        <div class="table-card-header">
          <div>
            <h3>Consolidado Académico por PNF</h3>
            <p class="section-desc">Resumen oficial de estudiantes, índices de aprobación y efectividad por programa</p>
          </div>
          <div class="table-actions">
            <input type="text" class="search-input" id="pnfSearch" placeholder="Buscar PNF..." oninput="filtrarPNF()" />
          </div>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th onclick="sortPNF(0)" style="cursor:pointer">PNF / Programa ⇅</th>
                <th onclick="sortPNF(1)" style="cursor:pointer">Total Matricula ⇅</th>
                <th onclick="sortPNF(2)" style="cursor:pointer">Aprobados ⇅</th>
                <th onclick="sortPNF(3)" style="cursor:pointer">Reprobados ⇅</th>
                <th onclick="sortPNF(4)" style="cursor:pointer">% Aprobación ⇅</th>
                <th>Rendimiento</th>
              </tr>
            </thead>
            <tbody id="pnfTableBody"></tbody>
          </table>
        </div>
      </div>

    </section>'''

# Reemplazar sección dashboard en index.html
dash_start = html.find('<section class="view active" id="view-dashboard">')
dash_end = html.find('<!-- ===== NÚCLEOS', dash_start)
if dash_end == -1:
    dash_end = html.find('<!-- ===== N', dash_start)
if dash_end == -1:
    dash_end = html.find('<section class="view" id="view-nucleos">', dash_start)

if dash_start != -1 and dash_end != -1:
    html = html[:dash_start] + dashboard_section + '\n\n    ' + html[dash_end:]
    print("Dashboard en index.html reemplazado con éxito!")
else:
    print("No se encontraron delimitadores para reemplazar dashboard en index.html")

# Actualizar versión de auto-purge en index.html a 8
html = re.sub(r'_db\.version < \d+', '_db.version < 8', html)

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html guardado exitosamente.")

# 4. Actualizar unes_sistema_final.js y app.js con el código completo y los 6.070 estudiantes
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Actualizar INITIAL_ESTUDIANTES
start_idx = js_code.find('const INITIAL_ESTUDIANTES =')
end_idx = js_code.find('const CAMPOS_SISTEMA =')
new_init = 'const INITIAL_ESTUDIANTES = ' + json.dumps(students, ensure_ascii=False) + ';\n\n// CAMPOS RECONOCIDOS\n'
js_code = js_code[:start_idx] + new_init + js_code[end_idx:]

# Funciones completas del mapa
map_functions_js = '''
// ── MAPA INTERACTIVO DE VENEZUELA Y DESGLOSE POR NÚCLEO ─────────────────────
let estadoSeleccionado = null;

function nucleoToEstado(n) {
  if (!n) return 'CARACAS';
  const clean = n.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toUpperCase().trim();
  if (['CARACAS', 'POLICARACAS', 'SAN PEDRO', 'EL LLANITO', 'EL JUNQUITO', 'CAFETAL', 'POLISUCRE'].some(x => clean.includes(x))) return 'CARACAS';
  if (['BARLOVENTO', 'VALLES DEL TUY', 'GUARENAS', 'GUATIRE', 'ALTOS MIRANDINOS', 'METROPOLITANO'].some(x => clean.includes(x))) return 'MIRANDA';
  if (['BOLIVAR', 'ANGOSTURA', 'PUERTO ORDAZ', 'PTO. ORDAZ'].some(x => clean.includes(x))) return 'BOLÍVAR';
  if (['SUCRE', 'CUMANA', 'CARUPANO', 'POLICIA ESTADAL'].some(x => clean.includes(x))) return 'SUCRE';
  if (clean.includes('GUAIRA')) return 'LA GUAIRA';
  if (clean.includes('ANZOATEGUI') || clean.includes('ANACO')) return 'ANZOÁTEGUI';
  if (clean.includes('PORTUGUESA')) return 'PORTUGUESA';
  if (clean.includes('BARINAS')) return 'BARINAS';
  if (clean.includes('MERIDA')) return 'MÉRIDA';
  if (clean.includes('ZULIA')) return 'ZULIA';
  if (clean.includes('MONAGAS')) return 'MONAGAS';
  if (clean.includes('FALCON')) return 'FALCÓN';
  if (clean.includes('TRUJILLO')) return 'TRUJILLO';
  if (clean.includes('CARABOBO')) return 'CARABOBO';
  if (clean.includes('NUEVA ESPARTA') || clean.includes('MARGARITA')) return 'NUEVA ESPARTA';
  if (clean.includes('APURE')) return 'APURE';
  if (clean.includes('AMAZONAS') || clean.includes('AMAZONA')) return 'AMAZONAS';
  if (clean.includes('TACHIRA')) return 'TÁCHIRA';
  if (clean.includes('DELTA')) return 'DELTA AMACURO';
  if (clean.includes('YARACUY')) return 'YARACUY';
  if (clean.includes('COJEDES')) return 'COJEDES';
  if (clean.includes('LARA')) return 'LARA';
  if (clean.includes('ARAGUA')) return 'ARAGUA';
  if (clean.includes('GUARICO')) return 'GUÁRICO';
  return 'CARACAS';
}

function renderMapa() {
  const est = DB.estudiantes;
  const estadoStats = {};

  est.forEach(e => {
    const estado = e.estado || nucleoToEstado(e.nucleo);
    if (!estadoStats[estado]) {
      estadoStats[estado] = { ap: 0, rep: 0, tot: 0, nucleos: {} };
    }
    estadoStats[estado].tot++;
    if (e.estatus === 'Aprobado') estadoStats[estado].ap++;
    else estadoStats[estado].rep++;

    const n = e.nucleo || 'Núcleo Central';
    if (!estadoStats[estado].nucleos[n]) {
      estadoStats[estado].nucleos[n] = { ap: 0, rep: 0, tot: 0 };
    }
    estadoStats[estado].nucleos[n].tot++;
    if (e.estatus === 'Aprobado') estadoStats[estado].nucleos[n].ap++;
    else estadoStats[estado].nucleos[n].rep++;
  });

  // Pintar cada estado en el SVG según su porcentaje de aprobación
  document.querySelectorAll('.map-state').forEach(path => {
    const estadoName = path.getAttribute('data-estado');
    const data = estadoStats[estadoName];

    path.classList.remove('pct-high', 'pct-mid', 'pct-low', 'selected');

    if (data && data.tot > 0) {
      const pct = (data.ap / data.tot) * 100;
      if (pct >= 90) path.classList.add('pct-high');
      else if (pct >= 75) path.classList.add('pct-mid');
      else path.classList.add('pct-low');

      path.setAttribute('data-tooltip', `${estadoName}: ${data.ap.toLocaleString()} Aprobados / ${data.rep.toLocaleString()} Reprobados (${Math.round(pct)}%)`);
    } else {
      path.setAttribute('data-tooltip', `${estadoName}: Sin registros`);
    }

    if (estadoSeleccionado && estadoName === estadoSeleccionado) {
      path.classList.add('selected');
    }
  });

  actualizarPanelEstado(estadoSeleccionado, estadoStats);
}

function seleccionarEstado(nombreEstado) {
  estadoSeleccionado = (estadoSeleccionado === nombreEstado) ? null : nombreEstado;
  renderMapa();
}

function hoverEstado(nombreEstado, evt) {
  const path = document.querySelector(`.map-state[data-estado="${nombreEstado}"]`);
  if (!path) return;
  const tip = path.getAttribute('data-tooltip');
  if (!tip) return;

  let tooltipEl = document.getElementById('mapTooltip');
  if (!tooltipEl) {
    tooltipEl = document.createElement('div');
    tooltipEl.id = 'mapTooltip';
    tooltipEl.className = 'map-tooltip';
    document.body.appendChild(tooltipEl);
  }
  tooltipEl.textContent = tip;
  tooltipEl.style.display = 'block';
  tooltipEl.style.left = (evt.pageX + 12) + 'px';
  tooltipEl.style.top = (evt.pageY - 28) + 'px';
}

function leaveEstado() {
  const tooltipEl = document.getElementById('mapTooltip');
  if (tooltipEl) tooltipEl.style.display = 'none';
}

function actualizarPanelEstado(estado, estadoStats) {
  const ph = document.getElementById('mapPanelPlaceholder');
  const ct = document.getElementById('mapPanelContent');
  if (!ph || !ct) return;

  if (!estado || !estadoStats[estado]) {
    const est = DB.estudiantes;
    const tot = est.length;
    const ap = est.filter(e => e.estatus === 'Aprobado').length;
    const rep = est.filter(e => e.estatus === 'Reprobado').length;
    const pct = tot ? Math.round((ap / tot) * 100) : 0;
    const estadosConDatos = Object.keys(estadoStats).length;

    ph.style.display = 'none';
    ct.style.display = 'block';
    ct.innerHTML = `
      <div class="map-panel-header" style="padding-bottom:10px;border-bottom:1px solid #e2e8f0;">
        <h4 style="margin:0;font-size:15px;color:#1e293b;font-weight:700;">🇻🇪 Resumen Nacional</h4>
        <span style="font-size:12px;color:#64748b;">${estadosConDatos} Estados con evaluaciones</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:8px 10px;">
          <div style="font-size:11px;color:#065f46;font-weight:600;">Total Aprobados</div>
          <div style="font-size:18px;color:#059669;font-weight:800;">${ap.toLocaleString()} <span style="font-size:11px;font-weight:600;">(${pct}%)</span></div>
        </div>
        <div style="background:#fff1f2;border:1px solid #fecdd3;border-radius:8px;padding:8px 10px;">
          <div style="font-size:11px;color:#9f1239;font-weight:600;">Total Reprobados</div>
          <div style="font-size:18px;color:#e11d48;font-weight:800;">${rep.toLocaleString()} <span style="font-size:11px;font-weight:600;">(${100 - pct}%)</span></div>
        </div>
      </div>
      <div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px;">Estados con Mayor Matrícula:</div>
      <div style="max-height:220px;overflow-y:auto;border:1px solid #f1f5f9;border-radius:8px;">
        ${Object.entries(estadoStats).sort((a,b) => b[1].tot - a[1].tot).map(([estName, data]) => {
          const ePct = Math.round((data.ap / data.tot) * 100);
          return `
            <div onclick="seleccionarEstado('${estName}')" style="display:flex;justify-content:space-between;align-items:center;padding:7px 10px;border-bottom:1px solid #f8fafc;cursor:pointer;transition:background 0.15s;" onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
              <strong style="font-size:12px;color:#334155;">${estName}</strong>
              <span style="font-size:11px;">
                <span style="color:#059669;font-weight:700;">${data.ap.toLocaleString()} ap</span> · 
                <span style="color:#e11d48;font-weight:700;">${data.rep.toLocaleString()} rep</span>
                <span style="color:#64748b;margin-left:4px;">(${ePct}%)</span>
              </span>
            </div>
          `;
        }).join('')}
      </div>
    `;
    return;
  }

  const data = estadoStats[estado];
  const pct = Math.round((data.ap / data.tot) * 100);

  ph.style.display = 'none';
  ct.style.display = 'block';

  const nucleosHTML = Object.entries(data.nucleos).sort((a,b) => b[1].tot - a[1].tot).map(([nName, nData]) => {
    const nPct = Math.round((nData.ap / nData.tot) * 100);
    return `
      <div class="map-nucleo-card" style="background:#ffffff;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
          <strong style="font-size:12px;color:#0f172a;">${escapeHTML(nName)}</strong>
          <span style="font-size:11px;font-weight:700;color:${nPct >= 90 ? '#059669' : nPct >= 75 ? '#d97706' : '#e11d48'};">${nPct}%</span>
        </div>
        <div style="background:#e2e8f0;height:5px;border-radius:3px;overflow:hidden;margin-bottom:6px;">
          <div style="width:${nPct}%;background:${nPct >= 90 ? '#10b981' : nPct >= 75 ? '#f59e0b' : '#ef4444'};height:100%;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:11px;color:#64748b;">
          <span>Total: <strong>${nData.tot.toLocaleString()}</strong></span>
          <span><span style="color:#059669;font-weight:700;">${nData.ap.toLocaleString()}</span> Aprobados · <span style="color:#e11d48;font-weight:700;">${nData.rep.toLocaleString()}</span> Rep</span>
        </div>
      </div>
    `;
  }).join('');

  ct.innerHTML = `
    <div class="map-panel-header" style="display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid #e2e8f0;">
      <div>
        <h4 style="margin:0;font-size:16px;color:#1e293b;font-weight:800;">📍 ${escapeHTML(estado)}</h4>
        <span style="font-size:12px;color:#64748b;">${Object.keys(data.nucleos).length} Núcleos registrados</span>
      </div>
      <button class="btn-secondary" onclick="seleccionarEstado(null)" style="font-size:11px;padding:4px 8px;border-radius:6px;cursor:pointer;">Ver Todo</button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">
      <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:8px 10px;">
        <div style="font-size:11px;color:#065f46;font-weight:600;">Aprobados</div>
        <div style="font-size:18px;color:#059669;font-weight:800;">${data.ap.toLocaleString()} <span style="font-size:11px;font-weight:600;">(${pct}%)</span></div>
      </div>
      <div style="background:#fff1f2;border:1px solid #fecdd3;border-radius:8px;padding:8px 10px;">
        <div style="font-size:11px;color:#9f1239;font-weight:600;">Reprobados</div>
        <div style="font-size:18px;color:#e11d48;font-weight:800;">${data.rep.toLocaleString()} <span style="font-size:11px;font-weight:600;">(${100 - pct}%)</span></div>
      </div>
    </div>
    <div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:8px;">Desglose por Núcleo:</div>
    <div style="max-height:220px;overflow-y:auto;padding-right:2px;">
      ${nucleosHTML}
    </div>
  `;
}
'''

# Inyectar funciones de mapa
if 'function renderMapa' not in js_code:
    idx_db = js_code.find('// ── DASHBOARD')
    js_code = js_code[:idx_db] + map_functions_js + '\n' + js_code[idx_db:]
else:
    # Reemplazar existente
    m_start = js_code.find('// ── MAPA INTERACTIVO')
    m_end = js_code.find('// ── DASHBOARD')
    if m_start != -1 and m_end != -1:
        js_code = js_code[:m_start] + map_functions_js + '\n' + js_code[m_end:]

# Asegurar que renderDashboard llame a renderMapa()
if 'renderMapa();' not in js_code:
    js_code = js_code.replace('renderPNFTable();', 'renderPNFTable();\n  renderMapa();')

# Actualizar versión de base de datos a 8
js_code = re.sub(r'version < \d+', 'version < 8', js_code)
js_code = re.sub(r'DB\.version = \d+;', 'DB.version = 8;', js_code)
js_code = js_code.replace('UNES v7', 'UNES v8 (6.070 registros con Mapa Interactivo)')
js_code = js_code.replace('2.443 estudiantes', '6.070 estudiantes: 5.890 Aprobados y 180 Reprobados')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("unes_sistema_final.js y app.js actualizados con 6.070 registros y funciones de mapa!")

# 5. Agregar estilos del tooltip y pulir estilos en styles.css
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

tooltip_css = '''
/* Tooltip flotante para el mapa interactivo de Venezuela */
.map-tooltip {
  position: absolute;
  background: rgba(15, 23, 42, 0.94);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  pointer-events: none;
  z-index: 1000;
  display: none;
  box-shadow: 0 4px 14px rgba(0,0,0,0.3);
  backdrop-filter: blur(4px);
  white-space: nowrap;
  border: 1px solid rgba(255,255,255,0.15);
  font-family: 'Inter', sans-serif;
}
'''

if '.map-tooltip' not in css:
    css += tooltip_css
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("styles.css actualizado con estilos de tooltip.")

print("Actualización integral completada exitosamente!")
