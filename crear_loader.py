
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load the processed data
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_importados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build the localStorage injection script
# The app stores data in localStorage key 'unesDB'
db = {
    'estudiantes': data['estudiantes'],
    'nextId': data['nextId'],
    'nucleos': [],   # app can derive from estudiantes
    'version': 2
}

db_json = json.dumps(db, ensure_ascii=False)

# Create a small HTML loader page that injects data then redirects
html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Cargando datos EPA...</title>
  <style>
    body {{ font-family: Inter, sans-serif; display:flex; align-items:center; justify-content:center;
           min-height:100vh; margin:0; background:#f8fafc; flex-direction:column; gap:16px; }}
    .card {{ background:#fff; border-radius:16px; padding:40px; box-shadow:0 4px 24px rgba(0,0,0,.1);
             text-align:center; max-width:420px; }}
    h2 {{ color:#800020; margin:0 0 8px; }}
    p {{ color:#64748b; margin:0 0 20px; font-size:14px; }}
    .stat {{ display:flex; gap:24px; justify-content:center; margin:16px 0; }}
    .s {{ text-align:center; }}
    .s b {{ display:block; font-size:28px; font-weight:800; color:#1e293b; }}
    .s span {{ font-size:12px; color:#94a3b8; text-transform:uppercase; letter-spacing:.05em; }}
    .bar {{ width:100%; height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden; margin:12px 0; }}
    .bar-fill {{ height:100%; border-radius:4px; transition:width 1s ease; }}
    button {{ background:#800020; color:#fff; border:none; border-radius:10px; padding:12px 28px;
              font-size:15px; font-weight:600; cursor:pointer; margin-top:8px; }}
    button:hover {{ background:#a00028; }}
    .ok {{ color:#10b981; font-weight:700; }}
  </style>
</head>
<body>
<div class="card">
  <h2>&#128202; EPA — Datos Cargados</h2>
  <p>Los siguientes datos han sido importados exitosamente al sistema:</p>

  <div class="stat">
    <div class="s"><b>{len(data['estudiantes'])}</b><span>Estudiantes</span></div>
    <div class="s"><b style="color:#10b981">{sum(1 for e in data['estudiantes'] if e['estatus']=='Aprobado')}</b><span>Aprobados</span></div>
    <div class="s"><b style="color:#ef4444">{sum(1 for e in data['estudiantes'] if e['estatus']=='Reprobado')}</b><span>Reprobados</span></div>
  </div>

  <div class="bar">
    <div class="bar-fill" id="barFill" style="width:0%;background:linear-gradient(90deg,#10b981,#059669)"></div>
  </div>
  <p class="ok" id="pct"></p>

  <p style="font-size:12px;color:#94a3b8">Criterio de aprobación: <strong>&#8805; 60 puntos</strong></p>

  <button onclick="cargar()">&#127968; Ir al Dashboard</button>
  <p id="status" style="font-size:12px;color:#10b981;margin-top:12px;"></p>
</div>

<script>
const DB_JSON = {json.dumps(db_json)};
const ap = {sum(1 for e in data['estudiantes'] if e['estatus']=='Aprobado')};
const total = {len(data['estudiantes'])};
const pct = Math.round(ap/total*100);

document.getElementById('pct').textContent = pct + '% de aprobación nacional';
setTimeout(() => {{
  document.getElementById('barFill').style.width = pct + '%';
}}, 200);

function cargar() {{
  try {{
    localStorage.setItem('unesDB', DB_JSON);
    document.getElementById('status').textContent = 'Datos guardados. Redirigiendo...';
    setTimeout(() => {{
      window.location.href = 'index.html';
    }}, 800);
  }} catch(e) {{
    document.getElementById('status').textContent = 'Error: ' + e.message;
    document.getElementById('status').style.color = '#ef4444';
  }}
}}
</script>
</body>
</html>"""

out_path = r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\cargar_datos.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Loader HTML created: {out_path}')
print(f'File size: {len(html)//1024} KB')
