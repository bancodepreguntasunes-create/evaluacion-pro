
import json

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json', 'r', encoding='utf-8') as f:
    imported = json.load(f)

estudiantes_data = imported['estudiantes']
print(f'Loading {len(estudiantes_data)} students for bundling into initial state...')

# Build app.js code
js_code = f"""// ========================================================
// UNES · Sistema EPA — Evaluación de Progreso Académico
// Lógica Principal de la Aplicación (app.js)
// ========================================================

// Datos iniciales de los estudiantes convertidos de los archivos oficiales
const INITIAL_ESTUDIANTES = {json.dumps(estudiantes_data, ensure_ascii=False)};

// Campos reconocidos para el mapeo de importación
const CAMPOS_SISTEMA = [
  {{ key: 'cedula',   label: 'Cédula de Identidad',                    req: true  }},
  {{ key: 'nombre',   label: 'Nombre y Apellido',                      req: true  }},
  {{ key: 'nucleo',   label: 'Núcleo / Sede',                          req: true  }},
  {{ key: 'pnf',      label: 'PNF / Carrera',                          req: true  }},
  {{ key: 'trayecto', label: 'Trayecto (Inicial, I, II, III, IV)',     req: true  }},
  {{ key: 'token',    label: 'Token de Evaluación',                    req: false }},
  {{ key: 'estatus',  label: 'Estado / Puntaje (>= 60 = Aprobado)',    req: true  }},
  {{ key: 'puntaje',  label: 'Puntaje Numérico (Opcional si separado)', req: false }}
];

// Estado global de la base de datos
let DB = {{
  estudiantes: [],
  nucleos: [],
  nextId: {imported['nextId']}
}};

// Variables para importación de archivos
let excelRows = [];
let excelHeaders = [];
let archivosImportados = [];

// Instancias de gráficos Chart.js
let chartPNFInstance = null;
let chartTrayectoInstance = null;
let chartNucleosInstance = null;

// Ordenamiento de tabla PNF en dashboard
let pnfSortCol = 1;
let pnfSortAsc = false;

// ── Inicialización ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {{
  cargarDB();
  poblarSelects();
  initEventListeners();
  showView('dashboard');
}});

// ── Persistencia (LocalStorage) ─────────────────────────────────────────────
function cargarDB() {{
  try {{
    const saved = localStorage.getItem('unesDB');
    if (saved) {{
      const parsed = JSON.parse(saved);
      if (parsed.estudiantes && parsed.estudiantes.length > 0) {{
        DB = parsed;
      }} else {{
        DB.estudiantes = INITIAL_ESTUDIANTES;
        guardarDB();
      }}
    }} else {{
      DB.estudiantes = INITIAL_ESTUDIANTES;
      guardarDB();
    }}
  }} catch (e) {{
    console.warn('Error al cargar localStorage, usando datos iniciales:', e);
    DB.estudiantes = INITIAL_ESTUDIANTES;
  }}
}}

function guardarDB() {{
  try {{
    localStorage.setItem('unesDB', JSON.stringify(DB));
  }} catch (e) {{
    console.error('Error al guardar en localStorage:', e);
  }}
}}

// ── Navegación entre vistas ─────────────────────────────────────────────────
function showView(viewId) {{
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.sidebar-nav .nav-item').forEach(n => n.classList.remove('active'));

  const targetView = document.getElementById('view-' + viewId);
  const targetNav = document.getElementById('nav-' + viewId);

  if (targetView) targetView.classList.add('active');
  if (targetNav) targetNav.classList.add('active');

  const titles = {{
    dashboard:   'Dashboard General',
    nucleos:     'Listado por Núcleo',
    estudiantes: 'Registro de Estudiantes',
    reportes:    'Reportes: Núcleo › PNF › Token',
    calendario:  'Cronograma de Evaluaciones – EPA',
    importar:    'Importar desde Excel',
    instructivo: 'Instructivo del Sistema EPA'
  }};

  const titleEl = document.getElementById('topbarTitle');
  if (titleEl) titleEl.textContent = titles[viewId] || 'Sistema EPA';

  if (viewId === 'dashboard')   renderDashboard();
  if (viewId === 'nucleos')     filtrarTabla();
  if (viewId === 'estudiantes') renderRecientes();
  if (viewId === 'reportes')    generarReporte();
  if (viewId === 'calendario')  renderCalendario();

  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function toggleSidebar() {{
  const sidebar = document.getElementById('sidebar');
  const main = document.getElementById('main');
  if (sidebar && main) {{
    sidebar.classList.toggle('collapsed');
    main.classList.toggle('sidebar-collapsed');
  }}
}}

// ── Población de Desplegables ───────────────────────────────────────────────
function poblarSelects() {{
  const nucleosSet = new Set(NUCLEOS);
  DB.estudiantes.forEach(e => {{ if (e.nucleo) nucleosSet.add(e.nucleo); }});
  const nucleosArray = Array.from(nucleosSet).sort();

  const pnfsSet = new Set();
  PNF_LIST.forEach(p => pnfsSet.add(p.nombre));
  pnfsSet.add('Ciencias Policiales');
  DB.estudiantes.forEach(e => {{ if (e.pnf) pnfsSet.add(e.pnf); }});
  const pnfsArray = Array.from(pnfsSet).sort();

  function fill(selectId, items, placeholder) {{
    const el = document.getElementById(selectId);
    if (!el) return;
    const current = el.value;
    el.innerHTML = `<option value="">${{placeholder}}</option>` +
      items.map(it => `<option value="${{escapeHTML(it)}}">${{escapeHTML(it)}}</option>`).join('');
    if (current) el.value = current;
  }}

  fill('filtroNucleo', nucleosArray, 'Todos los núcleos');
  fill('filtroPNF', pnfsArray, 'Todos los PNF');
  fill('nucleo', nucleosArray, 'Seleccionar núcleo...');
  fill('pnf', pnfsArray, 'Seleccionar PNF...');
  fill('reporteNucleo', nucleosArray, 'Todos los núcleos');
  fill('reportePNF', pnfsArray, 'Todos los PNF');
  fill('calFiltroNucleo', nucleosArray, 'Todos los núcleos');
  fill('calFiltroPNF', pnfsArray, 'Todos los PNF');
}}

// ── DASHBOARD ───────────────────────────────────────────────────────────────
function renderDashboard() {{
  const est = DB.estudiantes;
  const total = est.length;
  const aprobados = est.filter(e => e.estatus === 'Aprobado').length;
  const reprobados = est.filter(e => e.estatus === 'Reprobado').length;
  const pct = total ? Math.round((aprobados / total) * 100) : 0;

  const nucleosActivos = new Set(est.map(e => e.nucleo)).size;

  // 1. Stats Row
  const statsGrid = document.getElementById('statsGrid');
  if (statsGrid) {{
    statsGrid.innerHTML = `
      <div class="stat-card">
        <div class="stat-icon" style="background:rgba(99,102,241,0.12);color:#6366f1">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">${{total.toLocaleString()}}</span>
          <span class="stat-label">Total Estudiantes</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:rgba(16,185,129,0.12);color:#10b981">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value" style="color:#10b981">${{aprobados.toLocaleString()}}</span>
          <span class="stat-label">Aprobados (≥ 60 pts)</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:rgba(239,68,68,0.12);color:#ef4444">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value" style="color:#ef4444">${{reprobados.toLocaleString()}}</span>
          <span class="stat-label">Reprobados (&lt; 60 pts)</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:rgba(245,158,11,0.12);color:#f59e0b">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value" style="color:#f59e0b">${{pct}}%</span>
          <span class="stat-label">Efectividad General</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:rgba(128,0,32,0.12);color:#800020">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value" style="color:#800020">${{nucleosActivos}}</span>
          <span class="stat-label">Núcleos con Registros</span>
        </div>
      </div>
    `;
  }}

  // 2. Gráficos
  renderGraficos(est);

  // 3. Tabla de PNFs
  renderPNFTable();
}}

function renderGraficos(est) {{
  if (typeof Chart === 'undefined') return;

  // PNF Chart
  const pnfMap = {{}};
  est.forEach(e => {{
    const p = e.pnf || 'Sin PNF';
    if (!pnfMap[p]) pnfMap[p] = {{ ap: 0, rep: 0, tot: 0 }};
    pnfMap[p].tot++;
    if (e.estatus === 'Aprobado') pnfMap[p].ap++;
    else pnfMap[p].rep++;
  }});

  const pnfLabels = Object.keys(pnfMap).sort((a,b) => pnfMap[b].tot - pnfMap[a].tot).slice(0, 7);
  const pnfShortLabels = pnfLabels.map(l => l.length > 20 ? l.substring(0, 18) + '…' : l);
  const apData = pnfLabels.map(l => pnfMap[l].ap);
  const repData = pnfLabels.map(l => pnfMap[l].rep);

  const ctxPNF = document.getElementById('chartPNF');
  if (ctxPNF) {{
    if (chartPNFInstance) chartPNFInstance.destroy();
    chartPNFInstance = new Chart(ctxPNF, {{
      type: 'bar',
      data: {{
        labels: pnfShortLabels,
        datasets: [
          {{ label: 'Aprobados', data: apData, backgroundColor: '#10b981', borderRadius: 4 }},
          {{ label: 'Reprobados', data: repData, backgroundColor: '#ef4444', borderRadius: 4 }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top', labels: {{ font: {{ family: 'Inter', size: 11 }} }} }} }},
        scales: {{
          x: {{ stacked: false, ticks: {{ font: {{ family: 'Inter', size: 10 }} }} }},
          y: {{ beginAtZero: true, ticks: {{ font: {{ family: 'Inter', size: 10 }} }} }}
        }}
      }}
    }});
  }}

  // Trayecto Chart
  const trayectoCounts = {{ 'Inicial': 0, 'I': 0, 'II': 0, 'III': 0, 'IV': 0 }};
  est.forEach(e => {{
    const t = e.trayecto || 'I';
    if (trayectoCounts[t] !== undefined) trayectoCounts[t]++;
    else trayectoCounts['I']++;
  }});

  const ctxTrayecto = document.getElementById('chartTrayecto');
  if (ctxTrayecto) {{
    if (chartTrayectoInstance) chartTrayectoInstance.destroy();
    chartTrayectoInstance = new Chart(ctxTrayecto, {{
      type: 'doughnut',
      data: {{
        labels: ['Inicial', 'Trayecto I', 'Trayecto II', 'Trayecto III', 'Trayecto IV'],
        datasets: [{{
          data: Object.values(trayectoCounts),
          backgroundColor: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899']
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ family: 'Inter', size: 10 }} }} }} }}
      }}
    }});
  }}

  // Top 10 Núcleos Chart
  const nucleoCounts = {{}};
  est.forEach(e => {{
    const n = e.nucleo || 'Desconocido';
    nucleoCounts[n] = (nucleoCounts[n] || 0) + 1;
  }});
  const topNucleos = Object.entries(nucleoCounts)
    .sort((a,b) => b[1] - a[1])
    .slice(0, 10);

  const ctxNucleos = document.getElementById('chartNucleos');
  if (ctxNucleos) {{
    if (chartNucleosInstance) chartNucleosInstance.destroy();
    chartNucleosInstance = new Chart(ctxNucleos, {{
      type: 'bar',
      data: {{
        labels: topNucleos.map(n => n[0].length > 18 ? n[0].substring(0, 16) + '…' : n[0]),
        datasets: [{{
          label: 'Estudiantes',
          data: topNucleos.map(n => n[1]),
          backgroundColor: '#800020',
          borderRadius: 4
        }}]
      }},
      options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ beginAtZero: true, ticks: {{ font: {{ family: 'Inter', size: 10 }} }} }},
          y: {{ ticks: {{ font: {{ family: 'Inter', size: 10 }} }} }}
        }}
      }}
    }});
  }}
}}

// ── TABLA DE RENDIMIENTO POR PNF (EN DASHBOARD) ──────────────────────────────
function getPNFData() {{
  const est = DB.estudiantes;
  const map = {{}};
  est.forEach(e => {{
    const p = e.pnf || 'Sin PNF';
    if (!map[p]) map[p] = {{ pnf: p, total: 0, ap: 0, rep: 0, pct: 0 }};
    map[p].total++;
    if (e.estatus === 'Aprobado') map[p].ap++;
    else map[p].rep++;
  }});
  Object.values(map).forEach(item => {{
    item.pct = item.total ? Math.round((item.ap / item.total) * 100) : 0;
  }});
  return Object.values(map);
}}

function renderPNFTable() {{
  let list = getPNFData();
  const searchInput = document.getElementById('pnfSearch');
  const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
  if (q) {{
    list = list.filter(item => item.pnf.toLowerCase().includes(q));
  }}

  // Sorting
  list.sort((a, b) => {{
    let vA = pnfSortCol === 0 ? a.pnf : pnfSortCol === 1 ? a.total : pnfSortCol === 2 ? a.ap : pnfSortCol === 3 ? a.rep : a.pct;
    let vB = pnfSortCol === 0 ? b.pnf : pnfSortCol === 1 ? b.total : pnfSortCol === 2 ? b.ap : pnfSortCol === 3 ? b.rep : b.pct;
    if (typeof vA === 'string') return pnfSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
    return pnfSortAsc ? vA - vB : vB - vA;
  }});

  const tbody = document.getElementById('pnfTableBody');
  if (tbody) {{
    if (!list.length) {{
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:24px;color:#94a3b8">No se encontraron registros de PNF.</td></tr>';
    }} else {{
      tbody.innerHTML = list.map(item => `
        <tr>
          <td><strong style="color:#0f172a">${{escapeHTML(item.pnf)}}</strong></td>
          <td><span style="font-weight:700">${{item.total}}</span></td>
          <td style="color:#10b981;font-weight:600">${{item.ap}}</td>
          <td style="color:#ef4444;font-weight:600">${{item.rep}}</td>
          <td>
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-weight:700;width:38px">${{item.pct}}%</span>
              <div style="flex:1;height:6px;background:#e2e8f0;border-radius:3px;overflow:hidden;min-width:60px">
                <div style="width:${{item.pct}}%;height:100%;background:${{item.pct>=60 ? '#10b981' : '#ef4444'}};border-radius:3px"></div>
              </div>
            </div>
          </td>
          <td>
            <span class="badge badge-${{item.pct>=60 ? 'aprobado' : 'reprobado'}}">
              <span class="dot"></span>${{item.pct>=60 ? 'Óptimo' : 'Bajo'}}
            </span>
          </td>
        </tr>
      `).join('');
    }}
  }}

  // Update side cards
  const allPNFs = getPNFData();
  if (allPNFs.length > 0) {{
    const sortedByPct = [...allPNFs].filter(p => p.total >= 5).sort((a,b) => b.pct - a.pct);
    const top = sortedByPct[0] || allPNFs[0];
    const bot = sortedByPct[sortedByPct.length - 1] || allPNFs[allPNFs.length - 1];
    const avg = Math.round(allPNFs.reduce((acc, p) => acc + p.pct, 0) / allPNFs.length);

    const topName = document.getElementById('pnfTopName');
    const topPct  = document.getElementById('pnfTopPct');
    const botName = document.getElementById('pnfBotName');
    const botPct  = document.getElementById('pnfBotPct');
    const avgPct  = document.getElementById('pnfAvgPct');
    const pnfCount = document.getElementById('pnfCount');

    if (topName) topName.textContent = top.pnf;
    if (topPct)  topPct.textContent = top.pct + '% aprobación (' + top.total + ' estudiantes)';
    if (botName) botName.textContent = bot.pnf;
    if (botPct)  botPct.textContent = bot.pct + '% aprobación (' + bot.total + ' estudiantes)';
    if (avgPct)  avgPct.textContent = avg + '%';
    if (pnfCount) pnfCount.textContent = allPNFs.length;
  }}
}}

function filtrarPNF() {{
  renderPNFTable();
}}

function sortPNF(col) {{
  if (pnfSortCol === col) pnfSortAsc = !pnfSortAsc;
  else {{ pnfSortCol = col; pnfSortAsc = false; }}
  renderPNFTable();
}}

// ── VISTA DE NÚCLEOS & TABLA GENERAL ─────────────────────────────────────────
function filtrarTabla() {{
  const fNucleo   = document.getElementById('filtroNucleo')?.value.toLowerCase().trim() || '';
  const fPNF      = document.getElementById('filtroPNF')?.value.toLowerCase().trim() || '';
  const fTrayecto = document.getElementById('filtroTrayecto')?.value.trim() || '';
  const fEstatus  = document.getElementById('filtroEstatus')?.value.trim() || '';
  const fToken    = document.getElementById('filtroToken')?.value.toLowerCase().trim() || '';

  const filtrados = DB.estudiantes.filter(e => {{
    if (fNucleo && (e.nucleo || '').toLowerCase() !== fNucleo) return false;
    if (fPNF && (e.pnf || '').toLowerCase() !== fPNF) return false;
    if (fTrayecto && (e.trayecto || '') !== fTrayecto) return false;
    if (fEstatus && (e.estatus || '') !== fEstatus) return false;
    if (fToken && !(e.token || '').toLowerCase().includes(fToken)) return false;
    return true;
  }});

  // Actualizar estadísticas de la tabla
  const ap = filtrados.filter(e => e.estatus === 'Aprobado').length;
  const rep = filtrados.filter(e => e.estatus === 'Reprobado').length;
  const pct = filtrados.length ? Math.round((ap / filtrados.length) * 100) : 0;

  const tableStats = document.getElementById('tableStats');
  if (tableStats) {{
    tableStats.innerHTML = `
      <div class="table-stat-pill">Total: <strong style="color:#6366f1">${{filtrados.length}}</strong></div>
      <div class="table-stat-pill">Aprobados (≥ 60): <strong style="color:#10b981">${{ap}}</strong></div>
      <div class="table-stat-pill">Reprobados (&lt; 60): <strong style="color:#ef4444">${{rep}}</strong></div>
      <div class="table-stat-pill">Rendimiento: <strong style="color:#f59e0b">${{pct}}%</strong></div>
    `;
  }}

  // Renderizar filas (limitadas a 300 para fluidez en DOM si no hay filtro)
  const tbody = document.getElementById('tablaBody');
  if (tbody) {{
    if (!filtrados.length) {{
      tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:32px;color:#94a3b8">No se encontraron estudiantes con los filtros seleccionados.</td></tr>';
    }} else {{
      const limit = filtrados.length > 500 ? 500 : filtrados.length;
      const rows = filtrados.slice(0, limit).map(e => `
        <tr data-id="${{e.id}}">
          <td class="col-check">
            <label class="custom-check">
              <input type="checkbox" class="row-check" value="${{e.id}}" onchange="actualizarBulkBar()" />
              <span class="checkmark"></span>
            </label>
          </td>
          <td><strong>${{escapeHTML(e.cedula)}}</strong></td>
          <td>${{escapeHTML(e.nombre)}}</td>
          <td>${{escapeHTML(e.nucleo || '—')}}</td>
          <td><span style="font-size:12px;color:#475569">${{escapeHTML(e.pnf || '—')}}</span></td>
          <td><span class="badge" style="background:#f1f5f9;color:#334155">${{escapeHTML(e.trayecto || '—')}}</span></td>
          <td><span class="rpt-token-badge">${{escapeHTML(e.token || '—')}}</span></td>
          <td>
            <span class="badge badge-${{e.estatus === 'Aprobado' ? 'aprobado' : 'reprobado'}}">
              <span class="dot"></span>${{e.puntaje !== undefined && e.puntaje !== null ? e.puntaje + ' pts · ' : ''}}${{escapeHTML(e.estatus || '—')}}
            </span>
          </td>
          <td>
            <div style="display:flex;gap:4px">
              <button class="btn-icon" onclick="editarEstudiante('${{e.id}}')" title="Editar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button class="btn-icon" onclick="eliminarEstudiante('${{e.id}}')" title="Eliminar" style="color:#ef4444">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/></svg>
              </button>
            </div>
          </td>
        </tr>
      `).join('');
      tbody.innerHTML = rows + (filtrados.length > 500 ? `<tr><td colspan="9" style="text-align:center;padding:12px;color:#94a3b8;font-size:12px">Mostrando primeros 500 de ${{filtrados.length}} estudiantes. Usa los filtros para refinar.</td></tr>` : '');
    }}
  }}
  actualizarBulkBar();
}}

function limpiarFiltros() {{
  ['filtroNucleo', 'filtroPNF', 'filtroTrayecto', 'filtroEstatus', 'filtroToken'].forEach(id => {{
    const el = document.getElementById(id);
    if (el) el.value = '';
  }});
  filtrarTabla();
}}

// ── Acciones de selección masiva ────────────────────────────────────────────
function toggleSelectAll(master) {{
  document.querySelectorAll('.row-check').forEach(chk => chk.checked = master.checked);
  actualizarBulkBar();
}}

function actualizarBulkBar() {{
  const checked = document.querySelectorAll('.row-check:checked');
  const bar = document.getElementById('bulkBar');
  const countEl = document.getElementById('bulkCount');
  if (bar && countEl) {{
    countEl.textContent = checked.length;
    bar.style.display = checked.length > 0 ? 'flex' : 'none';
  }}
}}

function deseleccionarTodo() {{
  document.querySelectorAll('.row-check, #checkAll').forEach(chk => chk.checked = false);
  actualizarBulkBar();
}}

function confirmarEliminarSeleccionados() {{
  const checked = Array.from(document.querySelectorAll('.row-check:checked')).map(c => c.value);
  if (!checked.length) return;
  modal('Eliminar Estudiantes', `¿Deseas eliminar permanentemente los ${{checked.length}} estudiantes seleccionados?`, () => {{
    DB.estudiantes = DB.estudiantes.filter(e => !checked.includes(String(e.id)));
    guardarDB();
    toast(`${{checked.length}} estudiante(s) eliminados.`, 'success');
    filtrarTabla();
  }});
}}

function confirmarBorrarTodo() {{
  modal('⚠️ Borrar toda la base de datos', '¿Estás absolutamente seguro de eliminar todos los registros del sistema? Esta acción no se puede deshacer.', () => {{
    DB.estudiantes = [];
    guardarDB();
    toast('Todos los datos han sido borrados.', 'success');
    filtrarTabla();
    renderDashboard();
  }});
}}

// ── Formulario de Registro / Edición de Estudiante ──────────────────────────
function guardarEstudiante(e) {{
  if (e) e.preventDefault();
  const editId   = document.getElementById('editId')?.value;
  const cedula   = document.getElementById('cedula')?.value.trim();
  const nombre   = document.getElementById('nombre')?.value.trim();
  const nucleo   = document.getElementById('nucleo')?.value;
  const pnf      = document.getElementById('pnf')?.value;
  const trayecto = document.getElementById('trayecto')?.value;
  const token    = document.getElementById('token')?.value.trim();
  const estatus  = document.getElementById('estatus')?.value;

  if (!cedula || !nombre || !nucleo || !pnf || !trayecto || !estatus) {{
    toast('Por favor completa todos los campos requeridos (*).', 'error');
    return;
  }}

  if (editId) {{
    const idx = DB.estudiantes.findIndex(est => String(est.id) === String(editId));
    if (idx !== -1) {{
      DB.estudiantes[idx] = {{ ...DB.estudiantes[idx], cedula, nombre, nucleo, pnf, trayecto, token, estatus }};
      toast('Estudiante actualizado exitosamente.', 'success');
    }}
  }} else {{
    const nuevo = {{
      id: String(DB.nextId++),
      cedula, nombre, nucleo, pnf, trayecto, token, estatus
    }};
    DB.estudiantes.unshift(nuevo);
    toast('Estudiante registrado exitosamente.', 'success');
  }}

  guardarDB();
  limpiarFormulario();
  poblarSelects();
  showView('nucleos');
}}

function editarEstudiante(id) {{
  const est = DB.estudiantes.find(e => String(e.id) === String(id));
  if (!est) return;

  showView('estudiantes');
  document.getElementById('editId').value = est.id;
  document.getElementById('cedula').value = est.cedula;
  document.getElementById('nombre').value = est.nombre;
  document.getElementById('nucleo').value = est.nucleo;
  document.getElementById('pnf').value = est.pnf;
  document.getElementById('trayecto').value = est.trayecto;
  document.getElementById('token').value = est.token || '';
  document.getElementById('estatus').value = est.estatus;

  const btn = document.getElementById('btnGuardar');
  if (btn) btn.innerHTML = '💾 Actualizar Estudiante';
}}

function eliminarEstudiante(id) {{
  modal('Eliminar Registro', '¿Seguro que deseas eliminar este estudiante?', () => {{
    DB.estudiantes = DB.estudiantes.filter(e => String(e.id) !== String(id));
    guardarDB();
    toast('Registro eliminado.', 'success');
    filtrarTabla();
    renderDashboard();
  }});
}}

function limpiarFormulario() {{
  const form = document.getElementById('formEstudiante');
  if (form) form.reset();
  const editId = document.getElementById('editId');
  if (editId) editId.value = '';
  const btn = document.getElementById('btnGuardar');
  if (btn) btn.innerHTML = '💾 Guardar Estudiante';
}}

function renderRecientes() {{
  const tbody = document.getElementById('recentBody');
  if (!tbody) return;
  const recientes = DB.estudiantes.slice(0, 10);
  if (!recientes.length) {{
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:16px;color:#94a3b8">Sin registros recientes.</td></tr>';
    return;
  }}
  tbody.innerHTML = recientes.map(e => `
    <tr>
      <td><strong>${{escapeHTML(e.cedula)}}</strong></td>
      <td>${{escapeHTML(e.nombre)}}</td>
      <td>${{escapeHTML(e.nucleo || '—')}}</td>
      <td>${{escapeHTML(e.pnf || '—')}}</td>
      <td><span class="badge badge-${{e.estatus==='Aprobado'?'aprobado':'reprobado'}}">${{escapeHTML(e.estatus)}}</span></td>
    </tr>
  `).join('');
}}

// ── REPORTES: NÚCLEO › PNF › TOKEN ──────────────────────────────────────────
function generarReporte() {{
  const fNucleo = document.getElementById('reporteNucleo')?.value.toLowerCase().trim() || '';
  const fPNF    = document.getElementById('reportePNF')?.value.toLowerCase().trim() || '';
  const fToken  = document.getElementById('reporteToken')?.value.toLowerCase().trim() || '';

  const filtrados = DB.estudiantes.filter(e => {{
    if (fNucleo && (e.nucleo || '').toLowerCase() !== fNucleo) return false;
    if (fPNF && (e.pnf || '').toLowerCase() !== fPNF) return false;
    if (fToken && !(e.token || '').toLowerCase().includes(fToken)) return false;
    return true;
  }});

  const container = document.getElementById('reporteContainer');
  if (!container) return;

  if (!filtrados.length) {{
    container.innerHTML = '<div style="text-align:center;padding:48px;color:#94a3b8;background:#fff;border-radius:14px;border:1px solid #e2e8f0">No hay datos que coincidan con los filtros de reporte.</div>';
    return;
  }}

  // Agrupar por Núcleo
  const grupos = {{}};
  filtrados.forEach(e => {{
    const n = e.nucleo || 'Sin Núcleo';
    if (!grupos[n]) grupos[n] = [];
    grupos[n].push(e);
  }});

  container.innerHTML = Object.entries(grupos).map(([nucleo, ests]) => {{
    const ap = ests.filter(e => e.estatus === 'Aprobado').length;
    const rep = ests.filter(e => e.estatus === 'Reprobado').length;
    const pct = ests.length ? Math.round((ap / ests.length) * 100) : 0;

    // Sub-agrupar por PNF
    const pnfs = {{}};
    ests.forEach(e => {{
      const p = e.pnf || 'Sin PNF';
      if (!pnfs[p]) pnfs[p] = [];
      pnfs[p].push(e);
    }});

    const pnfBlocks = Object.entries(pnfs).map(([pnfName, pnfEsts]) => {{
      const pAp = pnfEsts.filter(e => e.estatus === 'Aprobado').length;
      const pRep = pnfEsts.filter(e => e.estatus === 'Reprobado').length;
      const pPct = pnfEsts.length ? Math.round((pAp / pnfEsts.length) * 100) : 0;

      // Tokens dentro de este PNF
      const tokens = Array.from(new Set(pnfEsts.map(e => e.token || 'Sin Token'))).sort();
      const tokenPills = tokens.map(tok => {{
        const count = pnfEsts.filter(e => (e.token || 'Sin Token') === tok).length;
        return `<span class="rpt-token-badge" style="margin:2px">${{escapeHTML(tok)}} (${{count}})</span>`;
      }}).join('');

      return `
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;margin-top:8px">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
            <strong style="color:#0f172a;font-size:14px">${{escapeHTML(pnfName)}}</strong>
            <div style="display:flex;gap:6px">
              <span class="rpt-pill ap">${{pAp}} Aprobados</span>
              <span class="rpt-pill rep">${{pRep}} Reprobados</span>
              <span class="rpt-pill" style="background:#e0e7ff;color:#3730a3;font-weight:700">${{pPct}}%</span>
            </div>
          </div>
          <div style="margin-top:8px;font-size:12px;color:#64748b">
            Tokens evaluados: ${{tokenPills}}
          </div>
        </div>
      `;
    }}).join('');

    return `
      <div class="rpt-nucleo-card">
        <div class="rpt-nucleo-header">
          <div>
            <span class="rpt-nucleo-title">📍 ${{escapeHTML(nucleo)}}</span>
            <span style="font-size:13px;color:#64748b;margin-left:8px">${{ests.length}} estudiantes</span>
          </div>
          <div style="display:flex;gap:8px">
            <span class="rpt-pill ap">✓ ${{ap}} Aprobados</span>
            <span class="rpt-pill rep">✗ ${{rep}} Reprobados</span>
            <span class="rpt-pill" style="background:${{pct>=60?'#d1fae5':'#fee2e2'}};color:${{pct>=60?'#065f46':'#991b1b'}};font-weight:700">${{pct}}% Aprobación</span>
          </div>
        </div>
        ${{pnfBlocks}}
      </div>
    `;
  }}).join('');
}}

// ── CALENDARIO EPA ──────────────────────────────────────────────────────────
const CALENDARIO_DATA = [
  {{ dia: 'Miércoles 04 Nov', sedes: 'Caracas, Amazonas, Anzoátegui, Apure, Aragua, Barinas, Bolívar', fecha: '2026-11-04', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Jueves 05 Nov',    sedes: 'Carabobo, Cojedes, Delta Amacuro, Falcón, Guárico, La Guaira, Lara', fecha: '2026-11-05', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Viernes 06 Nov',   sedes: 'Mérida, Miranda (Valles del Tuy, Barlovento, Guarenas), Monagas', fecha: '2026-11-06', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Lunes 09 Nov',     sedes: 'Nueva Esparta, Portuguesa, Sucre, Táchira, Trujillo, Yaracuy, Zulia', fecha: '2026-11-09', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Martes 10 Nov',    sedes: 'Sedes Especiales y Núcleos Metropolitanos', fecha: '2026-11-10', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Miércoles 11 Nov', sedes: 'Cierre 1ª Convocatoria', fecha: '2026-11-11', trayectos: 'Inicial, I, II' }},
  {{ dia: 'Jueves 12 Nov',    sedes: '2ª Convocatoria · Todos los Núcleos', fecha: '2026-11-12', trayectos: 'III, IV' }},
  {{ dia: 'Viernes 13 Nov',   sedes: '2ª Convocatoria · Todos los Núcleos', fecha: '2026-11-13', trayectos: 'III, IV' }},
  {{ dia: 'Lunes 16 Nov',     sedes: '2ª Convocatoria · Evaluaciones Avanzadas', fecha: '2026-11-16', trayectos: 'III, IV' }},
  {{ dia: 'Martes 17 Nov',    sedes: '2ª Convocatoria · Cierre Trayectos III y IV', fecha: '2026-11-17', trayectos: 'III, IV' }},
  {{ dia: 'Miércoles 18 Nov', sedes: '🚨 JORNADA ESPECIAL FINAL DE REZAGADOS Y REPROBADOS', fecha: '2026-11-18', trayectos: 'Todos los Trayectos' }}
];

function renderCalendario() {{
  const grid = document.getElementById('calGrid');
  if (!grid) return;

  grid.innerHTML = CALENDARIO_DATA.map(d => `
    <div class="cal-day ${{d.fecha === '2026-11-18' ? 'alert-rezagados' : ''}}" style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
      <div style="font-size:12px;font-weight:700;color:#800020;text-transform:uppercase;letter-spacing:0.05em">${{d.dia}}</div>
      <div style="font-size:14px;font-weight:700;color:#0f172a;margin:6px 0">${{d.sedes}}</div>
      <div style="font-size:12px;color:#64748b;display:flex;align-items:center;gap:6px">
        <span class="badge" style="background:#f1f5f9;color:#334155">${{d.trayectos}}</span>
        <span>Aplica a todos los PNF</span>
      </div>
    </div>
  `).join('');
}}

function limpiarFiltrosCalendario() {{
  ['calFiltroNucleo', 'calFiltroPNF', 'calFiltroTrayecto'].forEach(id => {{
    const el = document.getElementById(id);
    if (el) el.value = '';
  }});
  renderCalendario();
}}

// ── IMPORTAR EXCEL (CON REGLA: >= 60 PTS = APROBADO) ────────────────────────
function dragOver(e) {{ e.preventDefault(); e.currentTarget.classList.add('drag-over'); }}
function dragLeave(e) {{ e.currentTarget.classList.remove('drag-over'); }}
function dropFile(e) {{
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  if (e.dataTransfer && e.dataTransfer.files) {{
    Array.from(e.dataTransfer.files).forEach(f => procesarArchivo(f));
  }}
}}

function handleFileSelect(e) {{
  if (e.target && e.target.files) {{
    Array.from(e.target.files).forEach(f => procesarArchivo(f));
    e.target.value = '';
  }}
}}

function procesarArchivo(file) {{
  const ext = file.name.split('.').pop().toLowerCase();
  if (!['xlsx', 'xls', 'csv'].includes(ext)) {{
    toast('Formato no compatible. Por favor sube archivos .xlsx, .xls o .csv', 'error');
    return;
  }}

  const reader = new FileReader();
  reader.onload = ev => {{
    try {{
      const workbook = XLSX.read(new Uint8Array(ev.target.result), {{ type: 'array' }});
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
      const json = XLSX.utils.sheet_to_json(firstSheet, {{ defval: '' }});

      if (!json.length) {{
        toast(`El archivo "${{file.name}}" está vacío.`, 'error');
        return;
      }}

      if (!excelRows.length) {{
        excelHeaders = Object.keys(json[0]);
      }}

      excelRows = [...excelRows, ...json];
      archivosImportados.push({{ nombre: file.name, filas: json.length }});

      mostrarMapeo(archivosImportados.map(a => a.nombre).join(' + '), excelRows.length);
      toast(`"${{file.name}}" cargado (${{json.length}} filas). Total: ${{excelRows.length}} filas.`, 'success');
    }} catch (err) {{
      toast('Error al leer el archivo: ' + err.message, 'error');
    }}
  }};
  reader.readAsArrayBuffer(file);
}}

function mostrarMapeo(nombreArchivo, totalFilas) {{
  const dropzone = document.getElementById('dropzone');
  const importConfig = document.getElementById('importConfig');
  const fileInfo = document.getElementById('importFileInfo');
  const listaEl = document.getElementById('archivos-cargados-lista');

  if (dropzone) dropzone.style.display = 'none';
  if (importConfig) importConfig.style.display = 'block';

  // Lista de archivos con chips
  if (listaEl && archivosImportados.length) {{
    listaEl.style.display = 'block';
    listaEl.innerHTML = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;">' +
      archivosImportados.map(a =>
        `<span style="background:rgba(16,185,129,0.12);color:#065f46;border:1px solid #6ee7b7;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;">✓ ${{escapeHTML(a.nombre)}} (${{a.filas}} filas)</span>`
      ).join('') +
      '<button onclick="resetImport()" style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;border-radius:20px;padding:4px 12px;font-size:12px;cursor:pointer;font-weight:600">✕ Limpiar todo</button>' +
      '</div>';
  }}

  if (fileInfo) {{
    fileInfo.innerHTML = `
      <div style="font-weight:700;font-size:15px;color:#0f172a">${{escapeHTML(nombreArchivo)}}</div>
      <div style="font-size:13px;color:#64748b">${{totalFilas.toLocaleString()}} filas de datos encontradas</div>
    `;
  }}

  // Construir selectores de columnas con autodetección inteligente
  const colMapper = document.getElementById('colMapper');
  if (colMapper) {{
    colMapper.innerHTML = CAMPOS_SISTEMA.map(c => {{
      const match = autodetectarColumna(c.key);
      const options = ['<option value="">(No mapear)</option>']
        .concat(excelHeaders.map(h => `<option value="${{escapeHTML(h)}}" ${{h === match ? 'selected' : ''}}>${{escapeHTML(h)}}</option>`))
        .join('');

      return `
        <div class="col-mapper-row" style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f1f5f9">
          <div>
            <strong style="font-size:13px;color:#1e293b">${{escapeHTML(c.label)}}</strong>
            ${{c.req ? '<span style="color:#ef4444;margin-left:4px">*</span>' : ''}}
          </div>
          <select id="map_${{c.key}}" style="padding:6px 12px;border:1px solid #cbd5e1;border-radius:8px;font-size:13px;min-width:240px">
            ${{options}}
          </select>
        </div>
      `;
    }}).join('');
  }}

  // Vista previa
  const preview = document.getElementById('previewSection');
  if (preview && excelRows.length) {{
    const previewRows = excelRows.slice(0, 5);
    const headersHTML = excelHeaders.map(h => `<th style="padding:8px 12px;font-size:11px;background:#f8fafc">${{escapeHTML(h)}}</th>`).join('');
    const rowsHTML = previewRows.map(r => `
      <tr>${{excelHeaders.map(h => `<td style="padding:6px 12px;font-size:12px">${{escapeHTML(String(r[h] ?? ''))}}</td>`).join('')}}</tr>
    `).join('');

    preview.innerHTML = `
      <h4 style="font-size:13px;font-weight:700;margin-bottom:8px">Vista previa de las primeras filas:</h4>
      <div style="overflow-x:auto;max-height:180px;border:1px solid #e2e8f0;border-radius:8px">
        <table class="data-table" style="font-size:12px;width:100%">
          <thead><tr>${{headersHTML}}</tr></thead>
          <tbody>${{rowsHTML}}</tbody>
        </table>
      </div>
    `;
  }}
}}

function autodetectarColumna(campo) {{
  const lowerHeaders = excelHeaders.map(h => h.toLowerCase().trim());
  const synonyms = {{
    cedula:   ['cedula', 'cédula', 'ci', 'identificacion', 'documento', 'ced'],
    nombre:   ['nombre', 'estudiante', 'apellidos y nombres', '1er nombre', 'alumno'],
    nucleo:   ['nucleo', 'núcleo', 'sede', 'centro', 'nombre de la evaluación', 'evaluacion'],
    pnf:      ['carrera', 'pnf', 'programa', 'especialidad', 'malla'],
    trayecto: ['trayecto', 'tray', 'nivel', 'semestre', 'año'],
    token:    ['token', 'codigo', 'código', 'id evaluación', 'eval'],
    estatus:  ['pts', 'puntos', 'puntaje', 'calificacion', 'nota', 'aprobado', 'estatus', 'estado', 'resultado'],
    puntaje:  ['pts', 'puntos', 'puntaje', 'nota', 'score']
  }};

  const targets = synonyms[campo] || [campo];
  for (const t of targets) {{
    const idx = lowerHeaders.findIndex(h => h === t || h.includes(t));
    if (idx !== -1) return excelHeaders[idx];
  }}
  return '';
}}

function ejecutarImportacion() {{
  const mapeo = {{}};
  CAMPOS_SISTEMA.forEach(c => {{
    const sel = document.getElementById('map_' + c.key);
    mapeo[c.key] = sel ? sel.value : '';
  }});

  // Validaciones mínimas
  if (!mapeo.cedula) {{ toast('Debes seleccionar la columna de Cédula.', 'error'); return; }}
  if (!mapeo.estatus && !mapeo.puntaje) {{ toast('Debes seleccionar la columna de Pts o Estatus.', 'error'); return; }}

  const importados = [];

  excelRows.forEach((row, idx) => {{
    const cedula = String(row[mapeo.cedula] || '').trim();
    if (!cedula) return;

    // Nombre
    let nombre = mapeo.nombre ? String(row[mapeo.nombre] || '').trim() : '';
    // Si viene partido en 1er Nombre, 2do Nombre, etc.
    if (!nombre || nombre === '') {{
      const nom1 = String(row['1er Nombre'] || '').trim();
      const nom2 = String(row['2do Nombre'] || '').trim();
      const ap1  = String(row['1er Apellido'] || '').trim();
      const ap2  = String(row['2do Apellido'] || '').trim();
      if (nom1 || ap1) nombre = `${{nom1}} ${{nom2}} ${{ap1}} ${{ap2}}`.replace(/\\s+/g, ' ').trim();
    }}
    if (!nombre) nombre = 'Estudiante ' + cedula;

    // Pts y Estatus (Regla: >= 60 pts = Aprobado, < 60 = Reprobado)
    let pts = null;
    const ptsRaw = mapeo.puntaje ? row[mapeo.puntaje] : (mapeo.estatus ? row[mapeo.estatus] : null);
    if (ptsRaw !== null && ptsRaw !== undefined && String(ptsRaw).trim() !== '') {{
      const parsedNum = parseFloat(String(ptsRaw).replace(',', '.'));
      if (!isNaN(parsedNum)) pts = parsedNum;
    }}

    let estatus = 'Aprobado';
    if (pts !== null) {{
      estatus = pts >= 60 ? 'Aprobado' : 'Reprobado';
    }} else {{
      const valStr = String(row[mapeo.estatus] || '').toLowerCase().trim();
      if (['reprobado', 'reprobada', 'false', '0', 'no', 'r'].includes(valStr)) estatus = 'Reprobado';
      else estatus = 'Aprobado';
    }}

    // Núcleo y PNF
    let evalStr = mapeo.nucleo ? String(row[mapeo.nucleo] || '').trim() : '';
    let carrera = mapeo.pnf ? String(row[mapeo.pnf] || '').trim() : '';
    let trayecto = mapeo.trayecto ? String(row[mapeo.trayecto] || '').trim() : '';
    let token = mapeo.token ? String(row[mapeo.token] || '').trim() : '';

    // Si la carrera viene en blanco o la evaluación indica CP -> Ciencias Policiales
    let pnf = carrera;
    if (!pnf || pnf === '' || evalStr.toUpperCase().includes(' CP ')) {{
      pnf = 'Ciencias Policiales';
    }}

    // Detección de trayecto desde evaluación si está vacío
    if (!trayecto || trayecto === '') {{
      if (/\\bT1\\b/i.test(evalStr)) trayecto = 'I';
      else if (/\\bT2\\b/i.test(evalStr)) trayecto = 'II';
      else if (/\\bT3\\b/i.test(evalStr)) trayecto = 'III';
      else if (/\\bT4\\b/i.test(evalStr)) trayecto = 'IV';
      else if (/\\bTI\\b/i.test(evalStr)) trayecto = 'Inicial';
      else trayecto = 'I';
    }}

    // Limpieza de nombre de núcleo
    let nucleo = evalStr
      .replace(/\\b(T[0-9I]+|SP|IPCR|IP|CF|PCAD|EPH|CP|MN)\\b/gi, '')
      .replace(/\\s+/g, ' ')
      .trim();
    if (!nucleo) nucleo = 'Caracas';

    importados.push({{
      id: String(DB.nextId++),
      cedula,
      nombre,
      nucleo,
      pnf,
      trayecto,
      token,
      estatus,
      puntaje: pts
    }});
  }});

  if (!importados.length) {{
    toast('No se pudieron extraer registros válidos.', 'error');
    return;
  }}

  // Agregar al inicio
  DB.estudiantes = [...importados, ...DB.estudiantes];
  guardarDB();
  resetImport();
  poblarSelects();

  toast(`✅ ${{importados.length}} estudiante(s) importados exitosamente.`, 'success');
  showView('dashboard');
}}

function resetImport() {{
  excelRows = [];
  excelHeaders = [];
  archivosImportados = [];
  const dropzone = document.getElementById('dropzone');
  const importConfig = document.getElementById('importConfig');
  const listaEl = document.getElementById('archivos-cargados-lista');
  const fileInput = document.getElementById('fileInput');

  if (dropzone) dropzone.style.display = 'flex';
  if (importConfig) importConfig.style.display = 'none';
  if (listaEl) listaEl.style.display = 'none';
  if (fileInput) fileInput.value = '';
}}

// ── EXPORTACIÓN CSV ─────────────────────────────────────────────────────────
function exportarCSV() {{
  if (!DB.estudiantes.length) {{
    toast('No hay datos para exportar.', 'error');
    return;
  }}

  const headers = ['Cédula', 'Nombre', 'Núcleo', 'PNF', 'Trayecto', 'Token', 'Estatus', 'Puntaje'];
  const rows = DB.estudiantes.map(e => [
    `"${{(e.cedula || '').replace(/"/g, '""')}}"`,
    `"${{(e.nombre || '').replace(/"/g, '""')}}"`,
    `"${{(e.nucleo || '').replace(/"/g, '""')}}"`,
    `"${{(e.pnf || '').replace(/"/g, '""')}}"`,
    `"${{(e.trayecto || '').replace(/"/g, '""')}}"`,
    `"${{(e.token || '').replace(/"/g, '""')}}"`,
    `"${{(e.estatus || '').replace(/"/g, '""')}}"`,
    `"${{e.puntaje !== undefined && e.puntaje !== null ? e.puntaje : ''}}"`
  ].join(','));

  const csvContent = '\\uFEFF' + [headers.join(','), ...rows].join('\\r\\n');
  const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `UNES_EPA_Estudiantes_${{new Date().toISOString().slice(0,10)}}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  toast('Archivo CSV generado y descargado.', 'success');
}}

// ── INSTRUCTIVO SCROLL ──────────────────────────────────────────────────────
function instScroll(id, linkEl) {{
  const target = document.getElementById(id);
  if (target) {{
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
  document.querySelectorAll('.inst-toc-link').forEach(l => l.classList.remove('active'));
  if (linkEl) linkEl.classList.add('active');
  return false;
}}

// ── UTILIDADES DE UI (MODAL & TOAST) ────────────────────────────────────────
function modal(title, message, onConfirm) {{
  const overlay = document.getElementById('modalOverlay');
  const titleEl = document.getElementById('modalTitle');
  const bodyEl = document.getElementById('modalBody');
  const confirmBtn = document.getElementById('modalConfirm');

  if (!overlay) {{
    if (confirm(message)) onConfirm();
    return;
  }}

  titleEl.textContent = title;
  bodyEl.textContent = message;
  overlay.style.display = 'flex';

  confirmBtn.onclick = () => {{
    cerrarModal();
    if (onConfirm) onConfirm();
  }};
}}

function cerrarModal() {{
  const overlay = document.getElementById('modalOverlay');
  if (overlay) overlay.style.display = 'none';
}}

function toast(message, type = 'info') {{
  let container = document.getElementById('toastContainer');
  if (!container) {{
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }}

  const toastEl = document.createElement('div');
  toastEl.className = `toast toast-${{type}}`;
  toastEl.innerHTML = `<span>${{escapeHTML(message)}}</span>`;
  container.appendChild(toastEl);

  setTimeout(() => {{
    toastEl.classList.add('toast-fade');
    setTimeout(() => toastEl.remove(), 300);
  }}, 3500);
}}

function escapeHTML(str) {{
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}}

function initEventListeners() {{
  // Cerrar modal al hacer clic afuera
  const overlay = document.getElementById('modalOverlay');
  if (overlay) {{
    overlay.addEventListener('click', (e) => {{
      if (e.target === overlay) cerrarModal();
    }});
  }}
}}
"""

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print('app.js created successfully with all functionality!')
print(f'File size: {len(js_code)//1024} KB')
