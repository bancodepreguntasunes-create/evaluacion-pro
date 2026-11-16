# -*- coding: utf-8 -*-
"""
Corrige los estilos CSS del mapa vectorial para que sea visualmente limpio,
distinguible y profesional - con relleno real de colores por estado.
"""
import os, re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

with open(os.path.join(BASE_DIR, "styles.css"), "r", encoding="utf-8") as f:
    css = f.read()

# Remove old map-state styles and add clean ones
old_map_state = r'\.map-state \{[^}]+\}'
new_map_state = """.map-state {
  fill: #d4e6c3;
  stroke: #ffffff;
  stroke-width: 1.0px;
  stroke-linejoin: round;
  transition: fill 0.35s ease, filter 0.2s ease, stroke-width 0.2s;
  cursor: pointer;
}"""

css = re.sub(old_map_state, new_map_state, css)

# Fix hover to not remove the fill
old_hover = r'\.map-state:hover \{[^}]+\}'
new_hover = """.map-state:hover {
  filter: brightness(1.12) drop-shadow(0 2px 6px rgba(0,0,0,0.25));
  stroke: #800020;
  stroke-width: 2px;
}"""
css = re.sub(old_hover, new_hover, css)

# Remove old selected/dimmed if present
old_selected = r'\.map-state\.selected \{[^}]+\}'
new_selected = """.map-state.selected {
  stroke: #0f172a !important;
  stroke-width: 2.5px !important;
  filter: drop-shadow(0 0 8px rgba(15,23,42,0.4)) !important;
}"""
if '.map-state.selected' in css:
    css = re.sub(old_selected, new_selected, css)
else:
    css += "\n" + new_selected

old_dimmed = r'\.map-state\.dimmed \{[^}]+\}'
new_dimmed = """.map-state.dimmed {
  opacity: 0.5;
}"""
if '.map-state.dimmed' in css:
    css = re.sub(old_dimmed, new_dimmed, css)
else:
    css += "\n" + new_dimmed

# Fix map-label text styles
if '.map-label' not in css:
    css += """
.map-label {
  font-family: 'Inter', sans-serif;
  font-size: 7.5px;
  font-weight: 700;
  fill: #1e293b;
  pointer-events: none;
  user-select: none;
  text-anchor: middle;
  dominant-baseline: middle;
}"""

# Fix map container to have a visible background
map_container_old = r'\.map-container \{[^}]+\}'
map_container_new = """.map-container {
  background: #cce8f5;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  width: 100%;
  min-height: 350px;
}"""
if '.map-container' in css:
    css = re.sub(map_container_old, map_container_new, css)
else:
    css += "\n" + map_container_new

# Fix map-left/right layout
map_section_new = """
/* ===================== MAP SECTION OVERHAUL ===================== */
.map-section {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 16px;
  margin-bottom: 24px;
  align-items: start;
}

@media (max-width: 1024px) {
  .map-section { grid-template-columns: 1fr; }
}

.map-left {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15,23,42,0.05);
}

.map-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 16px 20px 10px 20px;
  border-bottom: 1px solid #f1f5f9;
  flex-wrap: wrap;
  gap: 10px;
}

.map-header h3 {
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 2px 0;
}

.map-header p {
  font-size: 11.5px;
  color: #64748b;
  margin: 0;
}

.map-container {
  background: #cce8f5;
  overflow: hidden;
  position: relative;
  width: 100%;
  min-height: 360px;
}

.map-container svg {
  display: block;
  width: 100%;
  height: auto;
}

.map-right {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 2px 8px rgba(15,23,42,0.05);
  min-height: 400px;
  overflow-y: auto;
}

/* ===================== NUCLEO PINS ===================== */
.map-nucleo-pin {
  transition: transform 0.2s ease;
  cursor: pointer;
}

.map-nucleo-pin:hover {
  transform: scale(1.5);
}

.nucleo-pulse {
  transform-origin: center center;
  transform-box: fill-box;
}

.map-nucleo-pin.pin-active .nucleo-pulse {
  animation: pulse-ring 1.8s ease-out infinite;
  transform-origin: center;
  transform-box: fill-box;
}

@keyframes pulse-ring {
  0%   { r: 7; opacity: 0.6; }
  60%  { r: 15; opacity: 0.1; }
  100% { r: 20; opacity: 0; }
}

/* ===================== MAP TOOLTIP ===================== */
#mapTooltip {
  display: none;
  position: fixed;
  background: #0f172a;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.6;
  padding: 10px 14px;
  border-radius: 10px;
  pointer-events: none;
  z-index: 99999;
  max-width: 220px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
}

/* ===================== LEGEND ===================== */
.map-legend-coropleth {
  padding: 10px 20px;
  border-top: 1px solid #f1f5f9;
  background: #f8fafc;
  border-radius: 0 0 16px 16px;
}

.legend-scale-items {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.legend-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #334155;
  font-weight: 600;
}

.legend-color-box {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 1px solid rgba(0,0,0,0.1);
  flex-shrink: 0;
}

.legend-pin-sample {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #800020;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #800020;
  display: inline-block;
  flex-shrink: 0;
}

/* ===================== COROPLETH TOGGLE ===================== */
.map-controls-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.coropleth-toggle-group {
  display: flex;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 2px;
  border: 1px solid #cbd5e1;
}

.btn-coropleth-toggle {
  padding: 4px 11px;
  font-size: 11px;
  font-weight: 700;
  border: none;
  background: transparent;
  color: #64748b;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-coropleth-toggle.active {
  background: #ffffff;
  color: #800020;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* ===================== MAP PANEL CONTENT ===================== */
.map-panel-body {
  font-family: 'Inter', sans-serif;
}

.btn-link {
  background: none;
  border: none;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  padding: 0;
}
"""

css = css + "\n" + map_section_new

with open(os.path.join(BASE_DIR, "styles.css"), "w", encoding="utf-8") as f:
    f.write(css)

print("styles.css actualizado con estilos correctos para el mapa vectorial.")
