import re

# ---- patch styles.css ----
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'rb') as f:
    css = f.read().decode('latin-1')

# 1) Stats row – más compacta
old = """.stats-row {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  flex-shrink: 0;
}"""
new = """.stats-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  flex-shrink: 0;
}"""
css = css.replace(old, new)

# 2) stat-card más compacta
old2 = """  padding: 14px 16px;"""
if '  padding: 14px 16px;' in css:
    # Only first occurrence in stat-card context
    idx = css.find('  padding: 14px 16px;')
    css = css[:idx] + '  padding: 8px 12px;' + css[idx+len('  padding: 14px 16px;'):]

# 3) dash-charts: replace grid to include map section in same layout
old3 = """.dash-charts {
  display: grid;
  grid-template-columns: 1fr 280px;
  grid-template-rows: 1fr 1fr;
  gap: 10px;
  flex: 1;
  min-height: 0;
}"""
new3 = """.dash-charts {
  display: grid;
  grid-template-columns: 1fr 220px;
  grid-template-rows: 1fr 1fr;
  gap: 8px;
  flex: 1;
  min-height: 0;
}"""
css = css.replace(old3, new3)

# 4) map-section: now embedded inline in grid, remove margin-top
old4 = """.map-section {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 20px;
  margin-top: 24px;
  align-items: start;
}"""
new4 = """.map-section {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 8px;
  align-items: stretch;
  min-height: 0;
  flex: 1;
}"""
css = css.replace(old4, new4)

# 5) map-left: remove overflow hidden issue
old5 = """.map-left {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}"""
new5 = """.map-left {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}"""
css = css.replace(old5, new5)

# 6) map-container compact
old6 = """.map-container {
  padding: 8px 10px;
  background: linear-gradient(160deg, #e8f0fe 0%, #f0f7ff 50%, #f8fafc 100%);
  min-height: 340px;
}"""
new6 = """.map-container {
  padding: 4px 8px;
  background: linear-gradient(160deg, #e8f0fe 0%, #f0f7ff 50%, #f8fafc 100%);
  flex: 1;
  min-height: 0;
  overflow: hidden;
}"""
css = css.replace(old6, new6)

# 7) map-header compact
old7 = """.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}"""
new7 = """.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  flex-shrink: 0;
}"""
css = css.replace(old7, new7)

# 8) map-header h3 compact
old8 = """.map-header h3 {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}"""
new8 = """.map-header h3 {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1px 0;
}"""
css = css.replace(old8, new8)

# 9) map-right compact
old9 = """.map-right {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  min-height: 480px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}"""
new9 = """.map-right {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}"""
css = css.replace(old9, new9)

# 10) map-legend compact
old10 = """.map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  padding: 12px 20px;
  border-top: 1px solid var(--border);
  background: #f8fafc;
}"""
new10 = """.map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 10px;
  padding: 6px 12px;
  border-top: 1px solid var(--border);
  background: #f8fafc;
  flex-shrink: 0;
}"""
css = css.replace(old10, new10)

# 11) chart-wrap height compact
old11 = """.chart-wrap {
  position: relative;
  width: 100%;
  height: calc(100% - 36px); /* descontar el header */"""
new11 = """.chart-wrap {
  position: relative;
  width: 100%;
  height: calc(100% - 32px); /* descontar el header */"""
css = css.replace(old11, new11)

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\styles.css', 'wb') as f:
    f.write(css.encode('latin-1'))

print('styles.css patched successfully')
