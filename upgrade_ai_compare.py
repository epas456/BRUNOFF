with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ══════════════════════════════════════════════════
# 1. STATE VARIABLES
# ══════════════════════════════════════════════════
OLD_STATE = "let analyticsMetric = 'wellbeing_index';\nlet analyticsLevel = 'company';"
NEW_STATE = """let analyticsMetric = 'wellbeing_index';
let analyticsLevel = 'company';
let analyticsSelectedEmps = ['e02','e05','e12']; // default: Pablo(red), Carla(red), Elena V(red) — impactful demo
let aiChat = [];
let aiPanelOpen = false;"""
src = src.replace(OLD_STATE, NEW_STATE, 1)

# ══════════════════════════════════════════════════
# 2. CSS ADDITIONS
# ══════════════════════════════════════════════════
AI_CSS = """
/* ── AI PANEL ── */
.ai-panel{position:fixed;right:0;top:0;bottom:0;width:400px;background:#fff;box-shadow:-6px 0 32px rgba(15,20,25,0.14);z-index:600;display:flex;flex-direction:column;transform:translateX(100%);transition:transform 320ms cubic-bezier(.4,0,.2,1)}
.ai-panel.open{transform:translateX(0)}
.ai-panel-header{padding:16px 20px;border-bottom:1px solid var(--border-md);display:flex;align-items:center;gap:10px;flex-shrink:0;background:linear-gradient(135deg,#0F172A,#1E3A5F)}
.ai-panel-title{font-size:14px;font-weight:600;color:#fff;flex:1}
.ai-panel-sub{font-size:10px;color:rgba(255,255,255,.6);font-family:'JetBrains Mono',monospace;letter-spacing:.04em}
.ai-close-btn{width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.1);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px;flex-shrink:0;transition:background 120ms}
.ai-close-btn:hover{background:rgba(255,255,255,.2)}
.ai-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
.ai-msg{display:flex;flex-direction:column;gap:4px;max-width:92%}
.ai-msg.user{align-self:flex-end;align-items:flex-end}
.ai-msg.ai{align-self:flex-start}
.ai-bubble{padding:10px 14px;border-radius:14px;font-size:12px;line-height:1.6}
.ai-msg.user .ai-bubble{background:var(--cobalt);color:#fff;border-bottom-right-radius:4px}
.ai-msg.ai .ai-bubble{background:var(--bg);border:1px solid var(--border-md);color:var(--ink2);border-bottom-left-radius:4px}
.ai-msg-time{font-size:10px;color:var(--ink4);font-family:'JetBrains Mono',monospace}
.ai-typing{display:flex;gap:4px;align-items:center;padding:10px 14px;background:var(--bg);border:1px solid var(--border-md);border-radius:14px;border-bottom-left-radius:4px;width:fit-content}
.ai-typing span{width:6px;height:6px;border-radius:50%;background:var(--ink3);animation:typing .9s infinite}
.ai-typing span:nth-child(2){animation-delay:.2s}
.ai-typing span:nth-child(3){animation-delay:.4s}
@keyframes typing{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
.ai-quick-chips{padding:12px 16px;border-top:1px solid var(--border);display:flex;flex-wrap:wrap;gap:6px;background:var(--bg);flex-shrink:0}
.ai-quick-chip{font-size:11px;padding:5px 10px;border-radius:100px;background:var(--surface);border:1px solid var(--border-md);color:var(--ink2);cursor:pointer;transition:all 120ms;white-space:nowrap}
.ai-quick-chip:hover{background:var(--cobalt-light);border-color:var(--cobalt-mid);color:var(--cobalt)}
.ai-input-row{padding:12px 16px;border-top:1px solid var(--border-md);display:flex;gap:8px;flex-shrink:0}
.ai-input{flex:1;padding:9px 12px;border:1px solid var(--border-md);border-radius:20px;font-size:13px;font-family:'Inter',sans-serif;outline:none;transition:border-color 150ms;background:#fff}
.ai-input:focus{border-color:var(--cobalt)}
.ai-send-btn{width:36px;height:36px;border-radius:50%;background:var(--cobalt);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;transition:background 120ms;font-size:14px}
.ai-send-btn:hover{background:var(--cobalt-mid)}
.ai-overlay{position:fixed;inset:0;background:rgba(15,20,25,0.3);z-index:599;display:none}
.ai-overlay.visible{display:block}
/* AI trigger button */
.ai-fab{position:fixed;bottom:24px;right:24px;z-index:500;background:linear-gradient(135deg,#1E3A5F,#2563EB);color:#fff;border-radius:100px;padding:12px 20px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px;box-shadow:0 4px 20px rgba(30,58,95,0.35);cursor:pointer;transition:transform 160ms,box-shadow 160ms;border:none}
.ai-fab:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(30,58,95,0.42)}
.ai-fab .ai-fab-dot{width:8px;height:8px;border-radius:50%;background:#34d399;animation:pulse-green 2s infinite}
@keyframes pulse-green{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.7;transform:scale(1.3)}}
/* ── COMPARE EMPLOYEE SELECTOR ── */
.emp-compare-grid{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.emp-compare-chip{display:flex;align-items:center;gap:7px;padding:6px 12px 6px 6px;border-radius:100px;border:2px solid var(--border-md);background:#fff;cursor:pointer;transition:all 130ms;user-select:none}
.emp-compare-chip:hover{border-color:var(--cobalt-mid);background:var(--cobalt-light)}
.emp-compare-chip.selected{border-color:var(--cobalt);background:var(--cobalt-light)}
.emp-compare-chip.selected-red{border-color:var(--terra);background:var(--terra-light)}
.emp-compare-chip.selected-amber{border-color:var(--amber);background:var(--amber-light)}
.emp-compare-chip.selected-green{border-color:var(--green);background:var(--green-light)}
.emp-chip-av{width:22px;height:22px;border-radius:50%;color:#fff;font-size:9px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.emp-chip-name{font-size:11px;font-weight:500;color:var(--ink)}
.emp-chip-check{width:14px;height:14px;border-radius:50%;border:1.5px solid var(--border-md);display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-left:2px;font-size:9px}
.emp-compare-chip.selected .emp-chip-check,.emp-compare-chip.selected-red .emp-chip-check,.emp-compare-chip.selected-amber .emp-chip-check,.emp-compare-chip.selected-green .emp-chip-check{border-color:currentColor;background:currentColor;color:#fff}
.dept-label-sm{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3);margin-top:10px;margin-bottom:4px}
/* AI bubble formatted content */
.ai-briefing-section{margin:6px 0;padding:8px 10px;background:rgba(255,255,255,.6);border-radius:8px;border:1px solid rgba(0,0,0,.06)}
.ai-briefing-title{font-weight:700;font-size:12px;color:var(--ink);margin-bottom:6px}
.ai-briefing-row{display:flex;justify-content:space-between;font-size:11px;padding:2px 0;border-bottom:1px solid rgba(0,0,0,.04)}
.ai-briefing-row:last-child{border-bottom:none}
.ai-briefing-key{color:var(--ink3)}
.ai-briefing-val{font-weight:600;font-family:'JetBrains Mono',monospace}
"""
src = src.replace('</style>', AI_CSS + '\n</style>', 1)

# ══════════════════════════════════════════════════
# 3. REPLACE ceoViewAnalitica with compare + AI button
# ══════════════════════════════════════════════════
OLD_ANAL_FN_START = 'function ceoViewAnalitica(){'
OLD_ANAL_FN_END   = '\n\n// end of script'

start_i = src.index(OLD_ANAL_FN_START)
end_i   = src.index(OLD_ANAL_FN_END, start_i)

NEW_ANAL_FN = r"""function ceoViewAnalitica(){
  const metrics=[
    {id:'wellbeing_index',label:'Índice de Bienestar',unit:'/100'},
    {id:'reuniones',label:'Reuniones por día',unit:''},
    {id:'tareas',label:'Carga de Tareas',unit:'%'},
    {id:'productividad',label:'Productividad',unit:'%'},
    {id:'horas_extra',label:'Horas Extra por día',unit:'h'},
    {id:'respuesta_email',label:'Variación Resp. Email',unit:'%'},
    {id:'teletrabajo',label:'Días Teletrabajo/sem',unit:''},
    {id:'absentismo',label:'Absentismo',unit:'%'}
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
  const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];

  // ── Employee selector (when level = trabajador) ──
  let empSelectorHtml='';
  if(analyticsLevel==='trabajador'){
    const selSet=new Set(analyticsSelectedEmps);
    const selCount=selSet.size;
    const deptChips=depts.map(dept=>{
      const emps=getEmpsByDept(dept);
      if(!emps.length) return '';
      const chips=emps.map(e=>{
        const isSel=selSet.has(e.id);
        const selClass=isSel?(e.status==='red'?'selected-red':e.status==='amber'?'selected-amber':'selected-green'):'';
        return `<div class="emp-compare-chip ${selClass}" onclick="toggleCompareEmployee('${e.id}')">
          <div class="emp-chip-av" style="background:${e.avatarColor}">${e.avatar}</div>
          <div>
            <div class="emp-chip-name">${e.name}</div>
            <div style="font-size:9px;color:var(--ink3)">${e.index}/100</div>
          </div>
          <div class="emp-chip-check">${isSel?'✓':''}</div>
        </div>`;
      }).join('');
      return `<div class="dept-label-sm">${dept}</div><div class="emp-compare-grid">${chips}</div>`;
    }).join('');

    empSelectorHtml=`
    <div style="padding:14px 16px;background:var(--bg);border-radius:var(--r);border:1px solid var(--border-md);margin-bottom:16px">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
        <div style="font-size:11px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em">
          Seleccionar empleados para comparar <span style="color:var(--cobalt-mid)">(${selCount} seleccionados · máx. 6)</span>
        </div>
        <div style="display:flex;gap:6px">
          <button class="btn-sm btn-ghost" style="font-size:10px" onclick="analyticsSelectedEmps=employees.filter(e=>e.status==='red').map(e=>e.id).slice(0,6);renderCEOView('analitica')">🚨 Solo críticos</button>
          <button class="btn-sm btn-ghost" style="font-size:10px" onclick="analyticsSelectedEmps=employees.map(e=>e.id).slice(0,6);renderCEOView('analitica')">Seleccionar 6</button>
          <button class="btn-sm btn-ghost" style="font-size:10px" onclick="analyticsSelectedEmps=[];renderCEOView('analitica')">Limpiar</button>
        </div>
      </div>
      ${deptChips}
    </div>`;
  }

  // ── Ranking table (trabajador view) ──
  let rankRows='';
  if(analyticsLevel==='trabajador'){
    const f={wellbeing_index:'index',reuniones:'reuniones',tareas:'cargaTareas',productividad:'productividad',horas_extra:'horasExtra',respuesta_email:'respEmail',teletrabajo:'teletrabajo'}[analyticsMetric]||'index';
    const sorted=[...employees].sort((a,b)=>{const va=f==='index'?a.index:(a.metrics[f]||0);const vb=f==='index'?b.index:(b.metrics[f]||0);return vb-va;});
    const selSet=new Set(analyticsSelectedEmps);
    rankRows=sorted.slice(0,10).map((e,i)=>{
      const val=f==='index'?e.index:(e.metrics[f]||0);
      const isSel=selSet.has(e.id);
      return `<tr onclick="openEmployee('${e.id}')" style="${isSel?'background:var(--cobalt-light)':''}">
        <td style="font-family:'JetBrains Mono',monospace;color:var(--ink3);font-size:11px">#${i+1}</td>
        <td><div class="emp-name-wrap">
          <div class="emp-av" style="background:${e.avatarColor};width:24px;height:24px;font-size:9px;box-shadow:${isSel?'0 0 0 2px #1E3A5F':''}">${e.avatar}</div>
          <span class="emp-name" style="color:${isSel?'var(--cobalt)':''}">${e.name}${isSel?' ◉':''}</span>
        </div></td>
        <td><span style="font-size:11px;color:var(--ink3)">${e.dept}</span></td>
        <td><span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:${idxColor(e.index)}">${val}</span></td>
        <td><span class="status-badge ${statusBadgeClass(e.status)}">${statusLabel(e.status)}</span></td>
        <td><span style="font-size:11px;color:var(--cobalt-mid)">Ver →</span></td>
      </tr>`;
    }).join('');
  }

  return `
  <div class="page-header" style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px">
    <div>
      <div class="page-title">Analítica Avanzada</div>
      <div class="page-subtitle">Métricas por empresa, departamento o trabajador · Comparativa multiempleado</div>
    </div>
    <button class="btn-sm btn-cobalt" style="display:flex;align-items:center;gap:6px;padding:8px 16px" onclick="openAIPanel()">
      <span style="font-size:15px">🤖</span> Asistente IA
    </button>
  </div>

  ${empSelectorHtml}

  <div class="chart-card" style="margin-bottom:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:16px">
      <div><div style="font-size:11px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Métrica</div>${metricSel}</div>
      <div><div style="font-size:11px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Nivel de análisis</div>${levelSeg}</div>
    </div>
    <div class="chart-card-title" style="margin-bottom:4px">${curMetric.label} · ${curLevel.label}
      ${analyticsLevel==='trabajador'&&analyticsSelectedEmps.length?`<span style="font-size:11px;color:var(--ink3);font-weight:400"> · ${analyticsSelectedEmps.length} empleado${analyticsSelectedEmps.length>1?'s':''}</span>`:''}
    </div>
    <div style="position:relative;height:300px"><canvas id="chart-analytics"></canvas></div>
  </div>

  ${analyticsLevel==='trabajador'?`
  <div class="table-card">
    <div class="table-header">Ranking — ${curMetric.label} <span style="font-weight:400;font-size:11px;color:var(--ink3)">(◉ = en comparativa)</span></div>
    <table class="emp-table">
      <thead><tr><th>#</th><th>Empleado</th><th>Dpto</th><th>Valor</th><th>Estado</th><th></th></tr></thead>
      <tbody>${rankRows}</tbody>
    </table>
  </div>`:''}`;
}
"""

src = src[:start_i] + NEW_ANAL_FN + src[end_i:]

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part A done. Lines:", src.count('\n'))
