import re

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the dashboard section
db_start = html.find('<section class="view active" id="view-dashboard">')
db_end   = html.find('\n    <!-- ===== NÚCLEOS', db_start)

new_dashboard = '''<section class="view active" id="view-dashboard">

      <!-- ROW 1: Stats + Charts -->
      <div class="db-top-row">
        <!-- Stats column -->
        <div class="stats-row" id="statsGrid"></div>
        <!-- Charts -->
        <div class="dash-charts" id="dashCharts">
          <div class="chart-card dash-chart-main">
            <div class="chart-header"><h3>Aprobados vs Reprobados por PNF</h3></div>
            <div class="chart-wrap"><canvas id="chartPNF"></canvas></div>
          </div>
          <div class="chart-card dash-chart-right">
            <div class="chart-header"><h3>Por Trayecto</h3></div>
            <div class="chart-wrap"><canvas id="chartTrayecto"></canvas></div>
          </div>
          <div class="chart-card dash-chart-bottom">
            <div class="chart-header"><h3>Top 10 Núcleos</h3></div>
            <div class="chart-wrap"><canvas id="chartNucleos"></canvas></div>
          </div>
        </div>
      </div>

      <!-- ROW 2: Mapa Interactivo -->
      <div class="map-section" id="mapSection">
        <!-- Panel izquierdo: Mapa -->
        <div class="map-left">
          <div class="map-header">
            <div>
              <h3>Mapa Nacional de Núcleos</h3>
              <p>Clic en un estado para ver sus núcleos</p>
            </div>
            <button class="btn-secondary" onclick="seleccionarEstado(null)" style="font-size:11px;padding:4px 10px;">Ver Todo</button>
          </div>
          <div class="map-container">
'''

# Grab the SVG from old content
svg_start = html.find('<svg id="venezuelaMap"', db_start)
svg_end   = html.find('</svg>', svg_start) + 6
svg_block = html[svg_start:svg_end]

new_dashboard += '            ' + svg_block + '\n'
new_dashboard += '''          </div>
          <div class="map-legend">
            <div class="map-legend-item"><span class="legend-dot" style="background:#10b981"></span>Alto (&ge;60%)</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#f59e0b"></span>Medio</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#ef4444"></span>Bajo</div>
            <div class="map-legend-item"><span class="legend-dot" style="background:#e2e8f0"></span>Sin datos</div>
          </div>
        </div>
        <!-- Panel derecho: Desglose -->
        <div class="map-right" id="mapPanel">
          <div class="map-panel-placeholder" id="mapPanelPlaceholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <h4>Selecciona un Estado</h4>
            <p>Haz clic en cualquier estado del mapa para ver sus núcleos y resultados académicos.</p>
          </div>
          <div id="mapPanelContent" style="display:none;"></div>
        </div>
      </div>

    </section>
'''

html = html[:db_start] + new_dashboard + html[db_end:]

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Dashboard HTML restructured successfully')
