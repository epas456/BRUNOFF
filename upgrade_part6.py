with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 9. Add ceoViewEmployeeDetail after switchTeam ──
NEW_EMP_DETAIL = r"""
function ceoViewEmployeeDetail(id){
  const e = employees.find(x=>x.id===id);
  if(!e) return '<div style="padding:40px;text-align:center;color:var(--ink3)">Empleado no encontrado</div>';
  const weekLabels=['S13','S14','S15','S16','S17','S18','S19','S20'];
  const radarLabels=['Energía','Concentración','Satisfacción','Carga (inv.)','Relaciones','Autonomía'];
  const radarInv=[e.radar[0],e.radar[1],e.radar[2],100-e.metrics.cargaTareas,e.radar[4],e.radar[5]];
  return `
  <button class="back-btn" onclick="renderCEOView('equipos')">← Volver a Equipos</button>
  <div class="emp-detail-hdr">
    <div class="emp-detail-av" style="background:${e.avatarColor}">${e.avatar}</div>
    <div class="emp-detail-info">
      <div class="emp-detail-name">${e.name}</div>
      <div class="emp-detail-role">${e.role} · ${e.dept}</div>
      <div class="emp-meta-chips">
        <span class="emp-meta-chip">📧 ${e.email}</span>
        <span class="emp-meta-chip">👤 ${e.age} años</span>
        <span class="emp-meta-chip status-badge ${statusBadgeClass(e.status)}">${statusLabel(e.status)}</span>
        <span class="emp-meta-chip risk-pill ${riskClass(e.risk)}">Riesgo ${riskLabel(e.risk)}: ${e.risk}%</span>
      </div>
    </div>
    <div class="emp-idx-big">
      <div class="emp-idx-num" style="color:${idxColor(e.index)}">${e.index}</div>
      <div class="emp-idx-sub">Índice Bienestar</div>
      <div style="font-size:11px;color:var(--ink4);margin-top:4px">/100 global</div>
    </div>
  </div>

  <!-- KPI ROW -->
  <div class="kpi-grid" style="margin-bottom:16px">
    <div class="kpi-card">
      <div class="kpi-label">Horas extra/día</div>
      <div class="kpi-value ${e.metrics.horasExtra>3?'':''}">
        <span style="color:${e.metrics.horasExtra>3?'var(--terra)':e.metrics.horasExtra>1?'var(--amber)':'var(--green)'}">${e.metrics.horasExtra}h</span>
      </div>
      <div class="kpi-trend ${e.metrics.horasExtra>2?'trend-down':'trend-up'}">${e.metrics.horasExtra>2?'Por encima del límite saludable':'Dentro del rango normal'}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Reuniones/día</div>
      <div class="kpi-value"><span style="color:${e.metrics.reuniones>6?'var(--terra)':e.metrics.reuniones>4?'var(--amber)':'var(--green)'}">${e.metrics.reuniones}</span></div>
      <div class="kpi-trend ${e.metrics.reuniones>6?'trend-down':'trend-neutral'}">${e.metrics.reuniones>6?'Alta fragmentación cognitiva':'Nivel manejable'}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Carga de trabajo</div>
      <div class="kpi-value"><span style="color:${e.metrics.cargaTareas>130?'var(--terra)':e.metrics.cargaTareas>100?'var(--amber)':'var(--green)'}">${e.metrics.cargaTareas}%</span></div>
      <div class="kpi-trend ${e.metrics.cargaTareas>130?'trend-down':e.metrics.cargaTareas>100?'trend-warn':'trend-up'}">${e.metrics.cargaTareas>100?'Por encima de capacidad':'Dentro de capacidad'}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Teletrabajo</div>
      <div class="kpi-value">${e.metrics.teletrabajo}<span class="kpi-value-unit"> días/sem</span></div>
      <div class="kpi-trend trend-neutral">Patrón de trabajo</div>
    </div>
  </div>

  <!-- CHARTS 2-col -->
  <div class="emp-charts-grid">
    <div class="chart-card">
      <div class="chart-card-title">Evolución Índice Bienestar — Últimas 8 semanas</div>
      <div style="position:relative;height:200px">
        <canvas id="chart-emp-trend"></canvas>
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-card-title">Perfil de Bienestar — Radar</div>
      <div style="position:relative;height:200px">
        <canvas id="chart-emp-radar"></canvas>
      </div>
      <div class="radar-legend">
        ${radarLabels.map((l,i)=>`<div class="radar-litem"><div class="radar-dot" style="background:${e.avatarColor}"></div>${l}</div>`).join('')}
      </div>
    </div>
  </div>

  <!-- CHECK-IN LAST WEEK -->
  <div class="chart-card" style="margin-bottom:16px">
    <div class="chart-card-title">Último Check-in Semanal (anónimo agregado)</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px">
      ${[['⚡ Energía',e.checkin.energia],['😤 Estrés (inv.)',10-e.checkin.estres],['😊 Satisfacción',e.checkin.satisfaccion],['🤝 Apoyo recibido',e.checkin.apoyo]].map(([l,v])=>`
      <div style="text-align:center;padding:12px;background:var(--bg);border-radius:var(--r);border:1px solid var(--border)">
        <div style="font-size:20px;font-weight:600;color:${v>=7?'var(--green)':v>=5?'var(--amber)':'var(--terra)'}">${v}/10</div>
        <div style="font-size:11px;color:var(--ink3);margin-top:4px">${l}</div>
        <div style="height:4px;background:var(--border-md);border-radius:100px;margin-top:6px;overflow:hidden"><div style="height:100%;width:${v*10}%;background:${v>=7?'var(--green)':v>=5?'var(--amber)':'var(--terra)'};border-radius:100px"></div></div>
      </div>`).join('')}
    </div>
  </div>

  <!-- SIGNALS -->
  <div class="chart-card" style="margin-bottom:16px">
    <div class="chart-card-title">Señales Detectadas por BURNOFF-AI</div>
    <div style="margin-top:8px">
      ${e.signals.map(s=>`<div class="sig-item sig-${s.sev}"><span class="sig-icon">${s.icon}</span><span class="sig-text">${s.text}</span></div>`).join('')}
    </div>
  </div>

  <!-- AI RECOMMENDATIONS -->
  <div class="chart-card" style="margin-bottom:16px;border-left:3px solid var(--cobalt-mid)">
    <div class="chart-card-title">🤖 Recomendaciones BURNOFF-AI</div>
    <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px">
      ${e.risk>=70?`
      <div style="padding:12px;background:var(--terra-light);border-radius:var(--r);border:1px solid rgba(220,38,38,.15)">
        <div style="font-size:12px;font-weight:600;color:var(--terra);margin-bottom:4px">🚨 Intervención urgente recomendada</div>
        <div style="font-size:12px;color:var(--ink2)">El perfil de ${e.name} indica riesgo de baja por burnout en las próximas 4–6 semanas si no se actúa. Se recomienda conversación privada con RRHH y reducción de carga inmediata.</div>
      </div>`:e.risk>=40?`
      <div style="padding:12px;background:var(--amber-light);border-radius:var(--r);border:1px solid rgba(217,119,6,.15)">
        <div style="font-size:12px;font-weight:600;color:var(--amber);margin-bottom:4px">⚠️ Seguimiento recomendado</div>
        <div style="font-size:12px;color:var(--ink2)">Tendencia de atención. Se recomienda check-in 1:1 con el manager y revisión de carga de trabajo en las próximas 2 semanas.</div>
      </div>`:`
      <div style="padding:12px;background:var(--green-light);border-radius:var(--r);border:1px solid rgba(5,150,105,.15)">
        <div style="font-size:12px;font-weight:600;color:var(--green);margin-bottom:4px">✅ Indicadores saludables</div>
        <div style="font-size:12px;color:var(--ink2)">El perfil de ${e.name} muestra indicadores positivos. Mantener las condiciones actuales y continuar el seguimiento semanal.</div>
      </div>`}
      <div style="padding:12px;background:var(--cobalt-light);border-radius:var(--r)">
        <div style="font-size:12px;font-weight:600;color:var(--cobalt);margin-bottom:4px">📋 Acciones sugeridas</div>
        <ul style="font-size:12px;color:var(--ink2);margin:0;padding-left:16px;line-height:1.8">
          ${e.metrics.horasExtra>2?'<li>Reducir extensión horaria — limitar horas extra a máx. 1h/día</li>':''}
          ${e.metrics.reuniones>5?'<li>Bloquear tiempo de concentración (Deep Work) 10:00–12:00</li>':''}
          ${e.metrics.cargaTareas>110?'<li>Redistribuir al menos 2 tareas a otros miembros del equipo</li>':''}
          <li>Próximo check-in individual: ${e.risk>=60?'Esta semana':'Próximas 2 semanas'}</li>
        </ul>
      </div>
    </div>
  </div>
  <div style="font-size:11px;color:var(--ink4);text-align:center;margin-top:4px">🔒 Datos anonimizados conforme RGPD · El empleado no puede ser identificado fuera del sistema</div>`;
}
"""

# Insert after switchTeam function
ANCHOR = '\nfunction applyTeamAction(key, btn) {'
src = src.replace(ANCHOR, NEW_EMP_DETAIL + '\nfunction applyTeamAction(key, btn) {', 1)

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 6 done. Lines:", src.count('\n'))
