with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 12. Fix ceoViewHistorico to use canvas ──
OLD_HIST_START = 'function ceoViewHistorico() {'
OLD_HIST_END   = '\n// ── ABSENTISMO'

start_i = src.index(OLD_HIST_START)
end_i   = src.index(OLD_HIST_END, start_i)

NEW_HIST = r"""function ceoViewHistorico() {
  return `
  <div class="page-header">
    <div class="page-title">Histórico &amp; Evaluación</div>
    <div class="page-subtitle">Ciclo mesurar → corregir → avaluar · 12 semanas</div>
  </div>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-label">Índice empresa (actual)</div><div class="kpi-value">63<span class="kpi-value-unit">/100</span></div><div class="kpi-trend trend-down">↓ -5 vs hace 8 semanas</div></div>
    <div class="kpi-card"><div class="kpi-label">Índice hace 8 semanas</div><div class="kpi-value">68<span class="kpi-value-unit">/100</span></div><div class="kpi-trend trend-neutral">— referencia S13</div></div>
    <div class="kpi-card"><div class="kpi-label">Acciones aplicadas (90d)</div><div class="kpi-value">7</div><div class="kpi-trend">3 completadas · 4 en curso</div></div>
    <div class="kpi-card"><div class="kpi-label">Predicción IA (+4 sem.)</div><div class="kpi-value">67<span class="kpi-value-unit">/100</span></div><div class="kpi-trend trend-up">↑ +4 si se aplican acciones</div></div>
  </div>
  <div class="chart-card" style="margin-bottom:20px">
    <div class="chart-card-title" style="margin-bottom:12px">Evolución por departamento · Semanas 10–21</div>
    <div style="position:relative;height:260px"><canvas id="chart-historico"></canvas></div>
  </div>
  <div class="table-card" style="margin-bottom:20px">
    <div class="table-header">Acciones implementadas y su impacto</div>
    <table>
      <thead><tr><th>Acción</th><th>Equipo</th><th>Semana</th><th>Impacto medido</th><th>Estado</th></tr></thead>
      <tbody>
        <tr><td>Bloqueo Deep Work (IA)</td><td>Producto &amp; Tech</td><td>S18</td><td style="color:var(--green)">+4 pts bienestar</td><td><span class="status-badge status-green">✅ Completada</span></td></tr>
        <tr><td>Redistribución carga</td><td>Operaciones</td><td>S19</td><td style="color:var(--amber)">+2 pts (parcial)</td><td><span class="status-badge status-amber">🔄 En curso</span></td></tr>
        <tr><td>Recordatorio descanso</td><td>Operaciones</td><td>S20</td><td style="color:var(--green)">+1 pt bienestar</td><td><span class="status-badge status-green">✅ Completada</span></td></tr>
        <tr><td>Día de recuperación</td><td>Soporte</td><td>S20</td><td style="color:var(--ink3)">En evaluación</td><td><span class="status-badge status-amber">🔄 En curso</span></td></tr>
      </tbody>
    </table>
  </div>
  <div class="callout-card"><p>🤖 <strong>Insight IA:</strong> Las acciones de tipo «bloqueo de tiempo» tienen un <strong>73% más de efectividad</strong>. Con 3 acciones pendientes, el índice subirá a <strong>67/100 en 4 semanas</strong>.</p></div>`;
}

"""
src = src[:start_i] + NEW_HIST + src[end_i:]

# ── 13. Patch renderEmpView to call tendencia chart ──
OLD_EMP_RENDER = """function renderEmpView(viewId) {
  setActiveNav(viewId);
  const mc = document.getElementById('main-content');
  mc.innerHTML = '';
  mc.className = 'main-content fade-enter';
  if (viewId === 'checkin')      mc.innerHTML = empViewCheckin();
  else if (viewId === 'tendencia') mc.innerHTML = empViewTendencia();
  else if (viewId === 'sugerencias') mc.innerHTML = empViewSugerencias();
  else if (viewId === 'calendario') mc.innerHTML = empViewCalendario();
  else if (viewId === 'bolsahoras') mc.innerHTML = empViewBolsaHoras();
  else if (viewId === 'formacion') mc.innerHTML = empViewFormacion();
  else if (viewId === 'misdatos') mc.innerHTML = empViewMisDatos();
}"""

NEW_EMP_RENDER = """function renderEmpView(viewId) {
  destroyAllCharts();
  setActiveNav(viewId);
  const mc = document.getElementById('main-content');
  mc.innerHTML = '';
  mc.className = 'main-content fade-enter';
  if (viewId === 'checkin')        mc.innerHTML = empViewCheckin();
  else if (viewId === 'tendencia') mc.innerHTML = empViewTendencia();
  else if (viewId === 'sugerencias') mc.innerHTML = empViewSugerencias();
  else if (viewId === 'calendario') mc.innerHTML = empViewCalendario();
  else if (viewId === 'bolsahoras') mc.innerHTML = empViewBolsaHoras();
  else if (viewId === 'formacion') mc.innerHTML = empViewFormacion();
  else if (viewId === 'misdatos')  mc.innerHTML = empViewMisDatos();
  if (viewId === 'tendencia') setTimeout(attachEmpTendenciaChart, 0);
}"""
src = src.replace(OLD_EMP_RENDER, NEW_EMP_RENDER, 1)

# ── 14. Replace empViewTendencia with canvas version ──
OLD_TEND_START = 'function empViewTendencia() {'
# find next function after it
OLD_TEND_END   = '\n// ── SUGERENCIAS IA'

start_t = src.index(OLD_TEND_START)
end_t   = src.index(OLD_TEND_END, start_t)

NEW_TEND = r"""function empViewTendencia() {
  const e=employees.find(x=>x.id==='e25')||employees[0];
  return `
  <div class="page-header">
    <div class="page-title">Mi Tendencia</div>
    <div class="page-subtitle">Evolución de tu bienestar · Últimas 8 semanas</div>
  </div>
  <div class="line-chart-card">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
      <div class="chart-card-title" style="margin-bottom:0">Índice de Bienestar Personal</div>
      <span class="status-badge ${statusBadgeClass(e.status)}">${statusLabel(e.status)}</span>
    </div>
    <div style="position:relative;height:220px"><canvas id="chart-tend-emp"></canvas></div>
  </div>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-value" style="color:${e.metrics.horasExtra>2?'var(--terra)':'var(--green)'}">${e.metrics.horasExtra>0?'+':''}${e.metrics.horasExtra}h</div><div class="stat-label">Horas extra estimadas</div></div>
    <div class="stat-card"><div class="stat-value" style="color:${e.metrics.reuniones>6?'var(--terra)':e.metrics.reuniones>4?'var(--amber)':'var(--green)'}">${e.metrics.reuniones}</div><div class="stat-label">Reuniones/día</div></div>
    <div class="stat-card"><div class="stat-value" style="color:${e.metrics.cargaTareas>110?'var(--amber)':'var(--green)'}">${e.metrics.cargaTareas}%</div><div class="stat-label">Carga de trabajo</div></div>
    <div class="stat-card"><div class="stat-value" style="color:var(--cobalt)">${e.metrics.productividad}</div><div class="stat-label">Productividad</div></div>
  </div>
  <div class="compare-card">
    <div class="chart-card-title" style="margin-bottom:12px">Insights personales</div>
    <div class="compare-item"><div class="compare-dot" style="background:var(--cobalt)"></div><div class="compare-text">Tu índice actual: <strong>${e.index}/100</strong> — ${e.index>=70?'Zona de bienestar ✅':e.index>=40?'Zona de atención ⚠️':'Zona crítica 🚨'}</div></div>
    <div class="compare-item"><div class="compare-dot" style="background:var(--amber)"></div><div class="compare-text">Tendencia 8 semanas: <strong>${e.trend[7]>e.trend[0]?'↑ Mejorando':e.trend[7]<e.trend[0]-3?'↓ Decreciendo':'→ Estable'}</strong> (${e.trend[0]} → ${e.trend[7]})</div></div>
    <div class="compare-item"><div class="compare-dot" style="background:var(--green)"></div><div class="compare-text">Mejor semana: <strong>S${e.trend.indexOf(Math.max(...e.trend))+13} (${Math.max(...e.trend)}/100)</strong></div></div>
    ${e.signals.map(s=>`<div class="compare-item"><div class="compare-dot" style="background:${s.sev==='red'?'var(--terra)':s.sev==='amber'?'var(--amber)':'var(--green)'}"></div><div class="compare-text">${s.text}</div></div>`).join('')}
  </div>`;
}

function attachEmpTendenciaChart(){
  const e=employees.find(x=>x.id==='e25')||employees[0];
  const ctx=document.getElementById('chart-tend-emp');
  if(!ctx) return;
  const weeks=['S13','S14','S15','S16','S17','S18','S19','S20'];
  const TOOLTIP={backgroundColor:'#0F172A',padding:10,cornerRadius:6,titleFont:{family:'Inter',size:11},bodyFont:{family:'Inter',size:12}};
  if(charts.empTend) try{charts.empTend.destroy();}catch(x){}
  charts.empTend=new Chart(ctx,{type:'line',data:{labels:weeks,datasets:[
    {label:'Mi Bienestar',data:e.trend,borderColor:e.avatarColor,backgroundColor:e.avatarColor+'20',tension:.4,fill:true,pointBackgroundColor:e.trend.map(v=>v>=70?'#059669':v>=40?'#D97706':'#DC2626'),pointRadius:6,pointHoverRadius:9},
    {label:'Umbral bienestar (70)',data:Array(8).fill(70),borderColor:'#059669',borderDash:[5,4],borderWidth:1.5,pointRadius:0,fill:false}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:{family:'Inter',size:11},usePointStyle:true,padding:12},position:'bottom'},tooltip:TOOLTIP},scales:{x:{grid:{display:false},ticks:{font:{family:'Inter',size:11},color:'#7A8394'}},y:{min:20,max:100,grid:{color:'rgba(15,20,25,0.05)'},ticks:{font:{family:'Inter',size:11},color:'#7A8394',callback:v=>v+'/100'}}}}});
}

"""
src = src[:start_t] + NEW_TEND + src[end_t:]

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 9 done. Lines:", src.count('\n'))
