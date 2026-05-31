with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ══════════════════════════════════════════════════
# 4. UPDATE attachCEOEvents analytics section for multi-employee
# ══════════════════════════════════════════════════
OLD_ANALYTICS_ATTACH = r"""      if(level==='trabajador'){
        const emp=employees.find(e=>e.id===selectedEmployee)||employees[0];
        const vals=emp.trend.map((_,i)=>metric==='wellbeing_index'?emp.trend[i]:metric==='horas_extra'?emp.metrics.horasExtra+(Math.random()*.4-.2):emp.metrics.productividad+(Math.random()*4-2)|0);
        return{labels:weeks,datasets:[{label:emp.name,data:vals.map(v=>+v.toFixed(1)),borderColor:emp.avatarColor,backgroundColor:emp.avatarColor+'18',tension:.4,fill:true,pointRadius:5}]};
      }"""

NEW_ANALYTICS_ATTACH = r"""      if(level==='trabajador'){
        const selEmps=analyticsSelectedEmps.map(id=>employees.find(e=>e.id===id)).filter(Boolean);
        if(!selEmps.length) selEmps.push(employees[0]);
        function empMetricVal(emp,m){
          if(m==='wellbeing_index') return null; // use trend
          if(m==='horas_extra') return emp.metrics.horasExtra;
          if(m==='reuniones') return emp.metrics.reuniones;
          if(m==='tareas') return emp.metrics.cargaTareas;
          if(m==='productividad') return emp.metrics.productividad;
          if(m==='respuesta_email') return emp.metrics.respEmail;
          if(m==='teletrabajo') return emp.metrics.teletrabajo;
          return 5;
        }
        const datasets=selEmps.map(emp=>{
          let vals;
          if(metric==='wellbeing_index'){
            vals=emp.trend;
          } else {
            const base=empMetricVal(emp,metric);
            // Generate realistic 8-week progression ending at current value
            const seed=emp.id.charCodeAt(1);
            vals=Array.from({length:8},(_,i)=>{
              const noise=(Math.sin(i*2.1+seed)*0.8+Math.cos(i*1.3+seed)*0.5);
              const progress=i/7; // 0→1 over weeks
              return Math.max(0,+(base*(0.85+0.15*progress)+noise).toFixed(1));
            });
          }
          return{
            label:emp.name,
            data:vals,
            borderColor:emp.avatarColor,
            backgroundColor:selEmps.length===1?emp.avatarColor+'18':'transparent',
            tension:.4,
            fill:selEmps.length===1,
            pointRadius:5,
            pointHoverRadius:8,
            borderWidth:2.5,
            pointBackgroundColor:metric==='wellbeing_index'?vals.map(v=>v>=70?'#059669':v>=40?'#D97706':'#DC2626'):emp.avatarColor
          };
        });
        return{labels:weeks,datasets};
      }"""

src = src.replace(OLD_ANALYTICS_ATTACH, NEW_ANALYTICS_ATTACH, 1)

# ══════════════════════════════════════════════════
# 5. ADD toggleCompareEmployee + AI functions BEFORE "// end of script"
# ══════════════════════════════════════════════════
AI_FUNCTIONS = r"""
// ═══════════════════════════════════════════════════
// COMPARE EMPLOYEE FUNCTIONS
// ═══════════════════════════════════════════════════
function toggleCompareEmployee(id){
  const idx=analyticsSelectedEmps.indexOf(id);
  if(idx>=0){
    analyticsSelectedEmps.splice(idx,1);
  } else {
    if(analyticsSelectedEmps.length>=6){
      analyticsSelectedEmps.shift(); // remove oldest
    }
    analyticsSelectedEmps.push(id);
  }
  renderCEOView('analitica');
}

// ═══════════════════════════════════════════════════
// AI ASSISTANT FUNCTIONS
// ═══════════════════════════════════════════════════
function openAIPanel(){
  aiPanelOpen=true;
  document.getElementById('ai-panel').classList.add('open');
  document.getElementById('ai-overlay').classList.add('visible');
  if(aiChat.length===0){
    aiChat.push({role:'ai',text:buildWelcomeMsg(),time:nowTime()});
    renderAIMessages();
  }
}
function closeAIPanel(){
  aiPanelOpen=false;
  document.getElementById('ai-panel').classList.remove('open');
  document.getElementById('ai-overlay').classList.remove('visible');
}
function nowTime(){
  const d=new Date();
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
}
function buildWelcomeMsg(){
  const s=getCompanyStats();
  return `<b>¡Hola! Soy el Asistente IA de BURNOFF.</b><br><br>
Tengo acceso a los datos de los <b>${s.n} empleados</b> de tu empresa.<br>
Índice empresa actual: <b style="color:${idxColor(s.avg)}">${s.avg}/100</b> · 
<b style="color:var(--terra)">${s.red} críticos</b> · 
<b style="color:var(--amber)">${s.amber} en atención</b><br><br>
Puedo ayudarte con:<br>
• Briefing detallado de cualquier empleado<br>
• Análisis de riesgo y burnout<br>
• Comparativas por departamento<br>
• Métricas específicas<br>
• Recomendaciones de acción<br><br>
¿Sobre qué quieres saber?`;
}

function sendAIMessage(){
  const input=document.getElementById('ai-input');
  const text=input.value.trim();
  if(!text) return;
  input.value='';
  aiChat.push({role:'user',text:text,time:nowTime()});
  renderAIMessages();
  // Show typing indicator then respond
  setTimeout(()=>{
    const response=generateAIResponse(text);
    aiChat.push({role:'ai',text:response,time:nowTime()});
    renderAIMessages();
  },600+Math.random()*400);
}

function handleAIQuickAction(text){
  document.getElementById('ai-input').value=text;
  sendAIMessage();
}

function aiInputKeydown(e){
  if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendAIMessage();}
}

function renderAIMessages(){
  const container=document.getElementById('ai-messages');
  if(!container) return;
  container.innerHTML=aiChat.map(m=>`
    <div class="ai-msg ${m.role}">
      <div class="ai-bubble">${m.text}</div>
      <div class="ai-msg-time">${m.time}</div>
    </div>`).join('');
  container.scrollTop=container.scrollHeight;
}

function getEmpVal(e,field){
  if(field==='index') return e.index;
  return e.metrics[field]||0;
}

function generateAIResponse(input){
  const q=input.toLowerCase().trim();
  const s=getCompanyStats();

  // ── Match employee by first or last name ──
  const matchedEmp=employees.find(e=>{
    const parts=e.name.toLowerCase().split(' ');
    return parts.some(p=>q.includes(p)&&p.length>3);
  });

  if(matchedEmp && (q.includes('briefing')||q.includes('resumen')||q.includes('perfil')||q.includes('datos')||q.includes('info')||q.length<40)){
    return generateEmpBriefing(matchedEmp);
  }

  // ── Top riesgo / críticos ──
  if(q.includes('riesgo')||q.includes('burnout')||q.includes('crítico')||q.includes('peor bienestar')||q.includes('alerta')){
    const top=employees.filter(e=>e.status==='red').sort((a,b)=>b.risk-a.risk);
    const ambs=employees.filter(e=>e.status==='amber').sort((a,b)=>b.risk-a.risk).slice(0,3);
    return `<b>🚨 Situación crítica — ${top.length} empleados en zona roja:</b><br><br>
${top.map((e,i)=>`<div style="margin:3px 0;padding:6px 10px;background:var(--terra-light);border-radius:6px;font-size:11px">
  <b>${i+1}. ${e.name}</b> · ${e.dept}<br>
  Índice: <b style="color:var(--terra)">${e.index}/100</b> · Riesgo: <b>${e.risk}%</b><br>
  <i style="font-size:10px">${e.signals[0]?.text||''}</i>
</div>`).join('')}
<br><b>⚠️ Top atención:</b><br>
${ambs.map(e=>`<div style="margin:3px 0;font-size:11px;padding:4px 8px;background:var(--amber-light);border-radius:6px"><b>${e.name}</b> — Riesgo ${e.risk}%</div>`).join('')}
<br>💡 <i>Tip: Escribe el nombre de un empleado para ver su briefing completo.</i>`;
  }

  // ── Mejor bienestar / top performers ──
  if(q.includes('mejor')||q.includes('más sano')||q.includes('bien')||q.includes('verde')){
    const top5=[...employees].sort((a,b)=>b.index-a.index).slice(0,5);
    return `<b>🌿 Top 5 empleados con mejor bienestar:</b><br><br>
${top5.map((e,i)=>`<div style="margin:3px 0;padding:6px 10px;background:var(--green-light);border-radius:6px;font-size:11px">
  <b>${i+1}. ${e.name}</b> · ${e.dept}<br>
  Índice: <b style="color:var(--green)">${e.index}/100</b> · Riesgo: ${e.risk}%
</div>`).join('')}
<br>📌 Referentes positivos a destacar como ejemplos de equilibrio saludable.`;
  }

  // ── Comparar departamentos ──
  if(q.includes('comparar')||q.includes('departamento')||q.includes('equipo')||q.includes('dept')){
    const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];
    const stats=depts.map(d=>{
      const emps=getEmpsByDept(d);
      const avg=Math.round(emps.reduce((s,e)=>s+e.index,0)/emps.length);
      const avgRisk=Math.round(emps.reduce((s,e)=>s+e.risk,0)/emps.length);
      const red=emps.filter(e=>e.status==='red').length;
      return{name:d,avg,avgRisk,red,count:emps.length};
    }).sort((a,b)=>a.avg-b.avg);
    return `<b>📊 Comparativa por departamento:</b><br><br>
${stats.map((d,i)=>`<div style="margin:4px 0;padding:8px 10px;background:var(--bg);border-radius:8px;border:1px solid var(--border-md);font-size:11px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <b>${i===0?'🚨':i===1?'⚠️':'🌿'} ${d.name}</b>
    <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:${idxColor(d.avg)}">${d.avg}/100</span>
  </div>
  <div style="color:var(--ink3);margin-top:3px">${d.count} pers. · Riesgo medio: ${d.avgRisk}%${d.red?' · <b style="color:var(--terra)">${d.red} críticos</b>':''}</div>
  <div style="height:3px;background:var(--border-md);border-radius:100px;margin-top:5px"><div style="height:100%;width:${d.avg}%;background:${idxColor(d.avg)};border-radius:100px"></div></div>
</div>`).join('')}
<br><b>Conclusión IA:</b> La brecha entre el mejor (Marketing ${stats[4].avg}/100) y el peor (Operaciones ${stats[0].avg}/100) es de <b>${stats[4].avg-stats[0].avg} puntos</b>. Se recomienda intervención urgente en ${stats[0].name}.`;
  }

  // ── Media empresa / índice global ──
  if(q.includes('media')||q.includes('índice')||q.includes('empresa')||q.includes('global')||q.includes('resumen empresa')||q.includes('overview')){
    const dists=[...employees].reduce((acc,e)=>{acc[e.status]=(acc[e.status]||0)+1;return acc;},{});
    const avgHExtra=+(employees.reduce((s,e)=>s+e.metrics.horasExtra,0)/employees.length).toFixed(1);
    const avgMeet=+(employees.reduce((s,e)=>s+e.metrics.reuniones,0)/employees.length).toFixed(1);
    const avgLoad=Math.round(employees.reduce((s,e)=>s+e.metrics.cargaTareas,0)/employees.length);
    return `<b>🏢 Resumen Global de Empresa — ${employees.length} empleados</b><br><br>
<div style="padding:10px;background:var(--bg);border-radius:8px;border:1px solid var(--border-md);margin-bottom:8px">
  <div style="font-size:22px;font-weight:700;color:${idxColor(s.avg)};text-align:center;line-height:1">${s.avg}<span style="font-size:14px">/100</span></div>
  <div style="text-align:center;font-size:10px;color:var(--ink3)">Índice Bienestar Empresa</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:8px">
  <div style="text-align:center;padding:8px;background:var(--green-light);border-radius:6px"><div style="font-weight:700;color:var(--green)">${s.green}</div><div style="font-size:10px;color:var(--ink3)">🌿 Bienestar</div></div>
  <div style="text-align:center;padding:8px;background:var(--amber-light);border-radius:6px"><div style="font-weight:700;color:var(--amber)">${s.amber}</div><div style="font-size:10px;color:var(--ink3)">⚠️ Atención</div></div>
  <div style="text-align:center;padding:8px;background:var(--terra-light);border-radius:6px"><div style="font-weight:700;color:var(--terra)">${s.red}</div><div style="font-size:10px;color:var(--ink3)">🚨 Crítico</div></div>
</div>
Horas extra/día media: <b>${avgHExtra}h</b> · Reuniones/día: <b>${avgMeet}</b> · Carga media: <b>${avgLoad}%</b><br><br>
💡 <b>BURNOFF-AI recomienda:</b> Acción inmediata en Operaciones (${getEmpsByDept('Operaciones').filter(e=>e.status==='red').length} críticos). Potencial ahorro en bajas: <b>€180.000/año</b> estimado.`;
  }

  // ── Horas extra ──
  if(q.includes('horas extra')||q.includes('overtime')||q.includes('extensión')){
    const sorted=[...employees].sort((a,b)=>b.metrics.horasExtra-a.metrics.horasExtra).slice(0,5);
    return `<b>🕐 Top 5 empleados con más horas extra:</b><br><br>
${sorted.map((e,i)=>`<div style="margin:3px 0;padding:6px 10px;background:${e.metrics.horasExtra>3?'var(--terra-light)':'var(--amber-light)'};border-radius:6px;font-size:11px">
  <b>${e.name}</b> · ${e.dept}<br>
  <span style="color:${e.metrics.horasExtra>3?'var(--terra)':'var(--amber)'}"><b>+${e.metrics.horasExtra}h/día</b></span> · Carga: ${e.metrics.cargaTareas}%
</div>`).join('')}
<br>Media empresa: <b>${+(employees.reduce((s,e)=>s+e.metrics.horasExtra,0)/employees.length).toFixed(1)}h/día</b>`;
  }

  // ── Reuniones ──
  if(q.includes('reuniones')||q.includes('meetings')||q.includes('meeting fatigue')){
    const sorted=[...employees].sort((a,b)=>b.metrics.reuniones-a.metrics.reuniones).slice(0,5);
    return `<b>📅 Top 5 con más reuniones/día:</b><br><br>
${sorted.map((e,i)=>`<div style="margin:3px 0;padding:6px 10px;background:${e.metrics.reuniones>7?'var(--terra-light)':'var(--amber-light)'};border-radius:6px;font-size:11px">
  <b>${e.name}</b> · ${e.dept}<br>
  <b>${e.metrics.reuniones} reuniones/día</b> · Productividad: ${e.metrics.productividad}%
</div>`).join('')}
<br>⚠️ Más de 6 reuniones/día = fragmentación cognitiva severa. Considera bloqueos de Deep Work.`;
  }

  // ── Productividad ──
  if(q.includes('productividad')||q.includes('rendimiento')||q.includes('performance')){
    const sorted=[...employees].sort((a,b)=>b.metrics.productividad-a.metrics.productividad);
    const top3=sorted.slice(0,3);
    const bot3=sorted.slice(-3);
    return `<b>📈 Análisis de Productividad</b><br><br>
<b style="color:var(--green)">Top 3 más productivos:</b><br>
${top3.map(e=>`<div style="margin:2px 0;font-size:11px;padding:5px 8px;background:var(--green-light);border-radius:5px"><b>${e.name}</b> — ${e.metrics.productividad}% · ${e.dept}</div>`).join('')}
<br><b style="color:var(--terra)">3 con menor productividad:</b><br>
${bot3.map(e=>`<div style="margin:2px 0;font-size:11px;padding:5px 8px;background:var(--terra-light);border-radius:5px"><b>${e.name}</b> — ${e.metrics.productividad}% · Riesgo burnout: ${e.risk}%</div>`).join('')}
<br>💡 Correlación detectada: productividad baja + riesgo alto = candidatos prioritarios para intervención.`;
  }

  // ── Briefing genérico sin nombre ──
  if(q.includes('briefing')){
    return `Para generar un briefing, indícame el nombre del empleado. Ejemplo:<br><br>
<i>"Briefing de Pablo Moreno"</i><br><i>"Resumen de Elena Vidal"</i><br><i>"Datos de Carla Jiménez"</i><br><br>
Empleados con mayor riesgo: <b>${employees.filter(e=>e.risk>=70).map(e=>e.name.split(' ')[0]).join(', ')}</b>`;
  }

  // ── Teletrabajo ──
  if(q.includes('teletrabajo')||q.includes('remoto')||q.includes('presencial')){
    const avgTele=+(employees.reduce((s,e)=>s+e.metrics.teletrabajo,0)/employees.length).toFixed(1);
    const noTele=employees.filter(e=>e.metrics.teletrabajo===0);
    return `<b>🏠 Análisis de Teletrabajo</b><br><br>
Media empresa: <b>${avgTele} días/semana</b><br><br>
${noTele.length?`<b style="color:var(--terra)">Sin ningún día remoto (${noTele.length} personas):</b><br>${noTele.map(e=>`<div style="font-size:11px;padding:4px 8px;background:var(--terra-light);border-radius:5px;margin:2px 0"><b>${e.name}</b> · ${e.dept} · Índice: ${e.index}/100</div>`).join('')}<br>`:''}
💡 Empleados sin teletrabajo en zona crítica muestran índice medio ${Math.round(noTele.reduce((s,e)=>s+e.index,0)/(noTele.length||1))}/100 vs ${Math.round(employees.filter(e=>e.metrics.teletrabajo>=3).reduce((s,e)=>s+e.index,0)/(employees.filter(e=>e.metrics.teletrabajo>=3).length||1))}/100 en empleados con ≥3 días remotos.`;
  }

  // ── Predicción / forecast ──
  if(q.includes('predicción')||q.includes('baja')||q.includes('forecast')||q.includes('prevision')){
    const highRisk=employees.filter(e=>e.risk>=70);
    return `<b>🔮 Predicción BURNOFF-AI — Próximas 8 semanas</b><br><br>
<div style="padding:10px;background:var(--terra-light);border-radius:8px;margin-bottom:8px">
  <b style="color:var(--terra)">Riesgo de baja laboral ALTO:</b><br>
  ${highRisk.map(e=>`<div style="font-size:11px;margin:3px 0">• <b>${e.name}</b> (${e.dept}) — ${e.risk}% probabilidad en 4 semanas</div>`).join('')}
</div>
<div style="padding:10px;background:var(--amber-light);border-radius:8px;margin-bottom:8px">
  <b style="color:var(--amber)">Coste estimado por baja:</b><br>
  <div style="font-size:12px;margin-top:4px">• Baja técnica (1 mes): <b>€3.500–8.000</b> por persona<br>• Rotación + sustitución: <b>€15.000–25.000</b> por persona<br>• Con ${highRisk.length} empleados críticos: riesgo total <b>€${(highRisk.length*18000).toLocaleString()}</b></div>
</div>
💡 Con intervención BURNOFF-AI ahora, reducción estimada del 73% del riesgo.`;
  }

  // ── Default fallback ──
  return `No he encontrado una respuesta específica para "<b>${input.slice(0,50)}</b>".<br><br>
Intenta preguntarme sobre:<br>
• Nombre de empleado: <i>"Briefing de Ana García"</i><br>
• Riesgos: <i>"¿Quién tiene mayor riesgo de burnout?"</i><br>
• Departamentos: <i>"Compara todos los departamentos"</i><br>
• Métricas: <i>"¿Cuál es el índice medio de la empresa?"</i><br>
• Predicciones: <i>"Predicción de bajas próximas semanas"</i>`;
}

function generateEmpBriefing(e){
  const trendDir=e.trend[7]>e.trend[0]?'↑ Mejorando':e.trend[7]<e.trend[0]-3?'↓ Decreciendo':'→ Estable';
  const riskColor=e.risk>=70?'var(--terra)':e.risk>=40?'var(--amber)':'var(--green)';
  return `<b>📋 BRIEFING · ${e.name}</b>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin:6px 0">
  <span class="status-badge ${statusBadgeClass(e.status)}" style="font-size:10px">${statusLabel(e.status)}</span>
  <span class="risk-pill ${riskClass(e.risk)}" style="font-size:10px">Riesgo ${riskLabel(e.risk)}: ${e.risk}%</span>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:8px 0">
  <div style="padding:8px;background:rgba(0,0,0,.04);border-radius:6px;text-align:center">
    <div style="font-size:20px;font-weight:700;color:${idxColor(e.index)}">${e.index}</div>
    <div style="font-size:9px;color:var(--ink3)">Índice bienestar</div>
  </div>
  <div style="padding:8px;background:rgba(0,0,0,.04);border-radius:6px;text-align:center">
    <div style="font-size:20px;font-weight:700;color:${riskColor}">${e.risk}%</div>
    <div style="font-size:9px;color:var(--ink3)">Riesgo burnout</div>
  </div>
</div>
<div style="font-size:11px;margin-bottom:8px"><b>${e.role}</b> · ${e.dept} · ${e.age} años<br>
Tendencia: <b>${trendDir}</b> (${e.trend[0]} → ${e.trend[7]})</div>
<b>📊 Métricas:</b>
<div style="background:rgba(0,0,0,.04);border-radius:6px;padding:8px;margin:5px 0">
${[['Horas extra/día',e.metrics.horasExtra+'h',e.metrics.horasExtra>3?'terra':e.metrics.horasExtra>1?'amber':'green'],
   ['Reuniones/día',e.metrics.reuniones,e.metrics.reuniones>6?'terra':e.metrics.reuniones>4?'amber':'green'],
   ['Carga trabajo',e.metrics.cargaTareas+'%',e.metrics.cargaTareas>130?'terra':e.metrics.cargaTareas>100?'amber':'green'],
   ['Productividad',e.metrics.productividad+'%',e.metrics.productividad<40?'terra':e.metrics.productividad<65?'amber':'green'],
   ['Teletrabajo',e.metrics.teletrabajo+' días/sem','green']
].map(([k,v,c])=>`<div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(0,0,0,.05);font-size:10px">
  <span style="color:var(--ink3)">${k}</span>
  <span style="font-weight:600;color:var(--${c})">${v}</span>
</div>`).join('')}
</div>
<b>🔍 Señales:</b><br>
${e.signals.map(s=>`<div style="font-size:10px;padding:4px 0;color:var(--ink2)">• ${s.icon} ${s.text}</div>`).join('')}
<br><div style="padding:8px;background:${e.risk>=70?'var(--terra-light)':e.risk>=40?'var(--amber-light)':'var(--green-light)'};border-radius:6px;font-size:11px">
<b>🤖 Recomendación:</b> ${e.risk>=70?`Intervención urgente. Riesgo de baja en 4–6 semanas. Conversación RRHH + reducción carga inmediata.`:e.risk>=40?`Seguimiento activo. Check-in 1:1 con manager y revisión reuniones en 2 semanas.`:`Indicadores positivos. Mantener condiciones y continuar seguimiento mensual.`}
</div>`;
}
"""

ANCHOR = '\n\n// end of script\n</script>'
src = src.replace(ANCHOR, AI_FUNCTIONS + '\n\n// end of script\n</script>', 1)

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part B done. Lines:", src.count('\n'))
