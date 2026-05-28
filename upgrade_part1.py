import re
with open('BURNOFF_V0.html','r',encoding='utf-8') as f:
    src=f.read()

# 1. Chart.js CDN
src=src.replace(
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n<link rel="preconnect" href="https://fonts.googleapis.com">'
)

# 2. Extra CSS before </style>
NEW_CSS="""
/* ── EMPLOYEE TABLE ── */
.emp-table{width:100%;border-collapse:collapse;font-size:12px}
.emp-table thead th{padding:9px 12px;text-align:left;font-size:10px;font-weight:600;color:var(--ink3);letter-spacing:.06em;text-transform:uppercase;border-bottom:2px solid var(--border-md);white-space:nowrap}
.emp-table tbody tr{cursor:pointer;transition:background 100ms;border-bottom:1px solid var(--border)}
.emp-table tbody tr:hover{background:var(--cobalt-light)}
.emp-table tbody td{padding:10px 12px;color:var(--ink2);vertical-align:middle}
.emp-av{width:30px;height:30px;border-radius:50%;color:#fff;font-size:10px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;margin-right:8px}
.emp-name-wrap{display:flex;align-items:center}
.emp-name{font-weight:600;color:var(--ink);font-size:12px}
.emp-role-sm{font-size:11px;color:var(--ink3)}
.risk-pill{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;padding:2px 8px;border-radius:100px;white-space:nowrap}
.risk-high{background:var(--terra-light);color:var(--terra)}
.risk-med{background:var(--amber-light);color:var(--amber)}
.risk-low{background:var(--green-light);color:var(--green)}
.idx-bar-wrap{display:flex;align-items:center;gap:6px}
.idx-bar{height:5px;width:60px;background:var(--bg);border-radius:100px;overflow:hidden;display:inline-block}
.idx-bar-fill{height:100%;border-radius:100px}
/* ── EMPLOYEE DETAIL ── */
.emp-detail-hdr{display:flex;align-items:center;gap:20px;padding:24px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);margin-bottom:16px;box-shadow:var(--shadow-sm);flex-wrap:wrap}
.emp-detail-av{width:64px;height:64px;border-radius:50%;color:#fff;font-size:22px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.emp-detail-info{flex:1;min-width:180px}
.emp-detail-name{font-size:22px;font-weight:600;color:var(--ink);letter-spacing:-.02em;margin-bottom:3px}
.emp-detail-role{font-size:13px;color:var(--ink3);margin-bottom:10px}
.emp-meta-chips{display:flex;gap:8px;flex-wrap:wrap}
.emp-meta-chip{font-size:11px;padding:3px 10px;border-radius:100px;background:var(--bg);border:1px solid var(--border-md);color:var(--ink2)}
.emp-idx-big{text-align:right;flex-shrink:0}
.emp-idx-num{font-size:48px;font-weight:300;letter-spacing:-.04em;line-height:1}
.emp-idx-sub{font-size:11px;color:var(--ink3);margin-top:2px}
.emp-charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
@media(max-width:860px){.emp-charts-grid{grid-template-columns:1fr}}
.chart-canvas-box{position:relative}
/* ── DEMO BANNER ── */
.demo-bar{background:linear-gradient(90deg,#0F172A 0%,#1E3A5F 50%,#1d4ed8 100%);color:#fff;padding:8px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.demo-bar-label{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;opacity:.7}
.demo-bar-title{font-size:13px;font-weight:600;flex:1}
.demo-emp-sel{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);color:#fff;padding:5px 10px;border-radius:6px;font-size:12px;cursor:pointer;font-family:'Inter',sans-serif}
.demo-emp-sel option{color:#0F172A;background:#fff}
.demo-bar-pill{font-size:10px;padding:3px 10px;border-radius:100px;border:1px solid rgba(255,255,255,.3);color:rgba(255,255,255,.8);font-family:'JetBrains Mono',monospace;letter-spacing:.04em}
/* ── KPI HOVER ── */
.kpi-card{transition:transform 150ms,box-shadow 150ms}
.kpi-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
/* ── RADAR LEGEND ── */
.radar-legend{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;justify-content:center}
.radar-litem{font-size:10px;color:var(--ink3);display:flex;align-items:center;gap:4px}
.radar-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
/* ── SIGNAL ITEM ── */
.sig-item{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:var(--r);margin-bottom:6px}
.sig-red{background:var(--terra-light)}
.sig-amber{background:var(--amber-light)}
.sig-green{background:var(--green-light)}
.sig-icon{font-size:16px;flex-shrink:0}
.sig-text{font-size:12px;font-weight:500;color:var(--ink2)}
/* ── BACK BTN ── */
.back-btn{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--ink3);cursor:pointer;margin-bottom:16px;padding:6px 12px;border:1px solid var(--border-md);border-radius:var(--r);background:var(--surface);transition:all 120ms}
.back-btn:hover{color:var(--cobalt);border-color:var(--cobalt);background:var(--cobalt-light)}
"""
src=src.replace('</style>',NEW_CSS+'\n</style>',1)

# 3. Demo banner in HTML (before topbar)
DEMO_BAR="""<div class="demo-bar" id="demo-bar">
  <span class="demo-bar-pill">🎯 DEMO</span>
  <span class="demo-bar-title">BURNOFF-AI — Plataforma de Prevención Predictiva de Burnout</span>
  <label style="font-size:11px;color:rgba(255,255,255,.7);white-space:nowrap">Vista empleado:</label>
  <select class="demo-emp-sel" id="demo-emp-sel" onchange="switchDemoEmployee(this.value)"></select>
</div>
"""
src=src.replace('<div class="topbar">', DEMO_BAR+'<div class="topbar">')

with open('BURNOFF_V0.html','w',encoding='utf-8') as f:
    f.write(src)
print("Part 1 done. Lines:",src.count('\n'))
