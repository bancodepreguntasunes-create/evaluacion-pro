// =============================================
// EPA - app.js  · Evaluación de Progreso Académico
// =============================================

// ──────────────────────────────────────────
//  ESTADO GLOBAL
// ──────────────────────────────────────────
let DB = { estudiantes: [], nextId: 1 };
let charts = {};
let deleteTargetId = null;

let excelRows    = [];
let excelHeaders = [];
let mappingMode  = 'replace';

// Campos del sistema (incluyendo Token)
const CAMPOS_SISTEMA = [
  { key: 'cedula',   label: 'Cédula',   keywords: ['cedula','ci','documento','id','identidad','cedula'] },
  { key: 'nombre',   label: 'Nombre',   keywords: ['nombre','apellido','estudiante','participante','alumno'] },
  { key: 'nucleo',   label: 'Núcleo',   keywords: ['nucleo','nucleo','sede','extension','lugar'] },
  { key: 'pnf',      label: 'PNF',      keywords: ['pnf','programa','carrera','mencion'] },
  { key: 'trayecto', label: 'Trayecto', keywords: ['trayecto','semestre','nivel','periodo'] },
  { key: 'token',    label: 'Token',    keywords: ['token','codigo','clave','prueba','evaluacion','code','key'] },
  { key: 'estatus',  label: 'Estatus',  keywords: ['estatus','status','resultado','condicion','situacion'] }
];

// ──────────────────────────────────────────
//  INICIALIZACIÓN
// ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  cargarDB();
  poblarSelectores();
  renderDashboard();
  renderTabla();
  renderRecientes();
  generarReporte();
});

// ──────────────────────────────────────────
//  PERSISTENCIA
// ──────────────────────────────────────────
function cargarDB() {
  const raw = localStorage.getItem('epa_db_v1');
  if (raw) {
    try { DB = JSON.parse(raw); } catch(e) { DB = { estudiantes: [], nextId: 1 }; }
  } else {
    DB = { estudiantes: [], nextId: 1 };
    guardarDB();
  }
}

function guardarDB() {
  localStorage.setItem('epa_db_v1', JSON.stringify(DB));
}

// ──────────────────────────────────────────
//  SELECTORES
// ──────────────────────────────────────────
function poblarSelectores() {
  ['filtroNucleo', 'nucleo', 'reporteNucleo'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    const ph = sel.options[0]?.textContent || '';
    sel.innerHTML = `<option value="">${ph || (id==='nucleo' ? 'Seleccionar núcleo...' : 'Todos los núcleos')}</option>`;
    NUCLEOS.forEach(n => { const o=document.createElement('option'); o.value=n; o.textContent=n; sel.appendChild(o); });
  });

  ['filtroPNF', 'pnf', 'reportePNF'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    const ph = sel.options[0]?.textContent || '';
    sel.innerHTML = `<option value="">${ph || (id==='pnf' ? 'Seleccionar PNF...' : 'Todos los PNF')}</option>`;
    PNF_LIST.forEach(p => { const o=document.createElement('option'); o.value=p.id; o.textContent=p.corto; sel.appendChild(o); });
  });
}

// ──────────────────────────────────────────
//  NAVEGACIÓN
// ──────────────────────────────────────────
function showView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const viewEl = document.getElementById('view-' + viewId);
  const navEl  = document.getElementById('nav-' + viewId);
  if (viewEl) viewEl.classList.add('active');
  if (navEl)  navEl.classList.add('active');
  const titles = {
    dashboard:  'Dashboard – EPA',
    nucleos:    'Listado por Núcleo',
    estudiantes:'Registro de Estudiantes',
    reportes:   'Reportes: Núcleo › PNF › Token',
    importar:   'Importar desde Excel'
  };
  document.getElementById('topbarTitle').textContent = titles[viewId] || viewId;
  if (viewId === 'dashboard')   renderDashboard();
  if (viewId === 'nucleos')     filtrarTabla();
  if (viewId === 'estudiantes') renderRecientes();
  if (viewId === 'reportes')    generarReporte();
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('collapsed');
  document.getElementById('main').classList.toggle('sidebar-collapsed');
}

// ──────────────────────────────────────────
//  DASHBOARD
// ──────────────────────────────────────────
function renderDashboard() {
  const est = DB.estudiantes;
  const total        = est.length;
  const aprobados    = est.filter(e => e.estatus === 'Aprobado').length;
  const reprobados   = est.filter(e => e.estatus === 'Reprobado').length;
  const nucleosAct   = new Set(est.map(e => e.nucleo)).size;
  const tokensAct    = new Set(est.map(e => e.token).filter(Boolean)).size;
  const pct = total ? Math.round((aprobados/total)*100) : 0;

  const statsData = [
    { label:'Total Estudiantes', value: total,       icon: iconUsers(),   color:'#b82352', bg:'rgba(184,35,82,0.15)' },
    { label:'Aprobados',         value: aprobados,   icon: iconCheck(),   color:'#10b981', bg:'rgba(16,185,129,0.15)' },
    { label:'Reprobados',        value: reprobados,  icon: iconX(),       color:'#e11d48', bg:'rgba(225,29,72,0.15)'  },
    { label:'% Aprobación',      value: pct + '%',   icon: iconBar(),     color:'#d97706', bg:'rgba(217,119,6,0.15)' },
    { label:'Núcleos Activos',   value: nucleosAct,  icon: iconMap(),     color:'#94a3b8', bg:'rgba(148,163,184,0.15)' },
    { label:'Tokens Registrados',value: tokensAct,   icon: iconKey(),     color:'#800020', bg:'rgba(128,0,32,0.2)' }
  ];

  const grid = document.getElementById('statsGrid');

  if (!total) {
    grid.innerHTML = `
      <div class="empty-dashboard" style="grid-column:1/-1">
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17,8 12,3 7,8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          <h3>Bienvenido a EPA</h3>
          <p>No hay datos cargados todavía.<br>Ve a <strong>Importar Excel</strong> para cargar tu archivo de resultados.</p>
          <button class="btn-primary" style="margin-top:20px" onclick="showView('importar')">
            📥 Importar Excel ahora
          </button>
        </div>
      </div>`;
    ['pnf','trayecto','nucleos'].forEach(k => { if(charts[k]){charts[k].destroy();charts[k]=null;} });
    return;
  }

  grid.innerHTML = statsData.map(s => `
    <div class="stat-card" style="--card-color:${s.color}; --card-color-bg:${s.bg}">
      <div class="stat-icon">${s.icon}</div>
      <div class="stat-info">
        <div class="stat-value">${s.value}</div>
        <div class="stat-label">${s.label}</div>
      </div>
    </div>
  `).join('');

  renderCharts(est);
}

// SVG helpers
const iconUsers = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>`;
const iconCheck= () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20,6 9,17 4,12"/></svg>`;
const iconX    = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;
const iconBar  = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>`;
const iconMap  = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>`;
const iconKey  = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 11-7.778 7.778 5.5 5.5 0 017.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>`;
const iconBook = () => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>`;

// ──────────────────────────────────────────
//  GRÁFICAS
// ──────────────────────────────────────────
function renderCharts(est) {
  const tickStyle   = { color:'#a1a1aa', font:{ family:'Inter', size:11 } };
  const gridStyle   = { color:'rgba(255,255,255,0.05)' };
  const legendStyle = { color:'#a1a1aa', font:{ family:'Inter', size:12 } };

  // Chart 1: Aprobados/Reprobados por PNF
  const pnfAp  = PNF_LIST.map(p => est.filter(e=>e.pnf===p.id&&e.estatus==='Aprobado').length);
  const pnfRep = PNF_LIST.map(p => est.filter(e=>e.pnf===p.id&&e.estatus==='Reprobado').length);
  if (charts.pnf) charts.pnf.destroy();
  charts.pnf = new Chart(document.getElementById('chartPNF'), {
    type:'bar',
    data:{ labels: PNF_LIST.map(p=>p.corto), datasets:[
      { label:'Aprobados',  data:pnfAp,  backgroundColor:'rgba(16,185,129,0.85)', borderRadius:6 },
      { label:'Reprobados', data:pnfRep, backgroundColor:'rgba(184,35,82,0.85)',  borderRadius:6 }
    ]},
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ labels:legendStyle } },
      scales:{ x:{ ticks:{...tickStyle,maxRotation:45}, grid:gridStyle },
               y:{ ticks:tickStyle, grid:gridStyle, beginAtZero:true } }
    }
  });

  // Chart 2: Distribución por Trayecto (dona)
  if (charts.trayecto) charts.trayecto.destroy();
  charts.trayecto = new Chart(document.getElementById('chartTrayecto'), {
    type:'doughnut',
    data:{ labels: TRAYECTOS.map(t=>'Trayecto '+t),
      datasets:[{ data: TRAYECTOS.map(t=>est.filter(e=>e.trayecto===t).length),
        backgroundColor:['#800020','#b82352','#9e1b42','#71717a','#52525b'],
        borderWidth:0, hoverOffset:8 }]
    },
    options:{ responsive:true, maintainAspectRatio:false, cutout:'65%',
      plugins:{ legend:{ labels:legendStyle, position:'right' } }
    }
  });

  // Chart 3: Top 10 Núcleos
  const nc = {}; est.forEach(e=>{ nc[e.nucleo]=(nc[e.nucleo]||0)+1; });
  const sorted = Object.entries(nc).sort((a,b)=>b[1]-a[1]).slice(0,10);
  const unesPalette = ['#800020','#8b1538','#9e1b42','#b82352','#c93667','#64748b','#71717a','#52525b','#3f3f46','#27272a'];
  if (charts.nucleos) charts.nucleos.destroy();
  charts.nucleos = new Chart(document.getElementById('chartNucleos'), {
    type:'bar',
    data:{ labels:sorted.map(e=>e[0]),
      datasets:[{ label:'Matrícula', data:sorted.map(e=>e[1]),
        backgroundColor:sorted.map((_,i)=>unesPalette[i % unesPalette.length]), borderRadius:6 }]
    },
    options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ display:false } },
      scales:{ x:{ ticks:tickStyle, grid:gridStyle, beginAtZero:true },
               y:{ ticks:tickStyle, grid:gridStyle } }
    }
  });
}

// ──────────────────────────────────────────
//  TABLA / FILTROS
// ──────────────────────────────────────────
function filtrarTabla() {
  const fN = document.getElementById('filtroNucleo').value;
  const fP = document.getElementById('filtroPNF').value;
  const fT = document.getElementById('filtroTrayecto').value;
  const fE = document.getElementById('filtroEstatus').value;
  const fTk= document.getElementById('filtroToken')?.value?.trim().toUpperCase() || '';

  let data = DB.estudiantes;
  if (fN)  data = data.filter(e => e.nucleo   === fN);
  if (fP)  data = data.filter(e => e.pnf      === fP);
  if (fT)  data = data.filter(e => e.trayecto === fT);
  if (fE)  data = data.filter(e => e.estatus  === fE);
  if (fTk) data = data.filter(e => (e.token||'').toUpperCase().includes(fTk));

  const ap  = data.filter(e=>e.estatus==='Aprobado').length;
  const rep = data.filter(e=>e.estatus==='Reprobado').length;

  document.getElementById('tableStats').innerHTML = `
    <div class="table-stat-pill">Total: <span>${data.length}</span></div>
    <div class="table-stat-pill">Aprobados: <span style="color:#34d399">${ap}</span></div>
    <div class="table-stat-pill">Reprobados: <span style="color:#fb7185">${rep}</span></div>`;

  renderTablaRows(data, 'tablaBody');
}

function renderTabla() { filtrarTabla(); }

function renderTablaRows(data, bodyId) {
  const tbody = document.getElementById(bodyId);
  if (!tbody) return;
  if (!data.length) {
    tbody.innerHTML = `<tr><td colspan="9">
      <div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <h3>Sin resultados</h3>
        <p>No hay estudiantes con los filtros seleccionados.<br>
           Usa <strong>Importar Excel</strong> para cargar tus datos en EPA.</p>
      </div>
    </td></tr>`;
    return;
  }

  tbody.innerHTML = data.map(e => {
    const pnf    = PNF_LIST.find(p => p.id === e.pnf);
    const isMain = bodyId === 'tablaBody';
    return `<tr data-id="${e.id}"${isMain ? ` onclick="toggleRowCheck(this)"` : ''}>
      ${isMain ? `<td class="col-check" onclick="event.stopPropagation()">
        <label class="custom-check">
          <input type="checkbox" class="row-cb" data-id="${e.id}" onchange="actualizarBulkBar()">
          <span class="checkmark"></span>
        </label>
      </td>` : ''}
      <td>${escHTML(e.cedula)}</td>
      <td>${escHTML(e.nombre)}</td>
      <td>${escHTML(e.nucleo)}</td>
      <td><span class="badge badge-pnf">${pnf ? escHTML(pnf.corto) : escHTML(e.pnf)}</span></td>
      <td><span class="badge badge-trayecto">${escHTML(e.trayecto)}</span></td>
      <td><span class="badge badge-token">${escHTML(e.token || '—')}</span></td>
      <td><span class="badge badge-${e.estatus==='Aprobado'?'aprobado':'reprobado'}">
            <span class="dot"></span>${escHTML(e.estatus)}</span></td>
      <td onclick="event.stopPropagation()">
        <button class="btn-edit" onclick="editarEstudiante('${e.id}')" title="Editar">✏️</button>
        <button class="btn-del"  onclick="confirmarEliminar('${e.id}')" title="Eliminar">🗑️</button>
      </td>
    </tr>`;
  }).join('');
}

function limpiarFiltros() {
  ['filtroNucleo','filtroPNF','filtroTrayecto','filtroEstatus'].forEach(id => {
    document.getElementById(id).value = '';
  });
  const ftk = document.getElementById('filtroToken');
  if (ftk) ftk.value = '';
  filtrarTabla();
}

// ──────────────────────────────────────────
//  FORMULARIO DE ESTUDIANTE
// ──────────────────────────────────────────
function guardarEstudiante(e) {
  e.preventDefault();
  const id      = document.getElementById('editId').value;
  const cedula  = document.getElementById('cedula').value.trim();
  const nombre  = document.getElementById('nombre').value.trim();
  const nucleo  = document.getElementById('nucleo').value;
  const pnf     = document.getElementById('pnf').value;
  const trayecto= document.getElementById('trayecto').value;
  const token   = document.getElementById('token').value.trim();
  const estatus = document.getElementById('estatus').value;

  if (!cedula||!nombre||!nucleo||!pnf||!trayecto||!estatus) {
    toast('Completa todos los campos obligatorios.', 'error'); return;
  }
  const dup = DB.estudiantes.find(s => s.cedula===cedula && s.id!==id);
  if (dup) { toast('Ya existe un estudiante con esa cédula.', 'error'); return; }

  if (id) {
    const idx = DB.estudiantes.findIndex(s => s.id===id);
    if (idx!==-1) DB.estudiantes[idx] = {id,cedula,nombre,nucleo,pnf,trayecto,token,estatus};
    toast('Estudiante actualizado.', 'success');
  } else {
    DB.estudiantes.push({ id:String(DB.nextId++), cedula, nombre, nucleo, pnf, trayecto, token, estatus });
    toast('Estudiante registrado.', 'success');
  }
  guardarDB(); limpiarFormulario(); renderRecientes();
}

function limpiarFormulario() {
  ['editId','cedula','nombre','nucleo','pnf','trayecto','token','estatus'].forEach(id => {
    const el = document.getElementById(id); if (el) el.value = '';
  });
  document.getElementById('btnGuardar').innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><polyline points="17,21 17,13 7,13 7,21"/><polyline points="7,3 7,8 15,8"/></svg>
    Guardar Estudiante`;
}

function editarEstudiante(id) {
  const e = DB.estudiantes.find(s => s.id===id);
  if (!e) return;
  showView('estudiantes');
  setTimeout(() => {
    document.getElementById('editId').value   = e.id;
    document.getElementById('cedula').value   = e.cedula;
    document.getElementById('nombre').value   = e.nombre;
    document.getElementById('nucleo').value   = e.nucleo;
    document.getElementById('pnf').value      = e.pnf;
    document.getElementById('trayecto').value = e.trayecto;
    document.getElementById('token').value    = e.token || '';
    document.getElementById('estatus').value  = e.estatus;
    document.getElementById('btnGuardar').innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><polyline points="17,21 17,13 7,13 7,21"/><polyline points="7,3 7,8 15,8"/></svg>
      Actualizar Estudiante`;
    document.getElementById('cedula').focus();
  }, 50);
}

function renderRecientes() {
  const recent = [...DB.estudiantes].reverse().slice(0, 10);
  renderTablaRows(recent, 'recentBody');
}

// ──────────────────────────────────────────
//  IMPORTAR EXCEL
// ──────────────────────────────────────────
function dragOver(e) { e.preventDefault(); document.getElementById('dropzone').classList.add('drag-over'); }
function dragLeave()  { document.getElementById('dropzone').classList.remove('drag-over'); }
function dropFile(e)  {
  e.preventDefault(); document.getElementById('dropzone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0]; if (file) procesarArchivo(file);
}
function handleFileSelect(e) { const file=e.target.files[0]; if(file) procesarArchivo(file); }

function procesarArchivo(file) {
  const ext = file.name.split('.').pop().toLowerCase();
  if (!['xlsx','xls','csv'].includes(ext)) { toast('Usa .xlsx, .xls o .csv','error'); return; }
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const workbook = XLSX.read(new Uint8Array(ev.target.result), {type:'array'});
      const json = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], {defval:''});
      if (!json.length) { toast('El archivo está vacío.','error'); return; }
      excelRows    = json;
      excelHeaders = Object.keys(json[0]);
      mostrarMapeo(file.name, json.length);
    } catch(err) { toast('Error al leer: '+err.message,'error'); }
  };
  reader.readAsArrayBuffer(file);
}

function autodetectarColumna(campo) {
  return excelHeaders.find(h => {
    const hn = h.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    return campo.keywords.some(k => hn.includes(k));
  }) || '';
}

function mostrarMapeo(fileName, rowCount) {
  document.getElementById('dropzone').style.display = 'none';
  document.getElementById('importConfig').style.display = 'block';
  document.getElementById('importFileInfo').innerHTML = `
    <span style="font-size:14px;font-weight:600;color:#f1f5f9">📄 ${escHTML(fileName)}</span>
    <span style="font-size:13px;color:#94a3b8;margin-left:12px">${rowCount} filas · ${excelHeaders.length} columnas</span>`;

  const mapper = document.getElementById('colMapper');
  mapper.innerHTML = CAMPOS_SISTEMA.map(campo => {
    const auto = autodetectarColumna(campo);
    const opts = excelHeaders.map(h=>`<option value="${escHTML(h)}"${h===auto?' selected':''}>${escHTML(h)}</option>`).join('');
    const isOptional = campo.key === 'token';
    return `
      <div class="mapper-row">
        <div class="mapper-field">
          <span class="mapper-label">${campo.label}</span>
          <span class="mapper-required" style="${isOptional?'color:#f59e0b':''}">${isOptional?'opcional':'requerido'}</span>
        </div>
        <div class="mapper-arrow">→</div>
        <select class="mapper-select" id="map_${campo.key}">
          <option value="">-- ${isOptional?'Omitir':'No mapear'} --</option>
          ${opts}
        </select>
        ${auto ? `<span class="mapper-auto">✓ auto</span>` : `<span class="mapper-manual">seleccionar</span>`}
      </div>`;
  }).join('');

  mapper.innerHTML += `
    <div class="mapper-row mapper-mode">
      <div class="mapper-field"><span class="mapper-label">Modo de importación</span></div>
      <div class="mapper-arrow">→</div>
      <select class="mapper-select" id="modoImport" onchange="mappingMode=this.value">
        <option value="replace">Reemplazar todos los datos existentes</option>
        <option value="append">Agregar al final (mantener existentes)</option>
      </select>
    </div>`;
  mostrarPrevia();
}

function mostrarPrevia() {
  const preview  = document.getElementById('previewSection');
  const muestra  = excelRows.slice(0,5);
  const colsHTML = excelHeaders.map(h=>`<th>${escHTML(h)}</th>`).join('');
  const rowsHTML = muestra.map(row=>`<tr>${excelHeaders.map(h=>`<td>${escHTML(String(row[h]||''))}</td>`).join('')}</tr>`).join('');
  preview.innerHTML = `
    <h3 class="section-title">Vista previa (primeras 5 filas)</h3>
    <div class="table-wrapper" style="max-height:220px;overflow:auto">
      <table class="data-table"><thead><tr>${colsHTML}</tr></thead><tbody>${rowsHTML}</tbody></table>
    </div>`;
}

function resetImport() {
  excelRows=[]; excelHeaders=[];
  document.getElementById('dropzone').style.display='';
  document.getElementById('importConfig').style.display='none';
  document.getElementById('previewSection').innerHTML='';
  document.getElementById('fileInput').value='';
}

function ejecutarImportacion() {
  const mapeo={};
  const faltantes=[];
  CAMPOS_SISTEMA.forEach(c => {
    const sel=document.getElementById('map_'+c.key);
    mapeo[c.key]=sel?sel.value:'';
    if (!sel?.value && c.key!=='token') faltantes.push(c.label);
  });
  if (faltantes.length) { toast('Asigna columnas para: '+faltantes.join(', '),'error'); return; }

  const modo = document.getElementById('modoImport')?.value||'replace';
  const importados=[], errores=[], pnfMap=construirMapaPNF();

  excelRows.forEach((row,idx) => {
    const cedula   = String(row[mapeo.cedula]   ||'').trim();
    const nombre   = String(row[mapeo.nombre]   ||'').trim();
    const nucleo   = normalizarNucleo(String(row[mapeo.nucleo]   ||'').trim());
    const pnfRaw   = String(row[mapeo.pnf]      ||'').trim();
    const trayecto = normalizarTrayecto(String(row[mapeo.trayecto]||'').trim());
    const token    = mapeo.token ? String(row[mapeo.token]||'').trim() : '';
    const estatus  = normalizarEstatus(String(row[mapeo.estatus] ||'').trim());
    const pnfId    = pnfMap(pnfRaw);

    if (!cedula||!nombre) { errores.push(`Fila ${idx+2}: vacíos`); return; }
    if (!trayecto) errores.push(`Fila ${idx+2} (${cedula}): trayecto inválido`);
    if (!estatus)  errores.push(`Fila ${idx+2} (${cedula}): estatus inválido`);

    importados.push({ id:String(DB.nextId++), cedula, nombre,
      nucleo: nucleo||String(row[mapeo.nucleo]||'').trim(),
      pnf:    pnfId ||pnfRaw,
      trayecto: trayecto||String(row[mapeo.trayecto]||'').trim(),
      token,
      estatus: estatus||String(row[mapeo.estatus]||'').trim()
    });
  });

  if (modo==='replace') { DB.estudiantes=importados; DB.nextId=importados.length+1; }
  else DB.estudiantes=[...DB.estudiantes,...importados];

  guardarDB(); resetImport();
  let msg=`✅ ${importados.length} estudiante(s) importados.`;
  if (errores.length) msg+=` ⚠️ ${errores.length} advertencia(s).`;
  toast(msg,'success');
  if (errores.length) console.warn(errores.join('\n'));
  setTimeout(()=>showView('dashboard'),600);
}

// Normalizaciones
function normalizarTrayecto(val) {
  const v=val.toUpperCase().trim();
  if (['INICIAL','TRAYECTO INICIAL','0','TRAY. INICIAL','TRAY INICIAL'].includes(v)) return 'Inicial';
  if (['I','1','TRAYECTO I','TRAY. I','TRAY I'].includes(v)) return 'I';
  if (['II','2','TRAYECTO II','TRAY. II'].includes(v)) return 'II';
  if (['III','3','TRAYECTO III','TRAY. III'].includes(v)) return 'III';
  if (['IV','4','TRAYECTO IV','TRAY. IV'].includes(v)) return 'IV';
  return '';
}
function normalizarEstatus(val) {
  const v=val.toUpperCase().trim();
  if (['APROBADO','APROBADA','AP','A','1','SI','APRO'].some(x=>v.includes(x))) return 'Aprobado';
  if (['REPROBADO','REPROBADA','REP','R','0','NO'].some(x=>v.includes(x))) return 'Reprobado';
  return '';
}
function normalizarNucleo(val) {
  const v=val.toUpperCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  return NUCLEOS.find(n => { const nn=n.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,''); return nn===v||nn.includes(v)||v.includes(nn); })||val;
}
function construirMapaPNF() {
  return raw => {
    const v=raw.toUpperCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const f=PNF_LIST.find(p => {
      const pn=p.nombre.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
      const pc=p.corto.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
      return pn.includes(v)||v.includes(pn.substring(0,8))||pc.includes(v)||v.includes(pc.substring(0,6));
    });
    return f?f.id:'';
  };
}

// ──────────────────────────────────────────
//  REPORTES: NÚCLEO → PNF → TOKEN
// ──────────────────────────────────────────
function generarReporte() {
  const fN  = document.getElementById('reporteNucleo')?.value || '';
  const fP  = document.getElementById('reportePNF')?.value    || '';
  const fTk = document.getElementById('reporteToken')?.value?.trim().toUpperCase() || '';

  let base = DB.estudiantes;
  if (fN)  base = base.filter(e => e.nucleo === fN);
  if (fP)  base = base.filter(e => e.pnf    === fP);
  if (fTk) base = base.filter(e => (e.token||'').toUpperCase().includes(fTk));

  const container = document.getElementById('reporteContainer');
  if (!container) return;

  if (!base.length) {
    container.innerHTML = `
      <div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14,2 14,8 20,8"/></svg>
        <h3>Sin datos para reportar</h3>
        <p>Importa tu archivo Excel o ajusta los filtros.</p>
        <button class="btn-primary" style="margin-top:16px" onclick="showView('importar')">📥 Importar Excel</button>
      </div>`;
    return;
  }

  // Jerarquía: Núcleo → PNF → Token
  const nucleos = [...new Set(base.map(e=>e.nucleo))].sort();

  container.innerHTML = nucleos.map(nucleo => {
    const estNucleo = base.filter(e=>e.nucleo===nucleo);
    const pnfsAct   = PNF_LIST.filter(p=>estNucleo.some(e=>e.pnf===p.id));
    const totN = estNucleo.length;
    const apN  = estNucleo.filter(e=>e.estatus==='Aprobado').length;
    const repN = totN - apN;
    const pctN = totN ? Math.round((apN/totN)*100) : 0;

    const pnfBlocks = pnfsAct.map(pnf => {
      const estPNF  = estNucleo.filter(e=>e.pnf===pnf.id);
      const tokens  = [...new Set(estPNF.map(e=>e.token||'SIN TOKEN'))].sort();
      const totPNF  = estPNF.length;
      const apPNF   = estPNF.filter(e=>e.estatus==='Aprobado').length;
      const repPNF  = totPNF-apPNF;

      const tokenRows = tokens.map(tok => {
        const estTok = estPNF.filter(e=>(e.token||'SIN TOKEN')===tok);
        const apTok  = estTok.filter(e=>e.estatus==='Aprobado').length;
        const repTok = estTok.length-apTok;
        const pctTok = estTok.length ? Math.round((apTok/estTok.length)*100) : 0;
        const barW   = pctTok;
        const barColor = pctTok>=60 ? '#10b981' : pctTok>=40 ? '#f59e0b' : '#f43f5e';

        return `
          <tr class="token-row">
            <td class="tok-name">
              <span class="badge badge-token">${escHTML(tok)}</span>
            </td>
            <td class="tok-total">${estTok.length}</td>
            <td class="tok-ap"><span style="color:#34d399;font-weight:700">${apTok}</span></td>
            <td class="tok-rep"><span style="color:#fb7185;font-weight:700">${repTok}</span></td>
            <td class="tok-pct">
              <div class="pct-bar-wrap">
                <div class="pct-bar-fill" style="width:${barW}%;background:${barColor}"></div>
              </div>
              <span class="pct-label" style="color:${barColor}">${pctTok}%</span>
            </td>
          </tr>`;
      }).join('');

      return `
        <div class="rpt-pnf-block" style="--pnf-color:${pnf.color}">
          <div class="rpt-pnf-header">
            <div class="rpt-pnf-name">
              <span class="pnf-dot" style="background:${pnf.color}"></span>
              ${escHTML(pnf.nombre)}
            </div>
            <div class="rpt-pnf-summary">
              <span class="rpt-pill">${totPNF} est.</span>
              <span class="rpt-pill ap">${apPNF} aprobados</span>
              <span class="rpt-pill rep">${repPNF} reprobados</span>
            </div>
          </div>
          <table class="token-table">
            <thead>
              <tr>
                <th>Token de Evaluación</th>
                <th>Total</th>
                <th>✅ Aprobados</th>
                <th>❌ Reprobados</th>
                <th>% Aprobación</th>
              </tr>
            </thead>
            <tbody>${tokenRows}</tbody>
          </table>
        </div>`;
    }).join('');

    return `
      <div class="rpt-nucleo-block">
        <div class="rpt-nucleo-header">
          <div class="rpt-nucleo-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;flex-shrink:0"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${escHTML(nucleo)}
          </div>
          <div class="rpt-nucleo-stats">
            <div class="rpt-stat-chip">${totN} <small>total</small></div>
            <div class="rpt-stat-chip ap">${apN} <small>aprobados</small></div>
            <div class="rpt-stat-chip rep">${repN} <small>reprobados</small></div>
            <div class="rpt-stat-chip pct" style="--pct:${pctN}%">${pctN}% <small>aprob.</small></div>
          </div>
        </div>
        <div class="rpt-nucleo-body">
          ${pnfBlocks || '<p style="color:#475569;font-size:13px;padding:16px">Sin PNF registrados.</p>'}
        </div>
      </div>`;
  }).join('');
}

// ──────────────────────────────────────────
//  ELIMINAR / BULK / BORRAR TODO
// ──────────────────────────────────────────
function confirmarEliminar(id) {
  const e=DB.estudiantes.find(s=>s.id===id); if(!e) return;
  deleteTargetId=id;
  document.getElementById('modalTitle').textContent='Eliminar estudiante';
  document.getElementById('modalBody').innerHTML=`
    ¿Seguro que deseas eliminar a <strong style="color:#f1f5f9">${escHTML(e.nombre)}</strong>?
    <br><br><small style="color:#f43f5e">Esta acción no se puede deshacer.</small>`;
  document.getElementById('modalConfirm').onclick=ejecutarEliminar;
  document.getElementById('modalOverlay').classList.add('open');
}
function ejecutarEliminar() {
  DB.estudiantes=DB.estudiantes.filter(s=>s.id!==deleteTargetId);
  guardarDB(); cerrarModal(); filtrarTabla(); renderRecientes();
  toast('Estudiante eliminado.','info'); deleteTargetId=null;
}
function cerrarModal() { document.getElementById('modalOverlay').classList.remove('open'); }

// Selección masiva
function toggleRowCheck(row) {
  const cb=row.querySelector('.row-cb'); if(!cb) return;
  cb.checked=!cb.checked; row.classList.toggle('row-selected',cb.checked); actualizarBulkBar();
}
function toggleSelectAll(masterCb) {
  document.querySelectorAll('.row-cb').forEach(cb=>{
    cb.checked=masterCb.checked;
    const row=cb.closest('tr'); if(row) row.classList.toggle('row-selected',masterCb.checked);
  }); actualizarBulkBar();
}
function actualizarBulkBar() {
  const sel=document.querySelectorAll('.row-cb:checked');
  const tot=document.querySelectorAll('.row-cb').length;
  const bar=document.getElementById('bulkBar');
  const masterCb=document.getElementById('checkAll');
  document.getElementById('bulkCount').textContent=sel.length;
  bar.style.display=sel.length>0?'flex':'none';
  if(masterCb){ masterCb.indeterminate=sel.length>0&&sel.length<tot; masterCb.checked=sel.length===tot&&tot>0; }
}
function deseleccionarTodo() {
  const m=document.getElementById('checkAll'); if(m){m.checked=false;m.indeterminate=false;}
  document.querySelectorAll('.row-cb').forEach(cb=>{ cb.checked=false; const r=cb.closest('tr'); if(r) r.classList.remove('row-selected'); });
  document.getElementById('bulkBar').style.display='none';
}
function confirmarEliminarSeleccionados() {
  const ids=[...document.querySelectorAll('.row-cb:checked')].map(cb=>cb.dataset.id);
  if(!ids.length) return;
  document.getElementById('modalTitle').textContent='Eliminar seleccionados';
  document.getElementById('modalBody').innerHTML=`Eliminarás <strong style="color:#fb7185">${ids.length} estudiante(s)</strong>.<br><br><small style="color:#f43f5e">Irreversible.</small>`;
  document.getElementById('modalConfirm').onclick=()=>ejecutarEliminarSeleccionados(ids);
  document.getElementById('modalOverlay').classList.add('open');
}
function ejecutarEliminarSeleccionados(ids) {
  const set=new Set(ids); DB.estudiantes=DB.estudiantes.filter(s=>!set.has(s.id));
  guardarDB(); cerrarModal(); deseleccionarTodo(); filtrarTabla(); renderRecientes();
  toast(`${ids.length} estudiante(s) eliminados.`,'info');
}
function confirmarBorrarTodo() {
  if(!DB.estudiantes.length){toast('No hay datos que borrar.','error');return;}
  document.getElementById('modalTitle').textContent='⚠️ Borrar toda la base de datos';
  document.getElementById('modalBody').innerHTML=`
    ¿Estás <strong style="color:#fb7185">TOTALMENTE SEGURO</strong>?<br><br>
    Se eliminarán <strong style="color:#f1f5f9">${DB.estudiantes.length} registros</strong> de EPA.<br><br>
    <small style="color:#f43f5e">⚠️ Irreversible. Los datos no se recuperan.</small>`;
  document.getElementById('modalConfirm').onclick=ejecutarBorrarTodo;
  document.getElementById('modalOverlay').classList.add('open');
}
function ejecutarBorrarTodo() {
  const tot=DB.estudiantes.length; DB.estudiantes=[]; DB.nextId=1;
  guardarDB(); cerrarModal(); deseleccionarTodo(); filtrarTabla(); renderRecientes(); renderDashboard();
  toast(`Base limpiada. ${tot} registros eliminados.`,'info');
}

// CSV Export
function exportarCSV() {
  if(!DB.estudiantes.length){toast('No hay datos para exportar.','error');return;}
  const cols=['Cédula','Nombre','Núcleo','PNF','Trayecto','Token','Estatus'];
  const rows=DB.estudiantes.map(e=>{
    const pnf=PNF_LIST.find(p=>p.id===e.pnf);
    return [e.cedula,e.nombre,e.nucleo,pnf?pnf.nombre:e.pnf,e.trayecto,e.token||'',e.estatus].map(csvEsc).join(',');
  });
  const blob=new Blob(['\uFEFF'+[cols.join(','),...rows].join('\r\n')],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download='EPA_resultados_'+new Date().toISOString().slice(0,10)+'.csv';
  a.click(); toast('CSV exportado.','success');
}
function csvEsc(val){const s=String(val??'');return s.includes(',')||s.includes('"')||s.includes('\n')?`"${s.replace(/"/g,'""')}"`:s;}

// Toast
function toast(msg,type='info'){
  const icons={success:'✅',error:'❌',info:'ℹ️'};
  const el=document.createElement('div'); el.className=`toast ${type}`;
  el.innerHTML=`<span class="toast-icon">${icons[type]}</span><span>${escHTML(msg)}</span>`;
  document.getElementById('toastContainer').appendChild(el);
  setTimeout(()=>{el.style.opacity='0';el.style.transform='translateX(40px)';el.style.transition='0.3s';setTimeout(()=>el.remove(),300);},4000);
}

function escHTML(str){return String(str??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
