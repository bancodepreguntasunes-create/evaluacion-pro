
css_add = """
/* ===== PNF SECTION STYLES (DASHBOARD) ===== */
.pnf-section {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 16px;
  margin-top: 16px;
  align-items: start;
}
.pnf-table-card {
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: var(--radius-lg, 14px);
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.06));
  overflow: hidden;
}
.pnf-table-wrap {
  overflow-x: auto;
  max-height: 380px;
}
.pnf-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}
.pnf-table th {
  background: #f8fafc;
  color: var(--text-secondary, #64748b);
  font-weight: 600;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border, #e2e8f0);
  cursor: pointer;
  user-select: none;
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}
.pnf-table th:hover {
  color: var(--primary, #800020);
  background: #f1f5f9;
}
.pnf-table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border, #f1f5f9);
  color: var(--text-primary, #1e293b);
}
.pnf-table tr:hover td {
  background: rgba(128, 0, 32, 0.02);
}
.pnf-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pnf-side-card {
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: var(--radius-lg, 14px);
  padding: 14px 16px;
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.06));
  transition: transform 0.2s, box-shadow 0.2s;
}
.pnf-side-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md, 0 4px 6px -1px rgba(0,0,0,0.1));
}
.pnf-side-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary, #64748b);
  margin-bottom: 6px;
}
.pnf-side-value {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary, #0f172a);
  line-height: 1.2;
}
.pnf-side-pct {
  font-size: 13px;
  font-weight: 700;
  color: #10b981;
  margin-top: 4px;
}

/* ===== REPORTES CARDS & PILLS ===== */
.rpt-nucleo-card {
  background: #ffffff;
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 14px;
  margin-bottom: 16px;
  padding: 16px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.rpt-nucleo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 10px;
  margin-bottom: 12px;
}
.rpt-nucleo-title {
  font-size: 16px;
  font-weight: 700;
  color: #800020;
}
.rpt-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}
.rpt-pill.ap {
  background: rgba(16, 185, 129, 0.12);
  color: #065f46;
}
.rpt-pill.rep {
  background: rgba(239, 68, 68, 0.12);
  color: #991b1b;
}
.rpt-token-badge {
  display: inline-block;
  background: #f1f5f9;
  color: #475569;
  border-radius: 6px;
  padding: 2px 8px;
  font-family: monospace;
  font-size: 12px;
  font-weight: 600;
}
"""

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'r', encoding='utf-8', errors='ignore') as f:
    orig_css = f.read()

if '.pnf-section' not in orig_css:
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'a', encoding='utf-8') as f:
        f.write(css_add)
    print('styles.css updated with PNF & Reportes styles!')
else:
    print('Styles already present')
