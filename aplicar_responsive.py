import re

# 1. Actualizar styles.css
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

responsive_css = '''
/* ==========================================================================
   DISEÑO 100% RESPONSIVO PARA CELULAR (MÓVIL), TABLET Y COMPUTADOR (DESKTOP)
   ========================================================================== */

/* Backdrop semitransparente para menú en celulares */
.sidebar-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 998;
  transition: opacity 0.3s ease;
}
.sidebar-backdrop.active {
  display: block;
}

/* Fila de 6 tarjetas métricas base */
.stats-row {
  display: grid !important;
  grid-template-columns: repeat(6, 1fr) !important;
  gap: 12px;
  margin-bottom: 16px;
  width: 100%;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-width: 0;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* Sección de Mapa interactivo base */
.map-section {
  display: grid !important;
  grid-template-columns: 1fr 340px !important;
  gap: 14px;
  align-items: stretch;
  margin-bottom: 16px;
  width: 100%;
}

.map-left {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 440px;
}

.map-container {
  padding: 8px;
  background: linear-gradient(160deg, #e8f0fe 0%, #f0f7ff 50%, #f8fafc 100%);
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

#venezuelaMap {
  width: 100%;
  height: auto;
  max-height: 480px;
}

.map-right {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Gráficos del dashboard base */
.dash-charts {
  display: grid !important;
  grid-template-columns: 1fr 280px !important;
  grid-template-rows: auto auto !important;
  gap: 14px;
  margin-bottom: 16px;
  width: 100%;
}

/* PANTALLAS GRANDES Y MEDIANAS (TABLETS HORIZONTALES / LAPTOPS <= 1200px) */
@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 10px;
  }
  .map-section {
    grid-template-columns: 1fr 310px !important;
  }
}

/* TABLETS (<= 992px) */
@media (max-width: 992px) {
  .map-section {
    grid-template-columns: 1fr !important;
  }
  .map-left {
    min-height: 400px;
  }
  .map-right {
    width: 100%;
  }
  .dash-charts {
    grid-template-columns: 1fr !important;
    grid-template-rows: auto !important;
  }
  .dash-chart-main,
  .dash-chart-right,
  .dash-chart-bottom {
    grid-column: 1 !important;
    grid-row: auto !important;
  }
  .chart-card {
    height: 300px;
  }
}

/* TELÉFONOS CELULARES (<= 768px) */
@media (max-width: 768px) {
  /* Sidebar móvil off-canvas (se desliza suavemente sobre la pantalla) */
  .sidebar {
    position: fixed !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 270px !important;
    transform: translateX(-100%) !important;
    z-index: 1000 !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
  }
  .sidebar.mobile-open {
    transform: translateX(0) !important;
  }
  .sidebar .sidebar-logo-img {
    max-height: 36px;
  }
  .sidebar .nav-item span,
  .sidebar .sidebar-footer {
    opacity: 1 !important;
    display: inline-block !important;
    pointer-events: auto !important;
  }

  /* Contenido principal ocupa 100% sin margen izquierdo */
  .main-content {
    margin-left: 0 !important;
    width: 100% !important;
  }
  .main-content.sidebar-collapsed {
    margin-left: 0 !important;
  }

  /* Topbar compacta en celular */
  .topbar {
    padding: 0 12px !important;
    gap: 8px !important;
    height: 54px !important;
  }
  .topbar-toggle {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    padding: 0;
  }
  .topbar-title {
    font-size: 14px !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }
  .topbar-actions {
    gap: 6px;
  }
  .topbar-actions .btn-secondary {
    padding: 6px 10px !important;
    font-size: 11px !important;
  }
  .topbar-actions .btn-text-full {
    display: none !important;
  }
  .topbar-unes-img {
    height: 26px !important;
  }

  /* Padding adaptado en vistas móviles */
  .view {
    padding: 12px 10px 48px 10px !important;
  }

  /* 6 tarjetas organizadas en 2 columnas x 3 filas */
  .stats-row {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    margin-bottom: 12px !important;
  }
  .stat-card {
    padding: 10px 10px !important;
    gap: 10px !important;
    border-radius: 10px !important;
  }
  .stat-icon {
    width: 32px !important;
    height: 32px !important;
    border-radius: 6px !important;
    flex-shrink: 0;
  }
  .stat-icon svg {
    width: 16px !important;
    height: 16px !important;
  }
  .stat-value {
    font-size: 16px !important;
    font-weight: 800 !important;
  }
  .stat-label {
    font-size: 10px !important;
  }

  /* Mapa ajustado a pantalla de celular */
  .map-left {
    min-height: 330px !important;
  }
  .map-header {
    padding: 8px 12px !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 6px !important;
  }
  .map-header h3 {
    font-size: 12px !important;
  }
  .map-header p {
    font-size: 10px !important;
  }
  .map-legend {
    font-size: 10px !important;
    gap: 4px 8px !important;
    padding: 6px 10px !important;
  }

  /* Gráficas en celular */
  .chart-card {
    height: 250px !important;
    padding: 12px !important;
  }
  .chart-header h3 {
    font-size: 13px !important;
  }

  /* Tablas adaptables con scroll horizontal táctil */
  .table-card-header {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
  }
  .table-actions {
    width: 100% !important;
  }
  .table-actions input {
    width: 100% !important;
  }
  .table-wrapper {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .data-table {
    font-size: 12px !important;
    min-width: 580px;
  }
  .data-table th,
  .data-table td {
    padding: 7px 8px !important;
  }

  /* Formularios y filtros */
  .filters-bar,
  .filter-row {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
  }
  .filters-bar select,
  .filters-bar input,
  .filter-row select,
  .filter-row input {
    width: 100% !important;
  }

  .col-mapper-row {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 6px !important;
  }
  .col-mapper-row select {
    width: 100% !important;
    min-width: 100% !important;
  }
}

/* CELULARES PEQUEÑOS (<= 400px) */
@media (max-width: 400px) {
  .stats-row {
    grid-template-columns: 1fr 1fr !important;
    gap: 6px !important;
  }
  .stat-card {
    padding: 8px !important;
    gap: 6px !important;
  }
  .stat-value {
    font-size: 15px !important;
  }
}
'''

# Agregar al final de styles.css
if 'RESPONSIVE DESIGN (DESKTOP, TABLET, CELULARES / MÓVILES)' not in css:
    css += '\n' + responsive_css
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("styles.css actualizado con diseño responsivo completo!")
else:
    print("El diseño responsivo ya estaba presente en styles.css.")

# 2. Actualizar index.html para incluir el backdrop y clases de texto responsivas
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inyectar backdrop para móvil
if 'sidebarBackdrop' not in html:
    html = html.replace('<body>', '<body>\n  <!-- Backdrop oscuro para celulares al abrir menú lateral -->\n  <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebar()"></div>')
    print("Inyectado sidebarBackdrop en index.html.")

# Asegurar que el botón de restablecer datos tenga la clase .btn-text-full para ocultarse en móvil
html = re.sub(
    r'<button class="btn-secondary" onclick="restablecerDatos\(\)"[^>]*>.*?Restablecer Datos.*?</button>',
    '''<button class="btn-secondary" onclick="restablecerDatos()" style="font-size:12px;padding:6px 12px;display:inline-flex;align-items:center;gap:6px;background:rgba(239,68,68,0.1);color:#b91c1c;border:1px solid rgba(239,68,68,0.3);border-radius:6px;cursor:pointer;font-weight:600;" title="Restablecer a datos oficiales verificados">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          <span class="btn-text-full">Restablecer Datos</span>
        </button>''',
    html,
    flags=re.DOTALL
)

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html guardado con ajustes móviles.")

# 3. Actualizar unes_sistema_final.js y app.js con manejo inteligente de sidebar móvil
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Reemplazar toggleSidebar por versión compatible móvil y escritorio
old_toggle_start = js.find('function toggleSidebar() {')
old_toggle_end = js.find('}', old_toggle_start) + 1

new_toggle_js = '''function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const main = document.getElementById('main');
  const backdrop = document.getElementById('sidebarBackdrop');
  const isMobile = window.innerWidth <= 768;

  if (isMobile) {
    if (sidebar) {
      const isOpen = sidebar.classList.toggle('mobile-open');
      if (backdrop) backdrop.classList.toggle('active', isOpen);
    }
  } else {
    if (sidebar && main) {
      sidebar.classList.toggle('collapsed');
      main.classList.toggle('sidebar-collapsed');
    }
  }
}

function cerrarSidebarMobile() {
  if (window.innerWidth <= 768) {
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (sidebar) sidebar.classList.remove('mobile-open');
    if (backdrop) backdrop.classList.remove('active');
  }
}'''

if old_toggle_start != -1:
    js = js[:old_toggle_start] + new_toggle_js + js[old_toggle_end:]

# Asegurar que showView cierre el menú lateral si estamos en celular
if 'cerrarSidebarMobile();' not in js:
    js = js.replace('function showView(viewId) {', 'function showView(viewId) {\n  cerrarSidebarMobile();')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js', 'w', encoding='utf-8') as f:
    f.write(js)
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("unes_sistema_final.js y app.js actualizados con toggle responsivo!")
