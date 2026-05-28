with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 5. Add selectedEmployee state + destroyAllCharts ──
OLD_STATE = "let currentRole = 'ceo';"
NEW_STATE = """let currentRole = 'ceo';
let selectedEmployee = null;
let charts = {};
function destroyAllCharts(){
  Object.values(charts).forEach(c=>{ try{c.destroy();}catch(e){} });
  charts={};
}"""
src = src.replace(OLD_STATE, NEW_STATE, 1)

# ── 6. Patch renderCEOView: destroyAllCharts + empleado case ──
OLD_RENDER = """function renderCEOView(viewId) {
  setActiveNav(viewId);
  const mc = document.getElementById('main-content');
  mc.innerHTML = '';
  mc.className = 'main-content fade-enter';
  if (viewId === 'dashboard')    mc.innerHTML = ceoViewDashboard();
  else if (viewId === 'equipos') mc.innerHTML = ceoViewEquipos();
  else if (viewId === 'acciones') mc.innerHTML = ceoViewAcciones();
  else if (viewId === 'historico') mc.innerHTML = ceoViewHistorico();
  else if (viewId === 'analitica') mc.innerHTML = ceoViewAnalitica();
  else if (viewId === 'absentismo') mc.innerHTML = ceoViewAbsentismo();
  else if (viewId === 'integraciones') mc.innerHTML = ceoViewIntegraciones();
  else if (viewId === 'configuracion') mc.innerHTML = ceoViewConfiguracion();
  else if (viewId === 'privacidad') mc.innerHTML = ceoViewPrivacidad();
  else if (viewId === 'centrodatos') mc.innerHTML = ceoViewCentroDatos();
  attachCEOEvents(viewId);
}"""
NEW_RENDER = """function renderCEOView(viewId) {
  destroyAllCharts();
  setActiveNav(viewId);
  const mc = document.getElementById('main-content');
  mc.innerHTML = '';
  mc.className = 'main-content fade-enter';
  if (viewId === 'dashboard')       mc.innerHTML = ceoViewDashboard();
  else if (viewId === 'equipos')    mc.innerHTML = ceoViewEquipos();
  else if (viewId === 'empleado')   mc.innerHTML = ceoViewEmployeeDetail(selectedEmployee);
  else if (viewId === 'acciones')   mc.innerHTML = ceoViewAcciones();
  else if (viewId === 'historico')  mc.innerHTML = ceoViewHistorico();
  else if (viewId === 'analitica')  mc.innerHTML = ceoViewAnalitica();
  else if (viewId === 'absentismo') mc.innerHTML = ceoViewAbsentismo();
  else if (viewId === 'integraciones') mc.innerHTML = ceoViewIntegraciones();
  else if (viewId === 'configuracion') mc.innerHTML = ceoViewConfiguracion();
  else if (viewId === 'privacidad') mc.innerHTML = ceoViewPrivacidad();
  else if (viewId === 'centrodatos') mc.innerHTML = ceoViewCentroDatos();
  attachCEOEvents(viewId);
}
function openEmployee(id){
  selectedEmployee=id;
  renderCEOView('empleado');
}
function switchDemoEmployee(id){
  currentRole='empleado';
  // rebuild emp portal - find emp
  const e=employees.find(x=>x.id===id);
  if(!e) return;
  buildApp();
}"""
src = src.replace(OLD_RENDER, NEW_RENDER, 1)

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 3 done. Lines:", src.count('\n'))
