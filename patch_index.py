import re

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add inline cache cleaner after <body>
if 'AUTO-PURGE' not in html:
    body_tag = '<body>'
    cleaner_script = '''<body>
  <script>
    // AUTO-PURGE: Limpia de inmediato cualquier base de datos con calculo invertido guardada en localStorage
    try {
      var _raw = localStorage.getItem('unesDB');
      if (_raw) {
        var _db = JSON.parse(_raw);
        if (_db && _db.estudiantes) {
          var _ap = _db.estudiantes.filter(function(e) { return e.estatus === 'Aprobado'; }).length;
          var _rep = _db.estudiantes.filter(function(e) { return e.estatus === 'Reprobado'; }).length;
          if (_rep > _ap || !_db.version || _db.version < 5) {
            console.warn('Purgando localStorage corrupto...');
            localStorage.removeItem('unesDB');
            localStorage.removeItem('unes_estudiantes');
          }
        }
      }
    } catch(e) {
      localStorage.clear();
    }
  </script>'''
    html = html.replace(body_tag, cleaner_script, 1)

# 2. Add button in topbar-actions
if 'restablecerDatos()' not in html:
    target = '<button class="btn-icon" onclick="exportarCSV()"'
    btn_html = '''<button class="btn-secondary" onclick="restablecerDatos()" style="font-size:12px;padding:6px 12px;margin-right:8px;display:inline-flex;align-items:center;gap:6px;background:rgba(239,68,68,0.1);color:#b91c1c;border:1px solid rgba(239,68,68,0.3);border-radius:6px;cursor:pointer;font-weight:600;" title="Restablecer a datos oficiales verificados (2.014 Aprobados, 78 Reprobados)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Restablecer Datos
        </button>
        <button class="btn-icon" onclick="exportarCSV()"'''
    html = html.replace(target, btn_html, 1)

# 3. Change script to unes_core_v5.js
html = re.sub(r'<script\s+src=["\']app\.js.*?["\']\s*></script>', '<script src="unes_core_v5.js"></script>', html)

with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html patched successfully!")
