
# -*- coding: utf-8 -*-
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'rb') as f:
    data = f.read()

# Find inst-body start and FIN INSTRUCTIVO
body_start_marker = b'<div class="inst-body" id="instBody">'
fin_marker        = b'<!-- ===== FIN INSTRUCTIVO ===== -->'

body_start = data.find(body_start_marker)
fin_idx    = data.find(fin_marker)

if body_start == -1 or fin_idx == -1:
    print(f'ERROR: body_start={body_start}, fin_idx={fin_idx}')
    exit()

# The section to replace: from <div class="inst-body"...> up to (but not including) <!-- FIN -->
# We keep everything BEFORE body_start, insert the new body, then keep from fin_marker onwards
before = data[:body_start]
after  = data[fin_idx:]  # starts with <!-- ===== FIN INSTRUCTIVO ===== -->

new_body = """<div class="inst-body" id="instBody">

          <!-- I. PROP\u00d3SITO -->
          <div class="inst-section" id="inst-intro">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>I. Prop\u00f3sito</h2>
              <p>La UNES ha implementado el presente instructivo para establecer los lineamientos y responsabilidades claras y precisas que rigen el proceso de <strong>Evaluaci\u00f3n de Progreso Acad\u00e9mico (EPA)</strong> de las materias de la malla curricular de cada uno de los PNF, garantizando que los procedimientos sean id\u00e9nticos en todos los n\u00facleos del pa\u00eds.</p>
              <h3 class="inst-h3">Objetivos del Instructivo</h3>
              <ul class="inst-list">
                <li><strong>Clarificar roles y responsabilidades</strong> de cada actor involucrado en el proceso.</li>
                <li><strong>Abordar la virtualidad:</strong> protocolos ante contingencias tecnol\u00f3gicas, conectividad y fallas de equipo.</li>
                <li><strong>Fortalecer la integridad acad\u00e9mica</strong> con mecanismos robustos que garanticen la probidad.</li>
                <li><strong>Construir una base s\u00f3lida</strong> para futuras evaluaciones virtuales, ajustando y mejorando continuamente.</li>
              </ul>
            </div>
          </div>

          <!-- II. DEFINICIONES -->
          <div class="inst-section" id="inst-definiciones">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#0ea5e9,#2563eb)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>II. Definiciones Clave</h2>
              <table class="inst-table">
                <thead><tr><th>T\u00e9rmino</th><th>Definici\u00f3n</th></tr></thead>
                <tbody>
                  <tr><td><strong>EPA</strong></td><td>Evaluaci\u00f3n de Progreso Acad\u00e9mico. Proceso evaluativo para verificar el nivel de conocimiento, habilidades y competencias de los estudiantes.</td></tr>
                  <tr><td><strong>Banco de Preguntas</strong></td><td>Repositorio sistem\u00e1tico de \u00edtems validados pedag\u00f3gicamente, categorizados por tem\u00e1tica, dificultad y competencia.</td></tr>
                  <tr><td><strong>N\u00facleo</strong></td><td>Sedes regionales o extensiones acad\u00e9micas y administrativas de la UNES.</td></tr>
                  <tr><td><strong>Competencia</strong></td><td>Capacidad probada para utilizar conocimientos, habilidades y aptitudes en situaciones de trabajo o estudio.</td></tr>
                  <tr><td><strong>Credenciales FUNDAUNES</strong></td><td>Usuario y contrase\u00f1a \u00fanicos asignados por la UNES a cada miembro de la comunidad universitaria v\u00eda SIGA.</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- III. MARCO JURIDICO -->
          <div class="inst-section" id="inst-marco">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>III. Marco Jur\u00eddico y Normativo</h2>
              <ul class="inst-list">
                <li>Ley de Universidades (1970) y su Reglamento (1970).</li>
                <li>Ley Org\u00e1nica de Educaci\u00f3n (2009).</li>
                <li>Reglamento de Evaluaci\u00f3n Acad\u00e9mica de la UNES \u2014 <strong>Acuerdo 0703</strong>.</li>
              </ul>
            </div>
          </div>

          <!-- IV. ALCANCE -->
          <div class="inst-section" id="inst-alcance">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#10b981,#059669)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>IV. Alcance</h2>
              <p>Aplicaci\u00f3n obligatoria para todo el personal y estudiantes de los N\u00facleos de la UNES. Incluye:</p>
              <ul class="inst-list">
                <li><strong>Decanatos:</strong> Supervisi\u00f3n directa, validaci\u00f3n y aprobaci\u00f3n final del proceso.</li>
                <li><strong>Unacies:</strong> Planificaci\u00f3n, organizaci\u00f3n log\u00edstica y gesti\u00f3n operativa.</li>
                <li><strong>Docentes / Supervisores:</strong> Elaboraci\u00f3n, validaci\u00f3n y aplicaci\u00f3n de los \u00edtems de evaluaci\u00f3n.</li>
                <li><strong>Administrador EPA:</strong> Gesti\u00f3n tecnol\u00f3gica y operativa de la plataforma.</li>
                <li><strong>Personal Administrativo:</strong> Log\u00edstica y soporte t\u00e9cnico.</li>
                <li><strong>Estudiantes UNES:</strong> Sujetos de la evaluaci\u00f3n, deben cumplir todas las disposiciones.</li>
              </ul>
            </div>
          </div>

          <!-- V-VI. DISPOSICIONES -->
          <div class="inst-section" id="inst-disposiciones">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#ec4899,#db2777)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>V &amp; VI. Disposiciones Generales y Especiales</h2>
              <div class="inst-warning">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                Cualquier acto que atente contra la probidad acad\u00e9mica (fraude, plagio, uso no autorizado de materiales) ser\u00e1 sancionado conforme a la normativa interna de la UNES y la legislaci\u00f3n vigente.
              </div>
              <ul class="inst-list" style="margin-top:12px">
                <li><strong>Confidencialidad:</strong> El banco de preguntas y los resultados individuales son de car\u00e1cter confidencial.</li>
                <li><strong>Accesibilidad e Inclusi\u00f3n:</strong> Se garantizan adaptaciones razonables para estudiantes con necesidades educativas especiales.</li>
                <li><strong>Infraestructura:</strong> Los N\u00facleos deben asegurar laboratorios con equipos funcionales, conexi\u00f3n estable y planes de contingencia el\u00e9ctrica o de conectividad.</li>
                <li><strong>Personal designado:</strong> Los Decanatos deben asignar y capacitar a los supervisores con pleno conocimiento de este instructivo.</li>
              </ul>
            </div>
          </div>

          <!-- VII. ROLES -->
          <div class="inst-section" id="inst-roles">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#14b8a6,#0d9488)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>VII. Roles y Responsabilidades</h2>

              <h3 class="inst-h3" style="color:var(--primary)">&#127970; Vicerrectorado Acad\u00e9mico</h3>
              <ul class="inst-list">
                <li>M\u00e1xima supervisi\u00f3n y autoridad del proceso EPA a nivel nacional.</li>
                <li>Aprobaci\u00f3n del banco de preguntas y configuraci\u00f3n de la plataforma.</li>
              </ul>

              <h3 class="inst-h3" style="color:var(--primary)">&#127970; N\u00facleo</h3>
              <ul class="inst-list">
                <li>Garantizar infraestructura: laboratorios, internet estable, espacios id\u00f3neos.</li>
                <li>Designar supervisores capacitados para cada sesi\u00f3n.</li>
                <li>Contacto: <a href="mailto:bancodepreguntasunes@gmail.com" style="color:var(--primary)">bancodepreguntasunes@gmail.com</a></li>
              </ul>

              <h3 class="inst-h3" style="color:var(--primary)">&#128104;&#8205;&#127979; Docente / Supervisor de la Prueba</h3>
              <ul class="inst-list">
                <li>Verificar identidad (c\u00e9dula o carnet) al ingreso al aula.</li>
                <li>Distribuir el c\u00f3digo de acceso \u00fanicamente al inicio de la sesi\u00f3n.</li>
                <li>Mantener vigilancia activa. Cero tolerancia al fraude.</li>
                <li>Tomar memoria fotogr\u00e1fica al finalizar y consolidar el listado de resultados.</li>
              </ul>

              <h3 class="inst-h3" style="color:var(--primary)">&#128187; Administrador de la Plataforma EPA</h3>
              <ul class="inst-list">
                <li>Configurar y mantener la plataforma tecnol\u00f3gica.</li>
                <li>Gestionar el banco de preguntas (carga, categorizaci\u00f3n, seguridad).</li>
                <li>Generar c\u00f3digos de acceso \u00fanicos con validez de <strong>90 minutos</strong>.</li>
                <li>Monitoreo en tiempo real y soporte t\u00e9cnico avanzado.</li>
              </ul>

              <h3 class="inst-h3" style="color:var(--primary)">&#127891; Estudiante</h3>
              <ul class="inst-list">
                <li>Prepararse revisando a fondo los contenidos y manuales de estudio.</li>
                <li>Verificar con anticipaci\u00f3n acceso a internet y dispositivo compatible.</li>
                <li>Ingresar a: <a href="https://unesexam.vercel.app" target="_blank" style="color:var(--primary);font-weight:600">https://unesexam.vercel.app</a> con credenciales FUNDAUNES.</li>
                <li>Gestionar los <strong>90 minutos</strong> de evaluaci\u00f3n eficientemente.</li>
                <li>Conducta \u00edntegra y honesta. Prohibido el uso de gu\u00edas, celulares o materiales.</li>
              </ul>
            </div>
          </div>

          <!-- VIII. PROCEDIMIENTO -->
          <div class="inst-section" id="inst-procedimiento">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#22c55e,#16a34a)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>VIII. Procedimiento de Aplicaci\u00f3n</h2>

              <h3 class="inst-h3">Fase 1 \u2014 Planificaci\u00f3n</h3>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>Establecer fechas y horarios de evaluaci\u00f3n (Decanatos y Vicerrectorado).</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Definir par\u00e1metros: <strong>90 minutos</strong>, formato selecci\u00f3n m\u00faltiple/simple/V-F, criterio de aprobaci\u00f3n <strong>\u2265 80%</strong>.</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>Acondicionar laboratorios y designar supervisores con conocimiento exhaustivo del instructivo.</span></div>
              </div>

              <h3 class="inst-h3">Fase 2 \u2014 Aplicaci\u00f3n</h3>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>El Administrador EPA genera un c\u00f3digo \u00fanico (<strong>validez: 90 minutos</strong>) y lo entrega al supervisor justo antes del inicio.</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Verificaci\u00f3n de identidad de cada estudiante (c\u00e9dula o carnet institucional).</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>Estudiantes ingresan a <strong>https://unesexam.vercel.app</strong> con sus credenciales FUNDAUNES y seleccionan el banco de preguntas.</span></div>
                <div class="inst-step"><span class="inst-step-num">4</span><span>El supervisor distribuye el c\u00f3digo al inicio. Cada estudiante lo introduce en la plataforma.</span></div>
                <div class="inst-step"><span class="inst-step-num">5</span><span>Supervisi\u00f3n activa: <strong>prohibido</strong> el uso de gu\u00edas, celulares o cualquier material externo.</span></div>
              </div>

              <h3 class="inst-h3">Fase 3 \u2014 Resultados y Certificaci\u00f3n</h3>
              <div class="inst-steps">
                <div class="inst-step"><span class="inst-step-num">1</span><span>La plataforma guarda las respuestas autom\u00e1ticamente. El estudiante hace clic en <strong>Enviar</strong> al terminar.</span></div>
                <div class="inst-step"><span class="inst-step-num">2</span><span>Calificaci\u00f3n <strong>automatizada</strong> con las claves del banco de preguntas.</span></div>
                <div class="inst-step"><span class="inst-step-num">3</span><span>Quienes obtengan <strong>\u2265 80%</strong> reciben un <strong>certificado digital PDF</strong> inmediatamente desde la plataforma.</span></div>
                <div class="inst-step"><span class="inst-step-num">4</span><span>El N\u00facleo env\u00eda informe al Vicerrectorado: asistencia, resultados por PNF y evidencias fotogr\u00e1ficas.</span></div>
              </div>
            </div>
          </div>

          <!-- X. CRONOGRAMA -->
          <div class="inst-section" id="inst-cronograma">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#f43f5e,#e11d48)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>X. Cronograma de Evaluaci\u00f3n</h2>
              <table class="inst-table">
                <thead>
                  <tr><th>D\u00eda</th><th>N\u00facleos / Sedes</th><th>Fecha L\u00edmite Rezagados</th></tr>
                </thead>
                <tbody>
                  <tr><td><strong>Lunes 08</strong></td><td>Caracas, Amazonas, Anzo\u00e1tegui, Apure, Aragua, Barinas, Bol\u00edvar, Puerto Ordaz, Carabobo</td><td>Viernes 12</td></tr>
                  <tr><td><strong>Martes 09</strong></td><td>El Junquito, Tinaquillo, Cojedes, Delta Amacuro, Falc\u00f3n, Gu\u00e1rico, La Guaira, Lara, M\u00e9rida, Altos Mirandinos</td><td>Viernes 12</td></tr>
                  <tr><td><strong>Mi\u00e9rcoles 10</strong></td><td>Guarenas-Guatire, Valles del Tuy, Eje Metropolitano, Barlovento, El Cafetal, El Llanito, Monagas, Nueva Esparta</td><td>Viernes 12</td></tr>
                  <tr><td><strong>Jueves 11</strong></td><td>San Pedro Caracas, Portuguesa, Sucre, T\u00e1chira, Trujillo, Yaracuy, Zulia, Guajira</td><td>Viernes 12</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- DISPOSICIONES FINALES -->
          <div class="inst-section" id="inst-finales">
            <div class="inst-section-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
            </div>
            <div class="inst-section-content">
              <h2>IX &amp; XI. Disposiciones Finales y Vigencia</h2>
              <ul class="inst-list">
                <li><strong>Resoluci\u00f3n de Contingencias:</strong> Situaciones no contempladas ser\u00e1n resueltas por el Vicerrectorado Acad\u00e9mico.</li>
                <li><strong>Canal Oficial:</strong> <a href="mailto:bancodepreguntasunes@gmail.com" style="color:var(--primary);font-weight:600">bancodepreguntasunes@gmail.com</a></li>
                <li><strong>Vigencia:</strong> A partir de su emisi\u00f3n. Podr\u00e1 ajustarse por instrucciones del Vicerrectorado ante contingencias.</li>
                <li><strong>Cumplimiento Obligatorio:</strong> El desconocimiento no exime de su cumplimiento.</li>
              </ul>
              <div class="inst-tip" style="margin-top:16px">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Aprobado por: <strong>Sim\u00f3n F. Le\u00f3n Correa</strong> \u2014 Vicerrector de Desarrollo Acad\u00e9mico
              </div>
            </div>
          </div>

        """

new_toc = b"""        <nav class="inst-toc">
          <div class="inst-toc-title">Contenido</div>
          <a class="inst-toc-link active" href="#inst-intro"         onclick="instScroll('inst-intro',this)">I. Prop\xc3\xb3sito</a>
          <a class="inst-toc-link"        href="#inst-definiciones"  onclick="instScroll('inst-definiciones',this)">II. Definiciones</a>
          <a class="inst-toc-link"        href="#inst-marco"         onclick="instScroll('inst-marco',this)">III. Marco Jur\xc3\xaddico</a>
          <a class="inst-toc-link"        href="#inst-alcance"       onclick="instScroll('inst-alcance',this)">IV. Alcance</a>
          <a class="inst-toc-link"        href="#inst-disposiciones" onclick="instScroll('inst-disposiciones',this)">V-VI. Disposiciones</a>
          <a class="inst-toc-link"        href="#inst-roles"         onclick="instScroll('inst-roles',this)">VII. Roles</a>
          <a class="inst-toc-link"        href="#inst-procedimiento" onclick="instScroll('inst-procedimiento',this)">VIII. Procedimiento</a>
          <a class="inst-toc-link"        href="#inst-cronograma"    onclick="instScroll('inst-cronograma',this)">X. Cronograma</a>
          <a class="inst-toc-link"        href="#inst-finales"       onclick="instScroll('inst-finales',this)">Disposiciones Finales</a>
        </nav>"""

# Replace old TOC
old_toc_start = b'        <nav class="inst-toc">'
toc_start_idx = data.find(old_toc_start)
toc_end_idx   = data.find(b'        </nav>', toc_start_idx) + len(b'        </nav>')

if toc_start_idx != -1:
    data = data[:toc_start_idx] + new_toc + data[toc_end_idx:]
    print('TOC replaced')
    # Recalculate positions after modification
    body_start = data.find(body_start_marker)
    fin_idx    = data.find(fin_marker)

# Replace body content
before = data[:body_start]
after  = data[fin_idx:]
data   = before + new_body.encode('utf-8') + b'\n      </div>\n    </section>\n    ' + after

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html', 'wb') as f:
    f.write(data)
print('Instructivo updated with real content. File saved.')
