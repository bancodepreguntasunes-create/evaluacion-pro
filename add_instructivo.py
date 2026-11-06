
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    data = f.read()

# ── 1. Add nav item for Instructivo ──────────────────────────────────────────
old_nav_end = b'    </nav>\r\n\r\n    <div class="sidebar-footer">'
nav_item = (
    b'      <a class="nav-item" data-view="instructivo" id="nav-instructivo" href="#" onclick="showView(\'instructivo\'); return false;">\r\n'
    b'        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    b'<path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>'
    b'<path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>\r\n'
    b'        <span>Instructivo</span>\r\n'
    b'      </a>\r\n'
)
new_nav_end = nav_item + old_nav_end

if old_nav_end in data:
    data = data.replace(old_nav_end, new_nav_end, 1)
    print('Nav item added OK')
else:
    print('ERROR: nav end not found')

# ── 2. Build instructivo section in utf-8 ─────────────────────────────────────
section_html = """
    <!-- ===== INSTRUCTIVO ===== -->
    <section class="view" id="view-instructivo">
      <div class="view-header flex-row">
        <div>
          <h1>Instructivo del Sistema EPA</h1>
          <p class="view-subtitle">Gu\u00eda de uso del Sistema de Evaluaci\u00f3n de Progreso Acad\u00e9mico</p>
        </div>
        <button class="btn-secondary" onclick="window.print()" style="gap:6px;display:flex;align-items:center;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><polyline points="6,9 6,2 18,2 18,9"/><path d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          Imprimir
        </button>
      </div>

      <div class="instructivo-grid">

        <nav class="inst-toc">
          <div class="inst-toc-title">Contenido</div>
          <a class="inst-toc-link active" href="#inst-intro"     onclick="instScroll('inst-intro',this)">Introducci\u00f3n</a>
          <a class="inst-toc-link"        href="#inst-acceso"    onclick="instScroll('inst-acceso',this)">Acceso al Sistema</a>
          <a class="inst-toc-link"        href="#inst-dashboard" onclick="instScroll('inst-dashboard',this)">Dashboard</a>
          <a class="inst-toc-link"        href="#inst-nucleos"   onclick="instScroll('inst-nucleos',this)">N\u00facleos</a>
          <a class="inst-toc-link"        href="#inst-estud"     onclick="instScroll('inst-estud',this)">Estudiantes</a>
          <a class="inst-toc-link"        href="#inst-reportes"  onclick="instScroll('inst-reportes',this)">Reportes</a>
          <a class="inst-toc-link"        href="#inst-excel"     onclick="instScroll('inst-excel',this)">Importar Excel</a>
          <a class="inst-toc-link"        href="#inst-mapa"      onclick="instScroll('inst-mapa',this)">Mapa de Venezuela</a>
          <a class="inst-toc-link"        href="#inst-faq"       onclick="instScroll('inst-faq',this)">Preguntas Frecuentes</a>
        </nav>

        <div class="inst-body" id="instBody">

          <div class="inst-section" id="inst-intro">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>1. Introducci\u00f3n</h2>
              <p>El <strong>Sistema EPA (Evaluaci\u00f3n de Progreso Acad\u00e9mico)</strong> es una herramienta desarrollada para la
              <strong>Universidad Nacional Experimental de la Seguridad (UNES)</strong> que permite visualizar, analizar y gestionar
              los resultados acad\u00e9micos de los estudiantes distribuidos en los distintos n\u00facleos del pa\u00eds.</p>
              <div class="inst-tip">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                El sistema funciona completamente en el navegador. No requiere instalaci\u00f3n ni conexi\u00f3n a internet despu\u00e9s de abrir el archivo.
              </div>
            </div>
          </div>

          <div class="inst-section" id="inst-acceso">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#0ea5e9,#2563eb)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/><polyline points="10,17 15,12 10,7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>2. Acceso al Sistema</h2>
              <p>Para abrir el sistema simplemente haga doble clic en el archivo <code>index.html</code>. Se abrir\u00e1 en su navegador predeterminado (se recomienda Google Chrome o Microsoft Edge).</p>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>Localice la carpeta del sistema en su equipo.</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Haga doble clic en <code>index.html</code>.</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>El sistema carga autom\u00e1ticamente con los datos guardados o de demostraci\u00f3n.</span></div>
              </div>
              <div class="inst-warning">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                Los datos importados se guardan localmente en localStorage del navegador. No se sincronizar\u00e1n a otros equipos.
              </div>
            </div>
          </div>

          <div class="inst-section" id="inst-dashboard">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#10b981,#059669)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>3. Panel Principal (Dashboard)</h2>
              <p>Primera pantalla al abrir el sistema. Presenta un resumen general del estado acad\u00e9mico nacional.</p>
              <table class="inst-table">
                <thead><tr><th>Elemento</th><th>Descripci\u00f3n</th></tr></thead>
                <tbody>
                  <tr><td>Tarjetas de estad\u00edsticas</td><td>Totales nacionales: estudiantes, aprobados, reprobados y n\u00facleos activos.</td></tr>
                  <tr><td>Gr\u00e1fica PNF</td><td>Comparativa de aprobados vs reprobados por Programa Nacional de Formaci\u00f3n.</td></tr>
                  <tr><td>Gr\u00e1fica Trayecto</td><td>Distribuci\u00f3n de resultados por trayecto (I, II, III, IV).</td></tr>
                  <tr><td>Mapa de Venezuela</td><td>Vista geogr\u00e1fica interactiva por estado (ver secci\u00f3n 8).</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="inst-section" id="inst-nucleos">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>4. N\u00facleos</h2>
              <p>Listado de todos los n\u00facleos universitarios con indicadores de rendimiento. Puede buscar, filtrar y ordenar la tabla.</p>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>Use la barra de b\u00fasqueda para encontrar un n\u00facleo por nombre o estado.</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Haga clic en los encabezados de columna para ordenar los datos.</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>Use el bot\u00f3n <strong>Exportar CSV</strong> en la barra superior para descargar.</span></div>
              </div>
            </div>
          </div>

          <div class="inst-section" id="inst-estud">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#ec4899,#db2777)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>5. Estudiantes</h2>
              <p>Registro individual con filtros por n\u00facleo, PNF, trayecto y condici\u00f3n acad\u00e9mica.</p>
              <table class="inst-table">
                <thead><tr><th>Columna</th><th>Significado</th></tr></thead>
                <tbody>
                  <tr><td>C\u00e9dula</td><td>N\u00famero de identificaci\u00f3n del estudiante.</td></tr>
                  <tr><td>Nombre</td><td>Nombre completo.</td></tr>
                  <tr><td>N\u00facleo</td><td>N\u00facleo donde cursa estudios.</td></tr>
                  <tr><td>PNF</td><td>Programa Nacional de Formaci\u00f3n inscrito.</td></tr>
                  <tr><td>Trayecto</td><td>Nivel acad\u00e9mico actual (I\u2013IV).</td></tr>
                  <tr><td>Estado</td><td>Aprobado o Reprobado.</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="inst-section" id="inst-reportes">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#14b8a6,#0d9488)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>6. Reportes</h2>
              <p>Genera informes filtrando por estado, n\u00facleo, PNF y trayecto. Permite exportar en CSV.</p>
              <div class="inst-tip">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Puede combinar m\u00faltiples filtros simult\u00e1neamente para reportes espec\u00edficos.
              </div>
            </div>
          </div>

          <div class="inst-section" id="inst-excel">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#22c55e,#16a34a)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17,8 12,3 7,8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>7. Importar desde Excel</h2>
              <p>El sistema acepta archivos <code>.xlsx</code> o <code>.xls</code> con las siguientes columnas en la primera hoja:</p>
              <table class="inst-table">
                <thead><tr><th>Columna</th><th>Ejemplo</th><th>Nota</th></tr></thead>
                <tbody>
                  <tr><td>cedula</td><td>12345678</td><td>Sin puntos ni guiones</td></tr>
                  <tr><td>nombre</td><td>Juan P\u00e9rez</td><td>Nombre completo</td></tr>
                  <tr><td>nucleo</td><td>CARACAS</td><td>Nombre del n\u00facleo</td></tr>
                  <tr><td>pnf</td><td>Seguridad</td><td>Programa Nacional de Formaci\u00f3n</td></tr>
                  <tr><td>trayecto</td><td>II</td><td>Romano o num\u00e9rico (1\u20134)</td></tr>
                  <tr><td>estado</td><td>Aprobado</td><td>"Aprobado" o "Reprobado"</td></tr>
                </tbody>
              </table>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>Haga clic en <strong>Importar Excel</strong> en el men\u00fa lateral.</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Arrastre su archivo al \u00e1rea de carga o haga clic en <strong>Seleccionar archivo</strong>.</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>Elija si desea <em>reemplazar</em> o <em>agregar</em> los datos existentes.</span></div>
                <div class="inst-step"><span class="inst-step-num">4</span><span>Haga clic en <strong>Importar datos al sistema</strong> y espere la confirmaci\u00f3n.</span></div>
              </div>
            </div>
          </div>

          <div class="inst-section" id="inst-mapa">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#f43f5e,#e11d48)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1,6 1,22 8,18 16,22 23,18 23,2 16,6 8,2"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>8. Mapa Interactivo de Venezuela</h2>
              <p>En el Dashboard, el mapa muestra el rendimiento acad\u00e9mico por estado con el siguiente c\u00f3digo de colores:</p>
              <div class="inst-legend-row">
                <div class="inst-legend-item"><span class="inst-dot" style="background:#10b981"></span><strong>Verde</strong> \u2014 Alto rendimiento (\u2265 60% aprobados)</div>
                <div class="inst-legend-item"><span class="inst-dot" style="background:#f59e0b"></span><strong>Amarillo</strong> \u2014 Rendimiento medio (40\u201359%)</div>
                <div class="inst-legend-item"><span class="inst-dot" style="background:#ef4444"></span><strong>Rojo</strong> \u2014 Rendimiento bajo (&lt; 40%)</div>
                <div class="inst-legend-item"><span class="inst-dot" style="background:#e2e8f0"></span><strong>Gris</strong> \u2014 Sin datos registrados</div>
              </div>
              <p>Haga clic en cualquier estado del mapa para ver la lista de n\u00facleos, total de estudiantes, aprobados y reprobados de ese estado en el panel derecho.</p>
            </div>
          </div>

          <div class="inst-section" id="inst-faq">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>9. Preguntas Frecuentes</h2>
              <div class="inst-faq-list">
                <details class="inst-faq-item">
                  <summary>\u00bfSe pierden los datos al cerrar el navegador?</summary>
                  <p>No. Los datos se almacenan en localStorage y se conservan hasta que se borren manualmente o se importe un nuevo archivo.</p>
                </details>
                <details class="inst-faq-item">
                  <summary>\u00bfEl sistema funciona sin internet?</summary>
                  <p>S\u00ed, una vez abierto el archivo funciona sin conexi\u00f3n. Solo requiere internet la primera vez si se usan las librer\u00edas CDN.</p>
                </details>
                <details class="inst-faq-item">
                  <summary>\u00bfCu\u00e1ntos estudiantes soporta?</summary>
                  <p>El sistema puede manejar hasta aproximadamente 50.000 registros sin problemas de rendimiento en equipos modernos.</p>
                </details>
                <details class="inst-faq-item">
                  <summary>\u00bfC\u00f3mo exporto los datos?</summary>
                  <p>Use el bot\u00f3n de descarga en la barra superior para exportar todos los datos en formato CSV, compatible con Excel.</p>
                </details>
                <details class="inst-faq-item">
                  <summary>\u00bfQu\u00e9 navegadores son compatibles?</summary>
                  <p>Google Chrome 90+, Microsoft Edge 90+ y Mozilla Firefox 88+. Se recomienda Chrome para mejor rendimiento.</p>
                </details>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
    <!-- ===== FIN INSTRUCTIVO ===== -->
"""

# Insert before </main>
main_end = b'</main>'
if main_end in data:
    data = data.replace(main_end, section_html.encode('utf-8') + main_end, 1)
    print('Instructivo section inserted!')
else:
    print('ERROR: </main> not found')

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'wb') as f:
    f.write(data)
print('File saved.')
