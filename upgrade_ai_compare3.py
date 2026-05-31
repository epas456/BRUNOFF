with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# ══════════════════════════════════════════════════
# 6. ADD AI PANEL HTML + FAB before </body>
# ══════════════════════════════════════════════════
AI_PANEL_HTML = """
<!-- ═══════════════════════════════════════════════════
     AI ASSISTANT PANEL
═══════════════════════════════════════════════════ -->
<div id="ai-overlay" class="ai-overlay" onclick="closeAIPanel()"></div>
<div id="ai-panel" class="ai-panel">
  <div class="ai-panel-header">
    <div>
      <div class="ai-panel-title">🤖 BURNOFF-AI Asistente</div>
      <div class="ai-panel-sub">DATOS EN TIEMPO REAL · 25 EMPLEADOS</div>
    </div>
    <div class="ai-close-btn" onclick="closeAIPanel()">✕</div>
  </div>
  <div id="ai-messages" class="ai-messages">
    <div style="text-align:center;color:var(--ink4);padding:40px 20px;font-size:12px">
      Escribe una pregunta o usa los accesos rápidos de abajo
    </div>
  </div>
  <div class="ai-quick-chips">
    <div style="width:100%;font-size:10px;font-weight:600;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">Accesos rápidos</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Resumen global de la empresa')">🏢 Resumen empresa</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('¿Quién tiene mayor riesgo de burnout?')">🚨 Top riesgo</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Compara todos los departamentos')">📊 Comparar depts</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Briefing de Elena Vidal')">📋 Briefing crítico</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('¿Quién tiene mejor bienestar?')">🌿 Top bienestar</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Análisis de horas extra')">🕐 Horas extra</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Predicción de bajas próximas semanas')">🔮 Predicción bajas</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Análisis de reuniones y meeting fatigue')">📅 Reuniones</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Briefing de Camila Rodríguez')">⭐ Mejor empleada</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Análisis de productividad')">📈 Productividad</div>
    <div class="ai-quick-chip" onclick="handleAIQuickAction('Teletrabajo y trabajo remoto')">🏠 Teletrabajo</div>
  </div>
  <div class="ai-input-row">
    <input id="ai-input" class="ai-input" type="text" placeholder="Pregunta sobre métricas, empleados, departamentos..." onkeydown="aiInputKeydown(event)">
    <div class="ai-send-btn" onclick="sendAIMessage()">➤</div>
  </div>
</div>
"""

src = src.replace('</body>\n</html>', AI_PANEL_HTML + '</body>\n</html>')

# ══════════════════════════════════════════════════
# 7. VERIFY
# ══════════════════════════════════════════════════
import re
script = re.search(r'<script>(.*?)</script>', src, re.DOTALL).group(1)
opens = script.count('{')
closes = script.count('}')

checks = [
    ('AI panel HTML', 'id="ai-panel"' in src),
    ('AI messages div', 'id="ai-messages"' in src),
    ('AI input', 'id="ai-input"' in src),
    ('AI overlay', 'id="ai-overlay"' in src),
    ('openAIPanel fn', 'function openAIPanel()' in src),
    ('sendAIMessage fn', 'function sendAIMessage()' in src),
    ('generateAIResponse fn', 'function generateAIResponse(input)' in src),
    ('generateEmpBriefing fn', 'function generateEmpBriefing(e)' in src),
    ('toggleCompareEmployee fn', 'function toggleCompareEmployee(id)' in src),
    ('analyticsSelectedEmps state', 'analyticsSelectedEmps' in src),
    ('emp-compare-chip CSS', '.emp-compare-chip{' in src),
    ('ai-panel CSS', '.ai-panel{' in src),
    ('multi-dataset chart', 'analyticsSelectedEmps.map(id=>' in src),
    ('quick chips', 'ai-quick-chip' in src),
    ('JS balance', opens == closes),
]
all_ok = all(v for _,v in checks)
for name,ok in checks:
    print(f'  {"✓" if ok else "✗"} {name}')
print(f'\nAll checks: {all_ok}  |  JS {{ = {opens}, }} = {closes}  |  Lines: {src.count(chr(10))}')

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
