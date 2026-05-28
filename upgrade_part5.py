with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 8. Replace ceoViewEquipos with version that shows employee list ──
OLD_EQ_START = 'function ceoViewEquipos() {'
OLD_EQ_END   = '\nfunction switchTeam(idx) {'

start_i = src.index(OLD_EQ_START)
end_i   = src.index(OLD_EQ_END, start_i)

NEW_EQ = r"""function ceoViewEquipos() {
  const t = teams[selectedTeam];
  const statusMap = {green:'status-green',amber:'status-amber',red:'status-red'};
  const statusLbl = {green:'🌿 Bienestar',amber:'⚠️ Atención',red:'🚨 Situación Crítica'};
  const totalPct = t.verde + t.ambar + t.rojo;
  const vPct = Math.round(t.verde/totalPct*100);
  const aPct = Math.round(t.ambar/totalPct*100);
  const rPct = 100-vPct-aPct;
  const originLabel = {company:'🏢 Compañía',worker:'👤 Trabajador'};
  const deptEmps = getEmpsByDept(t.name).sort((a,b)=>a.index-b.index);

  let tabsHtml='<div class="team-tabs">';
  teams.forEach((tm,i)=>{
    tabsHtml+=`<div class="team-tab ${i===selectedTeam?'active':''}" onclick="switchTeam(${i})">${tm.name}</div>`;
  });
  tabsHtml+='</div>';

  let signalsHtml='';
  t.signals.forEach(s=>{
    signalsHtml+=`<div class="signal-item"><div class="signal-left"><span class="signal-icon">${s.icon}</span><div><span class="signal-name">${s.name}</span><span class="origin-badge">${originLabel[s.origin]||'🏢 Compañía'}</span></div></div><div style="text-align:right"><div class="signal-value">${s.value}</div><div class="signal-bar-wrap"><div class="signal-bar-fill" style="width:${s.pct}%"></div></div></div></div>`;
  });

  let empRowsHtml = deptEmps.length ? deptEmps.map(e=>`
    <tr onclick="openEmployee('${e.id}')">
      <td><div class="emp-name-wrap"><div class="emp-av" style="background:${e.avatarColor}">${e.avatar}</div><div><div class="emp-name">${e.name}</div><div class="emp-role-sm">${e.role}</div></div></div></td>
      <td><div class="idx-bar-wrap"><span style="font-family:'JetBrains Mono',monospace;font-weight:600;font-size:13px;color:${idxColor(e.index)}">${e.index}</span><div class="idx-bar"><div class="idx-bar-fill" style="width:${e.index}%;background:${idxColor(e.index)}"></div></div></div></td>
      <td><span class="status-badge ${statusBadgeClass(e.status)}">${statusLabel(e.status)}</span></td>
      <td><span class="risk-pill ${riskClass(e.risk)}">${riskLabel(e.risk)} ${e.risk}%</span></td>
      <td style="color:${e.trend[7]>e.trend[0]?'var(--green)':e.trend[7]<e.trend[0]-5?'var(--terra)':'var(--ink3)'}">${e.trend[7]>e.trend[0]?'↑ Mejorando':e.trend[7]<e.trend[0]-5?'↓ Bajando':'→ Estable'}</td>
      <td><span style="font-size:11px;color:var(--cobalt-mid)">Ver perfil →</span></td>
    </tr>`).join('') : `<tr><td colspan="6" style="text-align:center;color:var(--ink3);padding:20px">No hay perfiles individuales para este equipo en el demo.</td></tr>`;

  return `
  <div class="page-header">
    <div class="page-title">Equipos</div>
    <div class="page-subtitle">Análisis por equipo e individuos · Semana 21</div>
  </div>
  ${tabsHtml}
  <div class="team-header-card">
    <div class="team-header-top">
      <div>
        <div class="team-name">${t.name}</div>
        <div class="team-meta"><span>👤 ${t.manager}</span><span>👥 ${t.count} personas</span><span>📊 Índice ${t.index}/100</span></div>
      </div>
      <span class="status-badge ${statusMap[t.status]}" style="font-size:13px;padding:5px 12px">${statusLbl[t.status]}</span>
    </div>
    <div class="distribution-bar">
      <div class="dist-green" style="width:${vPct}%"></div>
      <div class="dist-amber" style="width:${aPct}%"></div>
      <div class="dist-red" style="width:${rPct}%"></div>
    </div>
    <div class="dist-labels">
      <span class="dist-label"><span style="width:8px;height:8px;border-radius:50%;background:var(--green);display:inline-block"></span>${t.verde} Bienestar</span>
      <span class="dist-label"><span style="width:8px;height:8px;border-radius:50%;background:var(--amber);display:inline-block"></span>${t.ambar} Atención</span>
      <span class="dist-label"><span style="width:8px;height:8px;border-radius:50%;background:var(--terra);display:inline-block"></span>${t.rojo} Situación Crítica</span>
    </div>
    <div style="position:relative;height:140px;margin-top:12px">
      <canvas id="chart-team-trend"></canvas>
    </div>
  </div>

  <div class="signals-card"><div class="chart-card-title" style="margin-bottom:4px">Señales detectadas esta semana</div>${signalsHtml}</div>

  <!-- EMPLOYEE LIST -->
  <div class="table-card" style="margin-top:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
      <div class="table-header" style="margin-bottom:0">Perfiles individuales — ${t.name}</div>
      <span style="font-size:11px;color:var(--ink3)">${deptEmps.length} perfiles · Haz clic para ver detalle</span>
    </div>
    <table class="emp-table">
      <thead><tr><th>Empleado</th><th>Índice</th><th>Estado</th><th>Riesgo Burnout</th><th>Tendencia</th><th></th></tr></thead>
      <tbody>${empRowsHtml}</tbody>
    </table>
  </div>

  <div class="chart-card" style="margin-top:16px">
    <div class="chart-card-title">Acciones recomendadas</div>
    <div style="display:flex;flex-direction:column;gap:10px;margin-top:4px">
      <div style="padding:12px 16px;background:var(--bg);border-radius:var(--r);border:1px solid var(--border)">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px">
          <div style="flex:1">
            <div style="margin-bottom:4px"><span style="font-family:'JetBrains Mono',monospace;color:var(--ink3);font-size:10px;margin-right:8px">R-01</span><span class="actor-badge actor-ia">🤖 IA</span><span class="type-badge type-supervised">👁️ Supervisión</span></div>
            <div style="font-size:12px;font-weight:600;color:var(--ink);margin-bottom:2px">Redistribuir carga de trabajo</div>
            <div style="font-size:11px;color:var(--ink3)">Reasignar tareas de empleados >130% a empleados <80%</div>
            <div class="action-responsibility"><span class="resp-label">Ejecuta:</span> Manager ${t.name} &nbsp;<span class="resp-label">Verifica:</span> RRHH</div>
          </div>
          <button class="btn-sm btn-cobalt" onclick="applyTeamAction('t${selectedTeam}-r01',this)">Revisar y aplicar</button>
        </div>
      </div>
      <div style="padding:12px 16px;background:var(--bg);border-radius:var(--r);border:1px solid var(--border)">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px">
          <div style="flex:1">
            <div style="margin-bottom:4px"><span style="font-family:'JetBrains Mono',monospace;color:var(--ink3);font-size:10px;margin-right:8px">R-02</span><span class="actor-badge actor-ia">🤖 IA</span><span class="type-badge type-supervised">👁️ Supervisión</span></div>
            <div style="font-size:12px;font-weight:600;color:var(--ink);margin-bottom:2px">Bloquear Deep Work 10:00–12:00</div>
            <div style="font-size:11px;color:var(--ink3)">Reservar bloque de concentración sin reuniones para todo el equipo</div>
            <div class="action-responsibility"><span class="resp-label">Ejecuta:</span> Manager ${t.name} &nbsp;<span class="resp-label">Verifica:</span> RRHH</div>
          </div>
          <button class="btn-sm btn-cobalt" onclick="applyTeamAction('t${selectedTeam}-r02',this)">Revisar y aplicar</button>
        </div>
      </div>
    </div>
  </div>`;
}
"""

src = src[:start_i] + NEW_EQ + src[end_i:]

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 5 done. Lines:", src.count('\n'))
