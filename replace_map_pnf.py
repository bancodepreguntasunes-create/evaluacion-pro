
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','rb') as f: d=f.read()

db_start  = d.find(b'id="view-dashboard"')
map_start = d.find(b'<!-- Mapa Interactivo', db_start)
# map ends at the </section> that closes view-dashboard
section_close = d.find(b'    </section>', map_start)

before = d[:map_start]
after  = d[section_close:]   # keeps </section> and everything after

pnf_block = """<!-- PNF resumen + aprobados/reprobados -->
      <div class="pnf-section" id="pnfSection">

        <!-- Tabla PNF -->
        <div class="pnf-table-card">
          <div class="chart-header" style="padding:14px 18px 10px;border-bottom:1px solid var(--border);">
            <h3>Rendimiento por PNF</h3>
            <div id="pnfFilterWrap" style="display:flex;gap:8px;align-items:center;">
              <input type="text" id="pnfSearch" placeholder="Buscar PNF\u2026"
                onkeyup="filtrarPNF()"
                style="padding:5px 10px;border:1px solid var(--border);border-radius:8px;font-size:12px;outline:none;width:160px;">
            </div>
          </div>
          <div class="pnf-table-wrap">
            <table class="pnf-table" id="pnfTable">
              <thead>
                <tr>
                  <th onclick="sortPNF(0)">PNF \u25bf</th>
                  <th onclick="sortPNF(1)">Total</th>
                  <th onclick="sortPNF(2)">Aprobados</th>
                  <th onclick="sortPNF(3)">Reprobados</th>
                  <th onclick="sortPNF(4)">% Aprob.</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody id="pnfTableBody">
                <tr><td colspan="6" style="text-align:center;padding:20px;color:var(--text-muted)">Cargando datos\u2026</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Mini stats laterales -->
        <div class="pnf-side">
          <div class="pnf-side-card" id="pnfTopCard">
            <div class="pnf-side-title">&#127941; Mejor PNF</div>
            <div class="pnf-side-value" id="pnfTopName">\u2014</div>
            <div class="pnf-side-pct" id="pnfTopPct"></div>
          </div>
          <div class="pnf-side-card" id="pnfBotCard" style="border-color:#fee2e2;background:#fff5f5;">
            <div class="pnf-side-title" style="color:#dc2626;">&#9888;&#65039; Menor Rendimiento</div>
            <div class="pnf-side-value" id="pnfBotName">\u2014</div>
            <div class="pnf-side-pct" id="pnfBotPct" style="color:#dc2626;"></div>
          </div>
          <div class="pnf-side-card">
            <div class="pnf-side-title">&#128202; Promedio Nacional</div>
            <div class="pnf-side-value" id="pnfAvgPct" style="font-size:28px">\u2014</div>
            <div style="font-size:11px;color:var(--text-muted);margin-top:2px">de aprobaci\u00f3n</div>
          </div>
          <div class="pnf-side-card">
            <div class="pnf-side-title">&#128218; Total PNFs</div>
            <div class="pnf-side-value" id="pnfCount" style="font-size:28px">\u2014</div>
            <div style="font-size:11px;color:var(--text-muted);margin-top:2px">programas activos</div>
          </div>
        </div>

      </div>

    """

combined = before + pnf_block.encode('utf-8') + after

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','wb') as f: f.write(combined)
print('Map removed, PNF section inserted. File saved.')
print(f'Original size: {len(d)}, New size: {len(combined)}')
