with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 7. Replace ceoViewDashboard ──
import re
OLD_DASH_START = 'function ceoViewDashboard() {'
OLD_DASH_END   = '\nfunction attachCEOEvents(viewId) {'

start_i = src.index(OLD_DASH_START)
end_i   = src.index(OLD_DASH_END, start_i)

NEW_DASH = r"""function ceoViewDashboard() {
  const s = getCompanyStats();
  const weekLabels = ['S13','S14','S15','S16','S17','S18','S19','S20','S21'];
  // company trend = average of all employee last trends
  const weeks=8;
  const companyTrend=Array.from({length:weeks},(_,i)=>
    Math.round(employees.reduce((sum,e)=>sum+e.trend[i],0)/employees.length));
  const critList = employees.filter(e=>e.risk>=65).sort((a,b)=>b.risk-a.risk).slice(0,5);
  const deptStats = ['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'].map(d=>{
    const emps=getEmpsByDept(d);
    const avg=Math.round(emps.reduce((s,e)=>s+e.index,0)/emps.length);
    const red=emps.filter(e=>e.status==='red').length;
    return {name:d,avg,red,count:emps.length};
  });

  return `
  <div class="page-header">
    <div class="page-title">Dashboard de Empresa</div>
    <div class="page-subtitle">Visión global del bienestar organizacional · ${s.n} empleados · Semana 21</div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Índice Bienestar Empresa</div>
      <div class="kpi-value">${s.avg}<span class="kpi-value-unit">/100</span></div>
      <div class="kpi-trend ${s.avg>=70?'trend-up':s.avg>=50?'trend-warn':'trend-down'}">${s.avg>=70?'↑ Zona bienestar':s.avg>=50?'⚠ Zona atención':'↓ Zona crítica'}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">🌿 En Bienestar</div>
      <div class="kpi-value" style="color:var(--green)">${s.green}</div>
      <div class="kpi-trend trend-up">${Math.round(s.green/s.n*100)}% de la plantilla</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">⚠️ En Atención</div>
      <div class="kpi-value" style="color:var(--amber)">${s.amber}</div>
      <div class="kpi-trend trend-warn">${Math.round(s.amber/s.n*100)}% requieren seguimiento</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">🚨 Situación Crítica</div>
      <div class="kpi-value" style="color:var(--terra)">${s.red}</div>
      <div class="kpi-trend trend-down">Riesgo de baja inminente</div>
    </div>
  </div>

  <div class="dashboard-grid">
    <div class="dashboard-main">
      <!-- TREND CHART -->
      <div class="chart-card" style="margin-bottom:16px">
        <div class="chart-card-title">Tendencia Índice de Bienestar — Empresa · Últimas 8 semanas</div>
        <div style="position:relative;height:180px">
          <canvas id="chart-trend"></canvas>
        </div>
      </div>

      <!-- DEPT BREAKDOWN -->
      <div class="chart-card" style="margin-bottom:16px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
          <div class="chart-card-title" style="margin-bottom:0">Índice por Departamento</div>
          <button class="btn-sm btn-outline" onclick="renderCEOView('equipos')">Ver empleados →</button>
        </div>
        <div style="position:relative;height:160px">
          <canvas id="chart-dept"></canvas>
        </div>
      </div>

      <!-- CRITICAL EMPLOYEES TABLE -->
      <div class="table-card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
          <div class="table-header" style="margin-bottom:0">Empleados de Mayor Riesgo</div>
          <button class="btn-sm btn-outline" onclick="renderCEOView('equipos')">Ver todos →</button>
        </div>
        <table class="emp-table">
          <thead><tr><th>Empleado</th><th>Dpto</th><th>Índice</th><th>Riesgo Burnout</th><th></th></tr></thead>
          <tbody>
            ${critList.map(e=>`<tr onclick="openEmployee('${e.id}')">
              <td><div class="emp-name-wrap"><div class="emp-av" style="background:${e.avatarColor}">${e.avatar}</div><div><div class="emp-name">${e.name}</div><div class="emp-role-sm">${e.role}</div></div></div></td>
              <td><span style="font-size:11px;color:var(--ink3)">${e.dept}</span></td>
              <td><span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:${idxColor(e.index)}">${e.index}</span></td>
              <td><span class="risk-pill ${riskClass(e.risk)}">${riskLabel(e.risk)} ${e.risk}%</span></td>
              <td><span style="font-size:11px;color:var(--cobalt-mid);cursor:pointer">Ver →</span></td>
            </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <div class="dashboard-side">
      <!-- DONUT -->
      <div class="chart-card" style="margin-bottom:16px">
        <div class="chart-card-title">Distribución de Bienestar</div>
        <div style="position:relative;height:160px">
          <canvas id="chart-donut"></canvas>
        </div>
        <div style="margin-top:10px;display:flex;flex-direction:column;gap:5px">
          <div class="legend-item"><div class="legend-dot" style="background:var(--green)"></div><div class="legend-label">🌿 Bienestar — ${s.green} empleados</div><div class="legend-pct">${Math.round(s.green/s.n*100)}%</div></div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--amber)"></div><div class="legend-label">⚠️ Atención — ${s.amber} empleados</div><div class="legend-pct">${Math.round(s.amber/s.n*100)}%</div></div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--terra)"></div><div class="legend-label">🚨 Crítico — ${s.red} empleados</div><div class="legend-pct">${Math.round(s.red/s.n*100)}%</div></div>
        </div>
      </div>

      <!-- ALERTS -->
      <div style="font-size:11px;font-weight:600;color:var(--ink3);letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px">Alertas IA</div>
      ${s.critRisk.slice(0,3).map(e=>`
      <div class="alert-card" style="margin-bottom:8px">
        <div class="alert-badge alert-critical">🔴 Riesgo Alto</div>
        <div class="alert-text"><strong>${e.name}</strong> — ${e.signals[0].text}</div>
        <button class="btn-sm btn-cobalt" style="margin-top:6px" onclick="openEmployee('${e.id}')">Ver perfil →</button>
      </div>`).join('')}
      <div class="alert-card" style="margin-top:4px">
        <div class="alert-badge alert-medium">🟡 Recomendación</div>
        <div class="alert-text">Equipo Operaciones necesita intervención. <strong>${getEmpsByDept('Operaciones').filter(e=>e.status==='red').length} personas en situación crítica</strong>.</div>
        <button class="btn-sm btn-outline" style="margin-top:6px" onclick="renderCEOView('acciones')">Ver acciones →</button>
      </div>

      <!-- WEEKLY PULSE -->
      <div style="margin-top:16px;padding:16px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg)">
        <div style="font-size:12px;font-weight:600;color:var(--ink);margin-bottom:10px">💬 Pols de la setmana</div>
        <div style="font-size:11px;color:var(--ink3);margin-bottom:8px;font-style:italic">Comentaris anònims · Sense identificació</div>
        ${!anonTopicsVisible ? `
        <div style="font-size:12px;color:var(--ink2);line-height:1.7;border-left:2px solid var(--border-md);padding-left:8px;margin-bottom:6px">"Massa reunions que podrien ser un email."</div>
        <div style="font-size:12px;color:var(--ink2);line-height:1.7;border-left:2px solid var(--border-md);padding-left:8px;margin-bottom:6px">"Falta feedback sobre el treball fet."</div>
        <div style="font-size:12px;color:var(--ink2);line-height:1.7;border-left:2px solid var(--border-md);padding-left:8px;margin-bottom:10px">"Les eines de comunicació estan fragmentades."</div>
        <button class="btn-sm btn-outline" style="font-size:11px;width:100%" onclick="anonTopicsVisible=true;renderCEOView('dashboard')">🤖 Analitzar amb IA</button>
        ` : `
        <div style="margin-bottom:8px;font-size:11px;color:var(--ink3)">Temes detectats:</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px">
          <span class="topic-chip">📅 Reunions (3)</span><span class="topic-chip">💬 Comunicació (2)</span><span class="topic-chip">🔧 Eines (2)</span><span class="topic-chip">📝 Feedback (1)</span>
        </div>`}
      </div>
    </div>
  </div>
  <div style="margin-top:8px;font-size:11px;color:var(--ink4);text-align:center">🔒 Todos los datos son anónimos y agregados. Ningún empleado puede ser identificado individualmente desde esta vista.</div>`;
}
"""

src = src[:start_i] + NEW_DASH + src[end_i:]

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 4 done. Lines:", src.count('\n'))
