with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 4. EMPLOYEE DATA (25 employees) inserted after teams array ──
EMPLOYEE_DATA = """
// ═══════════════════════════════════════════════════
// 25 EMPLOYEE PROFILES
// ═══════════════════════════════════════════════════
const employees = [
  // ── Producto & Tech (6) ──
  {id:'e01',name:'Ana García',role:'Frontend Developer',dept:'Producto & Tech',email:'ana.garcia@empresa.com',avatar:'AG',avatarColor:'#2563EB',age:32,status:'amber',index:63,risk:52,
   trend:[75,72,70,68,65,63,62,63],
   metrics:{horasExtra:1.5,reuniones:5.2,cargaTareas:112,respEmail:24,teletrabajo:2,productividad:68},
   signals:[{icon:'🕐',text:'Extensión horaria +1h 30min',sev:'amber'},{icon:'📅',text:'5 reuniones fuera de horario esta semana',sev:'red'},{icon:'💬',text:'Tiempo respuesta email +24%',sev:'amber'}],
   radar:[65,70,63,45,72,68],checkin:{energia:5,estres:7,satisfaccion:6,apoyo:7}},
  {id:'e02',name:'Pablo Moreno',role:'Backend Developer',dept:'Producto & Tech',email:'pablo.moreno@empresa.com',avatar:'PM',avatarColor:'#DC2626',age:28,status:'red',index:44,risk:78,
   trend:[68,63,58,54,50,47,44,44],
   metrics:{horasExtra:3.2,reuniones:4.1,cargaTareas:148,respEmail:61,teletrabajo:1,productividad:45},
   signals:[{icon:'🚨',text:'Carga de trabajo al 148% de capacidad',sev:'red'},{icon:'🕐',text:'Extensión horaria +3h 15min diarias',sev:'red'},{icon:'😶',text:'Sin día libre en 14 días consecutivos',sev:'red'},{icon:'📉',text:'Productividad cayendo (-23% en 4 semanas)',sev:'red'}],
   radar:[35,48,40,20,55,42],checkin:{energia:3,estres:9,satisfaccion:3,apoyo:4}},
  {id:'e03',name:'Marta Sánchez',role:'UX Designer',dept:'Producto & Tech',email:'marta.sanchez@empresa.com',avatar:'MS',avatarColor:'#059669',age:35,status:'green',index:78,risk:22,
   trend:[72,74,75,76,77,78,77,78],
   metrics:{horasExtra:0.3,reuniones:3.4,cargaTareas:82,respEmail:8,teletrabajo:3,productividad:84},
   signals:[{icon:'✅',text:'Carga equilibrada al 82%',sev:'green'},{icon:'🌿',text:'Buena desconexión digital por las noches',sev:'green'}],
   radar:[82,78,80,75,85,88],checkin:{energia:8,estres:3,satisfaccion:8,apoyo:9}},
  {id:'e04',name:'Lucas Hernández',role:'DevOps Engineer',dept:'Producto & Tech',email:'lucas.hernandez@empresa.com',avatar:'LH',avatarColor:'#D97706',age:30,status:'amber',index:57,risk:61,
   trend:[70,68,65,62,60,58,57,57],
   metrics:{horasExtra:2.1,reuniones:3.8,cargaTareas:124,respEmail:38,teletrabajo:2,productividad:61},
   signals:[{icon:'⚙️',text:'Guardia nocturna 2 veces esta semana',sev:'red'},{icon:'🕐',text:'Extensión horaria +2h diarias',sev:'amber'},{icon:'💬',text:'Respuesta email fines de semana',sev:'amber'}],
   radar:[58,65,55,40,68,60],checkin:{energia:5,estres:7,satisfaccion:5,apoyo:6}},
  {id:'e05',name:'Carla Jiménez',role:'Product Manager',dept:'Producto & Tech',email:'carla.jimenez@empresa.com',avatar:'CJ',avatarColor:'#DC2626',age:29,status:'red',index:41,risk:82,
   trend:[72,66,59,53,49,44,42,41],
   metrics:{horasExtra:3.8,reuniones:8.2,cargaTareas:162,respEmail:74,teletrabajo:0,productividad:38},
   signals:[{icon:'🚨',text:'8 reuniones diarias promedio — agotamiento cognitivo',sev:'red'},{icon:'🕐',text:'Extensión horaria +3h 45min',sev:'red'},{icon:'📉',text:'Carga al 162% — máximo histórico personal',sev:'red'},{icon:'😶',text:'Check-ins muestran estrés nivel 9/10',sev:'red'}],
   radar:[30,38,35,15,45,32],checkin:{energia:2,estres:9,satisfaccion:2,apoyo:3}},
  {id:'e06',name:'Diego López',role:'Data Engineer',dept:'Producto & Tech',email:'diego.lopez@empresa.com',avatar:'DL',avatarColor:'#059669',age:33,status:'green',index:72,risk:28,
   trend:[65,67,68,70,71,72,72,72],
   metrics:{horasExtra:0.5,reuniones:2.9,cargaTareas:88,respEmail:12,teletrabajo:4,productividad:79},
   signals:[{icon:'✅',text:'Tendencia de mejora sostenida (+7 pts en 8 semanas)',sev:'green'},{icon:'🌿',text:'Carga de trabajo equilibrada',sev:'green'}],
   radar:[75,72,74,72,78,82],checkin:{energia:7,estres:3,satisfaccion:7,apoyo:8}},

  // ── Ventas (5) ──
  {id:'e07',name:'Roberto García',role:'Account Executive',dept:'Ventas',email:'roberto.garcia@empresa.com',avatar:'RG',avatarColor:'#059669',age:38,status:'green',index:80,risk:18,
   trend:[74,76,77,78,79,80,81,80],
   metrics:{horasExtra:0.4,reuniones:4.5,cargaTareas:78,respEmail:6,teletrabajo:2,productividad:87},
   signals:[{icon:'✅',text:'Indicadores en zona de bienestar',sev:'green'},{icon:'🏆',text:'Mejor índice del equipo de ventas',sev:'green'}],
   radar:[84,80,82,78,88,85],checkin:{energia:8,estres:2,satisfaccion:8,apoyo:9}},
  {id:'e08',name:'Sofía Martínez',role:'Sales Manager',dept:'Ventas',email:'sofia.martinez@empresa.com',avatar:'SM',avatarColor:'#D97706',age:31,status:'amber',index:65,risk:45,
   trend:[70,70,68,67,66,65,65,65],
   metrics:{horasExtra:1.2,reuniones:6.8,cargaTareas:104,respEmail:22,teletrabajo:1,productividad:71},
   signals:[{icon:'📅',text:'Alta carga de reuniones como manager (6.8/día)',sev:'amber'},{icon:'💬',text:'Responde emails fuera de horario 4 días/semana',sev:'amber'}],
   radar:[68,62,65,55,72,60],checkin:{energia:6,estres:6,satisfaccion:6,apoyo:7}},
  {id:'e09',name:'Antonio Ruiz',role:'Business Dev (BDR)',dept:'Ventas',email:'antonio.ruiz@empresa.com',avatar:'AR',avatarColor:'#059669',age:26,status:'green',index:76,risk:24,
   trend:[70,72,73,74,75,76,76,76],
   metrics:{horasExtra:0.6,reuniones:3.2,cargaTareas:85,respEmail:10,teletrabajo:3,productividad:82},
   signals:[{icon:'✅',text:'Tendencia positiva constante',sev:'green'},{icon:'🌿',text:'Buena gestión del tiempo',sev:'green'}],
   radar:[78,75,76,74,80,79],checkin:{energia:7,estres:3,satisfaccion:8,apoyo:8}},
  {id:'e10',name:'Laura Pérez',role:'Key Account Manager',dept:'Ventas',email:'laura.perez@empresa.com',avatar:'LP',avatarColor:'#059669',age:34,status:'green',index:82,risk:15,
   trend:[76,78,79,80,81,82,82,82],
   metrics:{horasExtra:0.2,reuniones:3.8,cargaTareas:74,respEmail:4,teletrabajo:2,productividad:90},
   signals:[{icon:'⭐',text:'Indicadores excelentes — referente del equipo',sev:'green'},{icon:'✅',text:'Carga óptima y desconexión saludable',sev:'green'}],
   radar:[88,85,87,85,90,88],checkin:{energia:9,estres:2,satisfaccion:9,apoyo:9}},
  {id:'e11',name:'Carlos Gómez',role:'Sales Operations',dept:'Ventas',email:'carlos.gomez@empresa.com',avatar:'CG',avatarColor:'#D97706',age:29,status:'amber',index:61,risk:49,
   trend:[68,67,65,63,62,61,61,61],
   metrics:{horasExtra:1.6,reuniones:4.9,cargaTareas:108,respEmail:28,teletrabajo:2,productividad:66},
   signals:[{icon:'📊',text:'Carga por encima del 100%',sev:'amber'},{icon:'🕐',text:'Extensión horaria moderada (+1h 35min)',sev:'amber'}],
   radar:[62,60,61,48,65,58],checkin:{energia:5,estres:6,satisfaccion:5,apoyo:6}},

  // ── Operaciones (7) ──
  {id:'e12',name:'Elena Vidal',role:'Operations Manager',dept:'Operaciones',email:'elena.vidal@empresa.com',avatar:'EV',avatarColor:'#DC2626',age:41,status:'red',index:38,risk:87,
   trend:[60,55,50,46,43,40,38,38],
   metrics:{horasExtra:4.5,reuniones:9.1,cargaTareas:175,respEmail:92,teletrabajo:0,productividad:32},
   signals:[{icon:'🚨',text:'Carga crítica al 175% de capacidad',sev:'red'},{icon:'🚨',text:'9+ reuniones diarias — riesgo burnout severo',sev:'red'},{icon:'🕐',text:'Extensión horaria +4h 30min diarias',sev:'red'},{icon:'😶',text:'18 días consecutivos sin descanso',sev:'red'}],
   radar:[25,30,28,10,38,25],checkin:{energia:2,estres:10,satisfaccion:2,apoyo:2}},
  {id:'e13',name:'Javier Torres',role:'Supply Chain',dept:'Operaciones',email:'javier.torres@empresa.com',avatar:'JT',avatarColor:'#DC2626',age:36,status:'red',index:43,risk:74,
   trend:[62,58,54,50,48,45,43,43],
   metrics:{horasExtra:3.4,reuniones:5.8,cargaTareas:152,respEmail:68,teletrabajo:0,productividad:40},
   signals:[{icon:'🚨',text:'Carga al 152%',sev:'red'},{icon:'🕐',text:'Horas extra +3h 25min diarias',sev:'red'},{icon:'📦',text:'Bajo índice de desconexión digital',sev:'red'}],
   radar:[38,42,40,18,48,35],checkin:{energia:3,estres:9,satisfaccion:3,apoyo:4}},
  {id:'e14',name:'María González',role:'Logistics Coordinator',dept:'Operaciones',email:'maria.gonzalez@empresa.com',avatar:'MG',avatarColor:'#D97706',age:33,status:'amber',index:55,risk:58,
   trend:[65,63,61,59,57,55,55,55],
   metrics:{horasExtra:2.2,reuniones:4.6,cargaTareas:120,respEmail:42,teletrabajo:1,productividad:58},
   signals:[{icon:'🕐',text:'Extensión horaria +2h 10min',sev:'amber'},{icon:'📊',text:'Carga de trabajo elevada (120%)',sev:'amber'}],
   radar:[55,52,54,38,60,50],checkin:{energia:5,estres:7,satisfaccion:4,apoyo:5}},
  {id:'e15',name:'Álvaro Romero',role:'Process Analyst',dept:'Operaciones',email:'alvaro.romero@empresa.com',avatar:'AL',avatarColor:'#DC2626',age:27,status:'red',index:46,risk:71,
   trend:[65,60,57,53,50,48,46,46],
   metrics:{horasExtra:3.0,reuniones:4.2,cargaTareas:138,respEmail:55,teletrabajo:0,productividad:44},
   signals:[{icon:'🚨',text:'Carga al 138% — llevan 6 semanas bajando',sev:'red'},{icon:'🕐',text:'Extensión horaria +3h diarias',sev:'red'},{icon:'😶',text:'Nivel estrés 8/10 en últimos 3 check-ins',sev:'red'}],
   radar:[40,45,38,22,50,42],checkin:{energia:3,estres:8,satisfaccion:3,apoyo:4}},
  {id:'e16',name:'Natalia Fernández',role:'Operations Coordinator',dept:'Operaciones',email:'natalia.fernandez@empresa.com',avatar:'NF',avatarColor:'#D97706',age:30,status:'amber',index:58,risk:54,
   trend:[66,64,62,61,59,58,58,58],
   metrics:{horasExtra:1.8,reuniones:5.1,cargaTareas:116,respEmail:35,teletrabajo:1,productividad:62},
   signals:[{icon:'📅',text:'Reuniones fuera de horario 3x esta semana',sev:'amber'},{icon:'🕐',text:'Extensión horaria +1h 50min',sev:'amber'}],
   radar:[58,55,57,42,62,54],checkin:{energia:5,estres:7,satisfaccion:5,apoyo:5}},
  {id:'e17',name:'Sergio Muñoz',role:'Operations Specialist',dept:'Operaciones',email:'sergio.munoz@empresa.com',avatar:'SG',avatarColor:'#DC2626',age:38,status:'red',index:40,risk:83,
   trend:[62,58,53,49,46,42,40,40],
   metrics:{horasExtra:4.1,reuniones:5.5,cargaTareas:161,respEmail:80,teletrabajo:0,productividad:35},
   signals:[{icon:'🚨',text:'Carga al 161% durante 5 semanas seguidas',sev:'red'},{icon:'🕐',text:'Extensión horaria +4h 05min',sev:'red'},{icon:'🌙',text:'Actividad laboral habitual >22:00',sev:'red'},{icon:'😶',text:'Estrés 9/10 — riesgo de baja inminente',sev:'red'}],
   radar:[32,35,30,12,40,28],checkin:{energia:2,estres:9,satisfaccion:2,apoyo:3}},
  {id:'e18',name:'Patricia Díaz',role:'Project Coordinator',dept:'Operaciones',email:'patricia.diaz@empresa.com',avatar:'PD',avatarColor:'#D97706',age:35,status:'amber',index:62,risk:47,
   trend:[68,67,65,64,63,62,62,62],
   metrics:{horasExtra:1.4,reuniones:5.8,cargaTareas:110,respEmail:26,teletrabajo:2,productividad:65},
   signals:[{icon:'📅',text:'Alta carga de coordinación (5.8 reuniones/día)',sev:'amber'},{icon:'💬',text:'Tiempo respuesta email +26%',sev:'amber'}],
   radar:[62,58,63,50,66,60],checkin:{energia:6,estres:6,satisfaccion:5,apoyo:6}},

  // ── Marketing (4) ──
  {id:'e19',name:'David Chen',role:'Chief Marketing Officer',dept:'Marketing',email:'david.chen@empresa.com',avatar:'DC',avatarColor:'#7c3aed',age:42,status:'green',index:84,risk:12,
   trend:[78,80,81,82,83,84,84,84],
   metrics:{horasExtra:0.2,reuniones:4.2,cargaTareas:72,respEmail:5,teletrabajo:3,productividad:91},
   signals:[{icon:'⭐',text:'Índice excelente — liderazgo saludable',sev:'green'},{icon:'✅',text:'Buena delegación y gestión del tiempo',sev:'green'}],
   radar:[88,86,87,84,90,92],checkin:{energia:9,estres:2,satisfaccion:9,apoyo:9}},
  {id:'e20',name:'Camila Rodríguez',role:'Content Creator',dept:'Marketing',email:'camila.rodriguez@empresa.com',avatar:'CR',avatarColor:'#7c3aed',age:27,status:'green',index:88,risk:8,
   trend:[82,84,85,86,87,88,88,88],
   metrics:{horasExtra:0.1,reuniones:2.1,cargaTareas:68,respEmail:3,teletrabajo:5,productividad:94},
   signals:[{icon:'⭐',text:'Índice más alto de la empresa',sev:'green'},{icon:'✅',text:'Excelente equilibrio vida-trabajo',sev:'green'}],
   radar:[92,90,94,88,88,95],checkin:{energia:9,estres:1,satisfaccion:10,apoyo:10}},
  {id:'e21',name:'Tomás Alves',role:'Growth Hacker',dept:'Marketing',email:'tomas.alves@empresa.com',avatar:'TA',avatarColor:'#7c3aed',age:31,status:'green',index:79,risk:20,
   trend:[73,74,75,76,77,78,79,79],
   metrics:{horasExtra:0.4,reuniones:3.0,cargaTareas:80,respEmail:9,teletrabajo:4,productividad:85},
   signals:[{icon:'✅',text:'Carga equilibrada y tendencia positiva',sev:'green'},{icon:'🌿',text:'Buena desconexión digital',sev:'green'}],
   radar:[82,80,81,78,84,85],checkin:{energia:8,estres:2,satisfaccion:8,apoyo:9}},
  {id:'e22',name:'Isabel Ramos',role:'Brand Manager',dept:'Marketing',email:'isabel.ramos@empresa.com',avatar:'IR',avatarColor:'#D97706',age:35,status:'amber',index:67,risk:38,
   trend:[72,71,70,69,68,67,67,67],
   metrics:{horasExtra:1.0,reuniones:5.5,cargaTareas:98,respEmail:20,teletrabajo:2,productividad:72},
   signals:[{icon:'📅',text:'Carga de reuniones elevada para su rol',sev:'amber'},{icon:'⚠️',text:'Tendencia ligeramente decreciente (-5 pts en 8 sem)',sev:'amber'}],
   radar:[68,65,68,58,72,64],checkin:{energia:6,estres:5,satisfaccion:6,apoyo:7}},

  // ── Soporte (3) ──
  {id:'e23',name:'Elena Torres',role:'Support Lead',dept:'Soporte',email:'elena.torres@empresa.com',avatar:'ET',avatarColor:'#D97706',age:39,status:'amber',index:64,risk:43,
   trend:[68,67,66,65,64,64,64,64],
   metrics:{horasExtra:1.3,reuniones:4.8,cargaTareas:106,respEmail:24,teletrabajo:2,productividad:69},
   signals:[{icon:'📊',text:'Carga moderadamente elevada (106%)',sev:'amber'},{icon:'💬',text:'Gestión emocional de tickets de soporte',sev:'amber'}],
   radar:[65,63,64,52,70,60],checkin:{energia:6,estres:6,satisfaccion:6,apoyo:7}},
  {id:'e24',name:'Andrés Castro',role:'Support Agent',dept:'Soporte',email:'andres.castro@empresa.com',avatar:'AC',avatarColor:'#D97706',age:25,status:'amber',index:60,risk:52,
   trend:[66,65,63,62,61,60,60,60],
   metrics:{horasExtra:1.7,reuniones:3.5,cargaTareas:115,respEmail:32,teletrabajo:1,productividad:64},
   signals:[{icon:'📞',text:'Carga emocional por volumen de tickets',sev:'amber'},{icon:'🕐',text:'Extensión horaria +1h 45min',sev:'amber'}],
   radar:[60,58,60,45,65,55],checkin:{energia:5,estres:7,satisfaccion:5,apoyo:6}},
  {id:'e25',name:'Pilar Navarro',role:'Technical Support',dept:'Soporte',email:'pilar.navarro@empresa.com',avatar:'PN',avatarColor:'#059669',age:31,status:'green',index:71,risk:30,
   trend:[65,67,68,69,70,71,71,71],
   metrics:{horasExtra:0.6,reuniones:3.2,cargaTareas:88,respEmail:14,teletrabajo:3,productividad:76},
   signals:[{icon:'✅',text:'Índice en zona verde y mejorando',sev:'green'},{icon:'🌿',text:'Carga equilibrada',sev:'green'}],
   radar:[73,71,72,68,74,75],checkin:{energia:7,estres:4,satisfaccion:7,apoyo:8}}
];

// ── Helper functions ──
function getEmpsByDept(dept){ return employees.filter(e=>e.dept===dept); }
function getCompanyStats(){
  const n=employees.length;
  const avg=Math.round(employees.reduce((s,e)=>s+e.index,0)/n);
  const green=employees.filter(e=>e.status==='green').length;
  const amber=employees.filter(e=>e.status==='amber').length;
  const red=employees.filter(e=>e.status==='red').length;
  const critRisk=employees.filter(e=>e.risk>=70);
  return{n,avg,green,amber,red,critRisk};
}
function statusColor(s){ return s==='green'?'var(--green)':s==='amber'?'var(--amber)':'var(--terra)'; }
function statusBadgeClass(s){ return s==='green'?'status-green':s==='amber'?'status-amber':'status-red'; }
function statusLabel(s){ return s==='green'?'🌿 Bienestar':s==='amber'?'⚠️ Atención':'🚨 Crítico'; }
function riskClass(r){ return r>=70?'risk-high':r>=40?'risk-med':'risk-low'; }
function riskLabel(r){ return r>=70?'Alto':r>=40?'Moderado':'Bajo'; }
function idxColor(v){ return v>=70?'var(--green)':v>=40?'var(--amber)':'var(--terra)'; }
"""

# Insert employee data after the closing of teams array
# Find the unique end of teams array
ANCHOR = '  },\n];\n\nfunction ceoViewEquipos() {'
src = src.replace(ANCHOR, '  },\n];\n' + EMPLOYEE_DATA + '\nfunction ceoViewEquipos() {', 1)

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 2 done. Lines:", src.count('\n'))
