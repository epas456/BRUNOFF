with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ── 15. Demo employee selector + switchDemoEmployee wiring ──
# Replace the old switchDemoEmployee stub (it was added in part3)
OLD_DEMO_FN = r"""function switchDemoEmployee(id){
  currentRole='empleado';
  // rebuild emp portal - find emp
  const e=employees.find(x=>x.id===id);
  if(!e) return;
  buildApp();
}"""

NEW_DEMO_FN = r"""function switchDemoEmployee(id){
  selectedEmployee=id;
  // Switch to CEO employee detail view so investors can see individual metrics
  if(currentRole==='ceo'){
    openEmployee(id);
  } else {
    // Build CEO view focused on this employee
    currentRole='ceo';
    buildApp();
    setTimeout(()=>openEmployee(id),50);
  }
}"""
src = src.replace(OLD_DEMO_FN, NEW_DEMO_FN, 1)

# ── 16. Populate demo selector on initial CEO build ──
OLD_BUILD_CEO = """function buildCEOApp() {
  buildSidebar(ceoViews, 'dashboard');
  renderCEOView('dashboard');
}"""
NEW_BUILD_CEO = """function buildCEOApp() {
  buildSidebar(ceoViews, 'dashboard');
  renderCEOView('dashboard');
  // Populate demo employee selector
  setTimeout(()=>{
    const sel=document.getElementById('demo-emp-sel');
    if(sel && sel.options.length===0){
      employees.forEach(e=>{
        const o=document.createElement('option');
        o.value=e.id;
        o.textContent=`${e.name} — ${e.dept}`;
        sel.appendChild(o);
      });
    }
  },100);
}"""
src = src.replace(OLD_BUILD_CEO, NEW_BUILD_CEO, 1)

# ── 17. Verify JS brace balance ──
import re
script_match = re.search(r'<script>(.*?)</script>', src, re.DOTALL)
if script_match:
    js = script_match.group(1)
    opens = js.count('{')
    closes = js.count('}')
    print(f"JS braces {{ = {opens}, }} = {closes}, diff = {opens-closes}")
else:
    print("No script tag found")

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 10 done. Lines:", src.count('\n'))
