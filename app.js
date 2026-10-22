/* ── Calendario interactivo ── */
.cal-month-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  padding: 0 4px;
  gap: 8px;
}
.cal-month-title {
  font-weight: 700;
  font-size: 15px;
  color: #f1f5f9;
}
.cal-clear-btn {
  background: rgba(184,35,82,0.15);
  border: 1px solid rgba(184,35,82,0.4);
  color: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all .15s;
}
.cal-clear-btn:hover { background: rgba(184,35,82,0.3); }

.month-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
.month-header-day {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  padding: 6px 0;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.month-day {
  position: relative;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  border-radius: 8px;
  color: #cbd5e1;
  background: rgba(255,255,255,0.02);
  cursor: default;
  transition: all .15s;
  user-select: none;
}
.month-day.empty { background: transparent; }
.month-day.has-event {
  cursor: pointer;
  background: rgba(184,35,82,0.15);
  color: #f1f5f9;
  font-weight: 600;
  border: 1px solid rgba(184,35,82,0.35);
}
.month-day.has-event:hover {
  background: rgba(184,35,82,0.3);
  transform: scale(1.05);
}
.month-day.is-rezagados {
  background: rgba(220,38,38,0.2);
  border-color: rgba(220,38,38,0.5);
}
.month-day.is-rezagados:hover { background: rgba(220,38,38,0.35); }
.month-day.selected {
  outline: 2px solid #b82352;
  outline-offset: 1px;
  background: rgba(184,35,82,0.45);
}
.month-day-indicator {
  position: absolute;
  bottom: 4px;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #b82352;
}
.month-day.is-rezagados .month-day-indicator { background: #dc2626; }
