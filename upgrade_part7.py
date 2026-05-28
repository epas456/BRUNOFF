with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 10. Replace attachCEOEvents with Chart.js initialization ──
OLD_ATTACH = """function attachCEOEvents(viewId) {
  // view-specific post-render hooks (reserved)
}"""

NEW_ATTACH = r"""function attachCEOEvents(viewId){
  const CHART_FONT={family:'Inter',size:11};
  const TOOLTIP={backgroundColor:'#0F172A',titleFont:{family:'Inter',size:11},bodyFont:{family:'Inter',size:12},padding:10,cornerRadius:6,displayColors:true};
  const SCALE_X={grid:{display:false},ticks:{font:CHART_FONT,color:'#7A8394'}};
  const SCALE_Y={grid:{color:'rgba(15,20,25,0.05)'},ticks:{font:CHART_FONT,color:'#7A8394'},border:{dash:[4,4]}};

  if(viewId==='dashboard'){
    const s=getCompanyStats();
    const weeks=['S13','S14','S15','S16','S17','S18','S19','S20'];
    const companyTrend=Array.from({length:8},(_,i)=>Math.round(employees.reduce((sum,e)=>sum+e.trend[i],0)/employees.length));
    const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];
    const deptAvg=depts.map(d=>{const emps=getEmpsByDept(d);return Math.round(emps.reduce((s,e)=>s+e.index,0)/emps.length);});
    const deptColors=['#2563EB','#059669','#DC2626','#7c3aed','#D97706'];

    const tCtx=document.getElementById('chart-trend');
    if(tCtx) charts.trend=new Chart(tCtx,{type:'line',data:{labels:weeks,datasets:[{label:'Índice Bienestar',data:companyTrend,borderColor:'#1E3A5F',backgroundColor:'rgba(30,58,95,0.07)',tension:.4,fill:true,pointBackgroundColor:companyTrend.map(v=>v>=70?'#059669':v>=40?'#D97706':'#DC2626'),pointRadius:5,pointHoverRadius:7}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,min:30,max:100,ticks:{...SCALE_Y.ticks,callback:v=>v+'/100'}}}}});

    const dCtx=document.getElementById('chart-dept');
    if(dCtx) charts.dept=new Chart(dCtx,{type:'bar',data:{labels:depts.map(d=>d.length>12?d.slice(0,12)+'…':d),datasets:[{label:'Índice',data:deptAvg,backgroundColor:deptColors.map(c=>c+'CC'),borderColor:deptColors,borderWidth:1.5,borderRadius:6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,min:0,max:100,ticks:{...SCALE_Y.ticks,callback:v=>v+'/100'}}},indexAxis:'y'}});

    const doCtx=document.getElementById('chart-donut');
    if(doCtx) charts.donut=new Chart(doCtx,{type:'doughnut',data:{labels:['🌿 Bienestar','⚠️ Atención','🚨 Crítico'],datasets:[{data:[s.green,s.amber,s.red],backgroundColor:['#059669','#D97706','#DC2626'],borderWidth:3,borderColor:'#ffffff',hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{display:false},tooltip:TOOLTIP}}});
  }

  if(viewId==='equipos'){
    const t=teams[selectedTeam];
    const weeks=['S13','S14','S15','S16','S17','S18','S19','S20'];
    const ttCtx=document.getElementById('chart-team-trend');
    if(ttCtx) charts.teamTrend=new Chart(ttCtx,{type:'line',data:{labels:weeks,datasets:[{label:t.name,data:t.trend,borderColor:'#1E3A5F',backgroundColor:'rgba(30,58,95,0.07)',tension:.4,fill:true,pointBackgroundColor:t.trend.map(v=>v>=70?'#059669':v>=40?'#D97706':'#DC2626'),pointRadius:5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,min:30,max:100,ticks:{...SCALE_Y.ticks,callback:v=>v+'/100'}}}}});
  }

  if(viewId==='empleado'){
    const e=employees.find(x=>x.id===selectedEmployee);
    if(!e) return;
    const weeks=['S13','S14','S15','S16','S17','S18','S19','S20'];
    const etCtx=document.getElementById('chart-emp-trend');
    if(etCtx) charts.empTrend=new Chart(etCtx,{type:'line',data:{labels:weeks,datasets:[{label:'Índice Bienestar',data:e.trend,borderColor:e.avatarColor,backgroundColor:e.avatarColor+'18',tension:.4,fill:true,pointBackgroundColor:e.trend.map(v=>v>=70?'#059669':v>=40?'#D97706':'#DC2626'),pointRadius:6,pointHoverRadius:8},{label:'Umbral bienestar (70)',data:Array(8).fill(70),borderColor:'#059669',borderDash:[4,4],borderWidth:1.5,pointRadius:0,fill:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:CHART_FONT,usePointStyle:true,padding:12},position:'bottom'},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,min:20,max:100,ticks:{...SCALE_Y.ticks,callback:v=>v+'/100'}}}}});

    const erCtx=document.getElementById('chart-emp-radar');
    if(erCtx){
      const radarData=[e.radar[0],e.radar[1],e.radar[2],Math.max(0,100-e.metrics.cargaTareas+50),e.radar[4],e.radar[5]];
      charts.empRadar=new Chart(erCtx,{type:'radar',data:{labels:['Energía','Concentración','Satisfacción','Carga\n(inv.)','Relaciones','Autonomía'],datasets:[{label:e.name,data:radarData,borderColor:e.avatarColor,backgroundColor:e.avatarColor+'28',pointBackgroundColor:e.avatarColor,pointRadius:4,borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:TOOLTIP},scales:{r:{min:0,max:100,ticks:{stepSize:25,font:{size:9},color:'#7A8394'},grid:{color:'rgba(15,20,25,0.08)'},pointLabels:{font:{size:10,family:'Inter'},color:'#3D4552'}}}}});
    }
  }

  if(viewId==='analitica'){
    const weeks=['S13','S14','S15','S16','S17','S18','S19','S20'];
    const metrics={
      wellbeing_index:{label:'Índice de Bienestar',unit:'/100',type:'line'},
      reuniones:{label:'Reuniones por día',unit:'',type:'bar'},
      tareas:{label:'Carga de Tareas',unit:'%',type:'bar'},
      productividad:{label:'Productividad',unit:'%',type:'line'},
      horas_extra:{label:'Horas Extra',unit:'h',type:'line'},
      respuesta_email:{label:'Tiempo Respuesta Email',unit:'%',type:'bar'},
      teletrabajo:{label:'Días Teletrabajo',unit:' días',type:'bar'},
      absentismo:{label:'Absentismo',unit:'%',type:'line'}
    };
    const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];
    const deptColors=['#2563EB','#059669','#DC2626','#7c3aed','#D97706'];

    function getAnalyticsData(metric,level){
      if(level==='company'){
        const companyTrend=Array.from({length:8},(_,i)=>Math.round(employees.reduce((s,e)=>{
          const v=metric==='wellbeing_index'?e.index:metric==='reuniones'?e.metrics.reuniones:metric==='tareas'?e.metrics.cargaTareas:metric==='productividad'?e.metrics.productividad:metric==='horas_extra'?e.metrics.horasExtra:metric==='respuesta_email'?e.metrics.respEmail:metric==='teletrabajo'?e.metrics.teletrabajo:5;
          return s+v;
        },0)/employees.length));
        return{labels:weeks,datasets:[{label:'Empresa',data:companyTrend,borderColor:'#1E3A5F',backgroundColor:'rgba(30,58,95,0.09)',tension:.4,fill:metric==='wellbeing_index',borderRadius:6,pointRadius:5}]};
      }
      if(level==='departamento'){
        const datasets=depts.map((d,i)=>{
          const emps=getEmpsByDept(d);
          const avg=emps.length?Math.round(emps.reduce((s,e)=>{
            const v=metric==='wellbeing_index'?e.index:metric==='reuniones'?e.metrics.reuniones:metric==='tareas'?e.metrics.cargaTareas:metric==='productividad'?e.metrics.productividad:metric==='horas_extra'?e.metrics.horasExtra:metric==='respuesta_email'?e.metrics.respEmail:metric==='teletrabajo'?e.metrics.teletrabajo:5;
            return s+v;
          },0)/emps.length):0;
          return{label:d.length>14?d.slice(0,14)+'…':d,data:depts.map((_,j)=>j===i?avg:null).filter(Boolean).length?[avg]:Array(depts.length).fill(0).map((_,j)=>j===i?avg:0),backgroundColor:deptColors[i]+'CC',borderColor:deptColors[i],borderWidth:1.5,borderRadius:6};
        });
        return{labels:depts.map(d=>d.length>12?d.slice(0,12)+'…':d),datasets:[{label:'Por Departamento',data:depts.map((d)=>{const emps=getEmpsByDept(d);return emps.length?Math.round(emps.reduce((s,e)=>{const v=metric==='wellbeing_index'?e.index:metric==='reuniones'?e.metrics.reuniones:metric==='tareas'?e.metrics.cargaTareas:metric==='productividad'?e.metrics.productividad:metric==='horas_extra'?e.metrics.horasExtra:metric==='respuesta_email'?e.metrics.respEmail:metric==='teletrabajo'?e.metrics.teletrabajo:5;return s+v;},0)/emps.length):0;}),backgroundColor:deptColors.map(c=>c+'CC'),borderColor:deptColors,borderWidth:1.5,borderRadius:6}]};
      }
      if(level==='trabajador'){
        const emp=employees.find(e=>e.id===selectedEmployee)||employees[0];
        const vals=emp.trend.map((_,i)=>metric==='wellbeing_index'?emp.trend[i]:metric==='horas_extra'?emp.metrics.horasExtra+(Math.random()*.4-.2):emp.metrics.productividad+(Math.random()*4-2)|0);
        return{labels:weeks,datasets:[{label:emp.name,data:vals.map(v=>+v.toFixed(1)),borderColor:emp.avatarColor,backgroundColor:emp.avatarColor+'18',tension:.4,fill:true,pointRadius:5}]};
      }
      return{labels:weeks,datasets:[]};
    }

    const m=metrics[analyticsMetric]||metrics.wellbeing_index;
    const data=getAnalyticsData(analyticsMetric,analyticsLevel);
    const isBar=analyticsLevel==='departamento'||m.type==='bar';
    const aCtx=document.getElementById('chart-analytics');
    if(aCtx){
      charts.analytics=new Chart(aCtx,{
        type:isBar?'bar':'line',
        data,
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:CHART_FONT,usePointStyle:true,padding:14}},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,ticks:{...SCALE_Y.ticks,callback:v=>v+m.unit}}}}
      });
    }
  }

  if(viewId==='historico'){
    const depts=['Producto & Tech','Ventas','Operaciones','Marketing','Soporte'];
    const deptColors=['#2563EB','#059669','#DC2626','#7c3aed','#D97706'];
    const histData={
      'Producto & Tech':[72,70,67,64,63,60,59,61,62,63,64,61],
      'Ventas':[68,70,72,73,74,74,75,74,73,74,75,74],
      'Operaciones':[65,60,57,52,49,47,46,48,49,50,51,48],
      'Marketing':[75,76,78,80,81,82,83,82,83,84,85,82],
      'Soporte':[68,67,65,66,64,65,67,66,65,66,67,66]
    };
    const weeks12=Array.from({length:12},(_,i)=>'S'+(i+10));
    const hCtx=document.getElementById('chart-historico');
    if(hCtx){
      charts.historico=new Chart(hCtx,{type:'line',data:{labels:weeks12,datasets:depts.map((d,i)=>({label:d,data:histData[d],borderColor:deptColors[i],backgroundColor:'transparent',tension:.4,pointRadius:3,pointHoverRadius:6,borderWidth:2}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:CHART_FONT,usePointStyle:true,padding:12},position:'bottom'},tooltip:TOOLTIP},scales:{x:SCALE_X,y:{...SCALE_Y,min:30,max:100,ticks:{...SCALE_Y.ticks,callback:v=>v+'/100'}}}}});
    }
  }

  // Populate demo employee selector
  const sel=document.getElementById('demo-emp-sel');
  if(sel && sel.options.length===0){
    employees.forEach(e=>{
      const o=document.createElement('option');
      o.value=e.id; o.textContent=`${e.name} (${e.dept})`;
      sel.appendChild(o);
    });
    sel.value=employees[1].id; // default to Pablo (red) for demo impact
  }
}
"""

OLD_ATTACH = """function attachCEOEvents(viewId) {
  // view-specific post-render hooks (reserved)
}"""
src = src.replace(OLD_ATTACH, NEW_ATTACH, 1)

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 7 done. Lines:", src.count('\n'))
