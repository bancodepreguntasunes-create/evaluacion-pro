// ──────────────────────────────────────────
//  CALENDARIO DE EVALUACIONES (04 - 18 NOV)
// ──────────────────────────────────────────

const ALL_PNFS_IDS = PNF_LIST.map(p => p.id);

// 39 Núcleos distribuidos en 6 grupos de evaluación
const G1 = ["CARACAS", "HELICOIDE", "JUNQUITO", "SAN PEDRO - COMUNAL", "EL LLANITO", "CAFETAL"];
const G2 = ["LA GUAIRA", "CEFE CARMEN DE URIA", "EJE METROPOLITANO", "EJE ALTOS MIRANDINOS", "EJE VALLES DEL TUY", "EJE BARLOVENTO", "EJE GUARENAS - GUATIRE"];
const G3 = ["ARAGUA", "CARABOBO", "YARACUY", "FALCÓN", "LARA", "COJEDES", "COJEDES TINAQUILLO"];
const G4 = ["ZULIA", "EJE LA GUAJIRA", "EJE SUR DEL LAGO", "APURE", "BARINAS", "GUÁRICO", "PORTUGUESA"];
const G5 = ["MÉRIDA", "TÁCHIRA", "TRUJILLO", "ANZOÁTEGUI", "MONAGAS", "NUEVA ESPARTA"];
const G6 = ["SUCRE", "CARUPANO", "AMAZONAS", "BOLÍVAR - PTO. ORDAZ", "BOLÍVAR - ANGOSTURA", "DELTA AMACURO"];

const SCHEDULE_DAYS = [
  // ── 1ª CONVOCATORIA (INICIAL, I, II) ──
  { fecha:"2026-11-04", dia:"Miércoles 04 de Noviembre", label:"1ª Convocatoria · Día 01",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Región Capital & Miranda (Grupo 1)",
    nucleos:G1, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-05", dia:"Jueves 05 de Noviembre", label:"1ª Convocatoria · Día 02",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"La Guaira & Ejes Subregionales (Grupo 2)",
    nucleos:G2, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-06", dia:"Viernes 06 de Noviembre", label:"1ª Convocatoria · Día 03",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Región Central & Cojedes (Grupo 3)",
    nucleos:G3, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-07", dia:"Sábado 07 de Noviembre", label:"1ª Convocatoria · Día 04",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Zulia & Región Los Llanos (Grupo 4)",
    nucleos:G4, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-08", dia:"Domingo 08 de Noviembre", label:"1ª Convocatoria · Día 05",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Región Los Andes & Oriente (Grupo 5)",
    nucleos:G5, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-09", dia:"Lunes 09 de Noviembre", label:"1ª Convocatoria · Día 06",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Región Sur, Guayana & Delta (Grupo 6)",
    nucleos:G6, pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-10", dia:"Martes 10 de Noviembre", label:"1ª Convocatoria · Día 07",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Jornada de Cierre 1ª Convocatoria",
    nucleos:G1.concat(G2.slice(0,3)), pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-11", dia:"Miércoles 11 de Noviembre", label:"1ª Convocatoria · Día 08",
    convocatoria:"1ª Convocatoria (Trayecto Inicial, I y II)", region:"Jornada Final 1ª Convocatoria",
    nucleos:G3.concat(G4.slice(0,3)), pnfs:ALL_PNFS_IDS, trayectos:["Inicial","I","II"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto Inicial y Trayecto I", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto II", pnfs:"Todos los PNF de la UNES" }
    ]},

  // ── 2ª CONVOCATORIA (III, IV) ──
  { fecha:"2026-11-12", dia:"Jueves 12 de Noviembre", label:"2ª Convocatoria · Día 09",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"Región Capital & Miranda (Grupo 1)",
    nucleos:G1, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-13", dia:"Viernes 13 de Noviembre", label:"2ª Convocatoria · Día 10",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"La Guaira & Ejes Subregionales (Grupo 2)",
    nucleos:G2, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-14", dia:"Sábado 14 de Noviembre", label:"2ª Convocatoria · Día 11",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"Región Central & Cojedes (Grupo 3)",
    nucleos:G3, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-15", dia:"Domingo 15 de Noviembre", label:"2ª Convocatoria · Día 12",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"Zulia & Región Los Llanos (Grupo 4)",
    nucleos:G4, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-16", dia:"Lunes 16 de Noviembre", label:"2ª Convocatoria · Día 13",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"Región Los Andes & Oriente (Grupo 5)",
    nucleos:G5, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},
  { fecha:"2026-11-17", dia:"Martes 17 de Noviembre", label:"2ª Convocatoria · Día 14",
    convocatoria:"2ª Convocatoria (Trayecto III y IV)", region:"Región Sur, Guayana & Delta (Grupo 6)",
    nucleos:G6, pnfs:ALL_PNFS_IDS, trayectos:["III","IV"],
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Trayecto III", pnfs:"Todos los PNF de la UNES" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Trayecto IV", pnfs:"Todos los PNF de la UNES" }
    ]},

  // ── JORNADA FINAL ──
  { fecha:"2026-11-18", dia:"Miércoles 18 de Noviembre", label:"JORNADA NACIONAL FINAL",
    isRezagados:true,
    convocatoria:"Jornada Nacional de Rezagados y Reprobados",
    region:"TODOS LOS 40 NÚCLEOS DE LA UNES",
    nucleos:NUCLEOS, pnfs:ALL_PNFS_IDS, trayectos:TRAYECTOS,
    turnos:[
      { turno:"Turno Mañana (08:00 AM - 12:00 PM)", trayecto:"Todos los Trayectos (Inicial a IV)", pnfs:"🚨 Evaluación Extraordinaria Rezagados (Todos los 40 Núcleos - Todos los PNF)" },
      { turno:"Turno Tarde (01:00 PM - 05:00 PM)", trayecto:"Todos los Trayectos (Inicial a IV)", pnfs:"⚠️ Recuperación Estudiantes Reprobados (Todos los 40 Núcleos - Todos los PNF)" }
    ]}
];

let selectedCalDate = null;

// ──────────────────────────────────────────
//  RENDER CALENDARIO INTERACTIVO
// ──────────────────────────────────────────
function renderInteractiveCalendar() {
  const container = document.getElementById('interactiveCalendar');
  if (!container) return;

  const daysOfWeek = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
  const monthNames = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

  const viewYear = 2026, viewMonth = 10; // Noviembre
  const firstDay = new Date(viewYear, viewMonth, 1).getDay();
  const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();

  let html = `
    <div class="cal-month-nav">
      <span class="cal-month-title">${monthNames[viewMonth]} ${viewYear}</span>
      ${selectedCalDate ? `<button class="cal-clear-btn" onclick="limpiarSeleccionCalendario()">✕ Quitar filtro</button>` : ``}
    </div>
    <div class="month-grid">`;

  daysOfWeek.forEach(d => html += `<div class="month-header-day">${d}</div>`);
  for (let i = 0; i < firstDay; i++) html += `<div class="month-day empty"></div>`;

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${viewYear}-${String(viewMonth+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
    const eventDay = SCHEDULE_DAYS.find(d => d.fecha === dateStr);
    let classes = 'month-day';
    let indicator = '';
    if (eventDay) {
      classes += ' has-event';
      if (eventDay.isRezagados) classes += ' is-rezagados';
      indicator = `<div class="month-day-indicator"></div>`;
    }
    if (selectedCalDate === dateStr) classes += ' selected';
    const clickable = eventDay ? `onclick="seleccionarFechaCalendario('${dateStr}')"` : '';
    const titleAttr = eventDay ? `title="${escHTML(eventDay.label)} · ${escHTML(eventDay.region)}"` : '';
    html += `<div class="${classes}" ${clickable} ${titleAttr}>${day}${indicator}</div>`;
  }
  html += `</div>`;
  container.innerHTML = html;
}

function seleccionarFechaCalendario(fecha) {
  selectedCalDate = (selectedCalDate === fecha) ? null : fecha;
  renderInteractiveCalendar();
  renderCalendario();
}
function limpiarSeleccionCalendario() {
  selectedCalDate = null;
  renderInteractiveCalendar();
  renderCalendario();
}

// ──────────────────────────────────────────
//  RENDER TARJETAS DE JORNADAS
// ──────────────────────────────────────────
function renderCalendario() {
  renderInteractiveCalendar();
  const container = document.getElementById('calGrid');
  if (!container) return;

  const fNucleo   = document.getElementById('calFiltroNucleo')?.value   || '';
  const fPNF      = document.getElementById('calFiltroPNF')?.value      || '';
  const fTrayecto = document.getElementById('calFiltroTrayecto')?.value || '';

  let filteredDays = SCHEDULE_DAYS.filter(d => {
    if (selectedCalDate && d.fecha !== selectedCalDate) return false;
    if (fNucleo   && !d.nucleos.includes(fNucleo))     return false;
    if (fPNF      && !d.pnfs.includes(fPNF))           return false;
    if (fTrayecto && !d.trayectos.includes(fTrayecto)) return false;
    return true;
  });

  if (!filteredDays.length) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1">
        <h3>Sin jornadas coincidentes</h3>
        <p>No se encontraron días programados para los filtros seleccionados.<br>Intenta seleccionar otro Núcleo o PNF.</p>
        <button class="btn-secondary" style="margin-top:16px" onclick="limpiarFiltrosCalendario()">Ver todo el calendario</button>
      </div>`;
    return;
  }

  container.innerHTML = filteredDays.map(d => {
    const isRez = d.isRezagados;
    let matchingEst = DB.estudiantes.filter(e => d.nucleos.includes(e.nucleo) && d.trayectos.includes(e.trayecto));
    if (fPNF)      matchingEst = matchingEst.filter(e => e.pnf === fPNF);
    if (fTrayecto) matchingEst = matchingEst.filter(e => e.trayecto === fTrayecto);
    const reprobadosCount = isRez ? matchingEst.filter(e => e.estatus === 'Reprobado').length : 0;

    return `
      <div class="cal-card ${isRez ? 'is-rezagados' : ''}">
        <div class="cal-card-header">
          <div class="cal-date-block">
            <span class="cal-month">NOV</span>
            <span class="cal-day-num">${d.fecha.split('-')[2]}</span>
          </div>
          <div class="cal-header-info">
            <span class="cal-day-label">${escHTML(d.label)}</span>
            <h4 class="cal-date-title">${escHTML(d.dia)}</h4>
            <span class="cal-region-tag">${escHTML(d.region)}</span>
          </div>
        </div>
        <div class="cal-card-body">
          <div style="margin-bottom:12px">
            <span class="badge ${isRez ? 'badge-reprobado' : 'badge-trayecto'}" style="font-size:13px;font-weight:700">
              ${escHTML(d.convocatoria)}
            </span>
          </div>
          ${isRez ? `
            <div class="cal-alert rezagados-alert">
              <span class="alert-icon">🚨</span>
              <div class="alert-text">
                <strong>JORNADA NACIONAL DE REZAGADOS Y REPROBADOS</strong>
                <p>Atención especial para la evaluación extraordinaria de estudiantes rezagados y la recuperación de reprobados de <strong>todos los núcleos de la UNES (Todos los PNF)</strong>.</p>
              </div>
            </div>` : `
            <div class="cal-section">
              <div class="cal-sec-title">Núcleos Convocados</div>
              <div class="cal-nucleos-list">
                ${d.nucleos.map(n => `<span class="cal-nucleo-chip">${escHTML(n)}</span>`).join('')}
              </div>
            </div>`}
          <div class="cal-section" style="margin-top:12px;">
            <div class="cal-sec-title">Turnos y Programación</div>
            <div class="cal-turnos">
              ${d.turnos.map(t => `
                <div class="cal-turno-item">
                  <div class="cal-turno-name">${escHTML(t.turno)}</div>
                  <div class="cal-turno-desc">
                    <div class="cal-turno-row"><span class="cal-turno-label">Trayectos:</span>
                      <span class="badge badge-trayecto" style="font-size:11px;padding:2px 6px">${escHTML(t.trayecto)}</span>
                    </div>
                    <div class="cal-turno-row"><span class="cal-turno-label">Aplica a:</span>
                      <strong style="color:#800020">${escHTML(t.pnfs)}</strong>
                    </div>
                  </div>
                </div>`).join('')}
            </div>
          </div>
        </div>
        <div class="cal-card-footer">
          <span>Matrícula: <strong>${matchingEst.length}</strong></span>
          ${isRez && reprobadosCount > 0 ? `<span style="color:#dc2626;font-weight:700">${reprobadosCount} reprobados</span>` : ''}
        </div>
      </div>`;
  }).join('');
}

function limpiarFiltrosCalendario() {
  ['calFiltroNucleo','calFiltroPNF','calFiltroTrayecto'].forEach(id => {
    const el = document.getElementById(id); if (el) el.value = '';
  });
  selectedCalDate = null;
  renderCalendario();
}
