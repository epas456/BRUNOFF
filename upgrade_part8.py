with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# Replace from ceoViewAnalitica start through renderAnalyticsChart end
OLD_ANAL_START = 'function ceoViewAnalitica() {'
OLD_ANAL_END   = '\n\n\n// end of script\n</script>'

start_i = src.index(OLD_ANAL_START)
end_i   = src.index(OLD_ANAL_END, start_i)

NEW_ANAL = r"""function ceoViewAnalitica(){
  const metrics=[
    {id:'wellbeing_index',label:'Índice de Bienestar'},
    {id:'reuniones',label:'Reuniones por día'},
    {id:'tareas',label:'Carga de Tareas (%)'},
    {id:'productividad',label:'Productividad (%)'},
    {id:'horas_extra',label:'Horas Extra por día'},
    {id:'respuesta_email',label:'Variación Resp. Email (%)'},
    {id:'teletrabajo',label:'Días Teletrabajo / semana'},
    {id:'absentismo',label:'Absentismo (%)'}
  ];
  const levels=[
    {id:'company',label:'🏢 Empresa'},
    {id:'departamento',label:'🏬 Departamento'},
    {id:'trabajador',label:'👤 Trabajador'}
  ];
  const metricSel=`<select class="form-input" style="max-width:300px;cursor:pointer" onchange="analyticsMetric=this.value;renderCEOView('analitica')">
    ${metrics.map(m=>`<option value="${m.id}" ${analyticsMetric===m.id?'selected':''}>${m.label}</option>`).join('')}
  </select>`;
  const levelSeg=`<div style="display:flex;gap:4px">
    ${levels.map(l=>`<button class="btn-sm ${analyticsLevel===l.id?'btn-cobalt':'btn-outline'}" onclick="analyticsLevel='${l.id}';renderCEOView('analitica')">${l.label}</button>`).join('')}
  </div>`;
  const curMetric=metrics.find(m=>m.id===analyticsMetric)||metrics[0];
  const curLevel=levels.find(l=>l.id===analyticsLevel)||levels[0];

  const field={wellbeing_index:'index',reuniones:'reuniones',tareas:'cargaTareas',productividad:'productividad',horas_extra:'horasExtra',respuesta_email:'respEmail',teletrabajo:'teletrabajo',absentismo:'absentismo'};
  const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];

  let rankRows='';
  if(analyticsLevel==='trabajador'){
    const f=field[analyticsMetric]||'index';
    const sorted=[...employees].sort((a,b)=>{
      const va=f==='index'?a.index:(a.metrics[f]||0);
      const vb=f==='index'?b.index:(b.metrics[f]||0);
      return vb-va;
    });
    rankRows=sorted.slice(0,10).map((e,i)=>{
      const val=f==='index'?e.index:(e.metrics[f]||0);
      return `<tr onclick="openEmployee('${e.id}')">
        <td style="font-family:'JetBrains Mono',monospace;color:var(--ink3);font-size:11px">#${i+1}</td>
        <td><div class="emp-name-wrap"><div class="emp-av" style="background:${e.avatarColor};width:24px;height:24px;font-size:9px">${e.avatar}</div><span class="emp-name">${e.name}</span></div></td>
        <td><span style="font-size:11px;color:var(--ink3)">${e.dept}</span></td>
        <td><span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:${idxColor(e.index)}">${val}</span></td>
        <td><span class="status-badge ${statusBadgeClass(e.status)}">${statusLabel(e.status)}</span></td>
        <td><span style="font-size:11px;color:var(--cobalt-mid)">Ver →</span></td>
      </tr>`;
    }).join('');
  }

  return `
  <div class="page-header">
    <div class="page-title">Analítica Avanzada</div>
    <div class="page-subtitle">Métricas de bienestar por empresa, departamento o trabajador</div>
  </div>
  <div class="chart-card" style="margin-bottom:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:16px">
      <div><div style="font-size:11px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Métrica</div>${metricSel}</div>
      <div><div style="font-size:11px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Nivel de análisis</div>${levelSeg}</div>
    </div>
    <div class="chart-card-title" style="margin-bottom:12px">${curMetric.label} · ${curLevel.label}</div>
    <div style="position:relative;height:280px"><canvas id="chart-analytics"></canvas></div>
  </div>
  ${analyticsLevel==='trabajador'?`
  <div class="table-card">
    <div class="table-header">Ranking Empleados — ${curMetric.label}</div>
    <table class="emp-table">
      <thead><tr><th>#</th><th>Empleado</th><th>Dpto</th><th>Valor</th><th>Estado</th><th></th></tr></thead>
      <tbody>${rankRows}</tbody>
    </table>
  </div>`:''}`;
}

"""

src = src[:start_i] + NEW_ANAL + '\n\n// end of script\n</script>' + src[end_i + len('\n\n\n// end of script\n</script>'):]

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 8 done. Lines:", src.count('\n'))
