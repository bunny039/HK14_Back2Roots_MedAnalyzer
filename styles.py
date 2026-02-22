"""
styles.py — MediAssist Design System v5.1
iOS 26 Dark Liquid Glass + Professional AI Chat UI
"""

MAIN_CSS = """
<style>

/* ═══════════════════════════════════════════════════════════════════
   0. FONTS
   ═══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════════════════════════════
   1. DESIGN TOKENS
   ═══════════════════════════════════════════════════════════════════ */
:root {
    /* Canvas */
    --bg-base:   #000000;
    --bg-canvas: linear-gradient(145deg, #020810 0%, #030a18 45%, #04091a 100%);

    /* Glass fills */
    --glass-01: rgba(255,255,255,0.04);
    --glass-02: rgba(255,255,255,0.07);
    --glass-03: rgba(255,255,255,0.10);
    --glass-04: rgba(255,255,255,0.14);
    --glass-sidebar: rgba(12,20,40,0.85);

    /* Blur */
    --blur-sm: blur(16px) saturate(180%);
    --blur-md: blur(28px) saturate(200%);
    --blur-lg: blur(40px) saturate(220%);

    /* Borders */
    --border-dim:    rgba(255,255,255,0.06);
    --border-mid:    rgba(255,255,255,0.11);
    --border-bright: rgba(255,255,255,0.18);

    /* Specular rim */
    --rim-top:    rgba(255,255,255,0.18);
    --rim-strong: rgba(255,255,255,0.30);

    /* Typography */
    --text-primary:   #f2f4f7;
    --text-secondary: #a0aec0;
    --text-tertiary:  #4e6070;
    --text-inverse:   #ffffff;

    /* iOS Tints */
    --blue:    #0A84FF;
    --indigo:  #5E5CE6;
    --teal:    #32D2E0;
    --green:   #30D158;
    --orange:  #FF9F0A;
    --red:     #FF453A;
    --yellow:  #FFD60A;

    /* Semantic fills */
    --fill-blue:   rgba(10,132,255,0.16);
    --fill-green:  rgba(48,209,88,0.14);
    --fill-red:    rgba(255,69,58,0.14);
    --fill-orange: rgba(255,159,10,0.14);
    --fill-teal:   rgba(50,210,224,0.12);

    /* Chat specific */
    --chat-bg:          rgba(8,14,30,0.96);
    --chat-surface:     rgba(255,255,255,0.05);
    --chat-user-bubble: linear-gradient(135deg,#0A84FF 0%,#0055d4 100%);
    --chat-ai-bubble:   rgba(255,255,255,0.07);
    --chat-input-bg:    rgba(255,255,255,0.06);
    --chat-border:      rgba(255,255,255,0.09);

    /* Radii */
    --r-xs:   8px;
    --r-sm:   12px;
    --r-md:   16px;
    --r-lg:   22px;
    --r-xl:   28px;
    --r-pill: 9999px;

    /* Shadows */
    --shadow-sm:  0 2px 8px  rgba(0,0,0,0.50), 0 1px 3px  rgba(0,0,0,0.40);
    --shadow-md:  0 8px 28px rgba(0,0,0,0.60), 0 2px 8px  rgba(0,0,0,0.45);
    --shadow-lg:  0 20px 56px rgba(0,0,0,0.70),0 4px 16px rgba(0,0,0,0.50);
    --shadow-glow-blue:  0 0 20px rgba(10,132,255,0.28);
    --shadow-glow-green: 0 0 16px rgba(48,209,88,0.25);
    --shadow-glow-red:   0 0 16px rgba(255,69,58,0.25);

    --spring: cubic-bezier(0.34,1.56,0.64,1);
    --ease:   cubic-bezier(0.22,1,0.36,1);
}

/* ═══════════════════════════════════════════════════════════════════
   2. GLOBAL RESET & CANVAS
   ═══════════════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"],
p, span, div, label, li, a, button {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont,
                 'SF Pro Text','Helvetica Neue', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html, body { background: #000 !important; }

.stApp {
    background: var(--bg-canvas) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
    color: var(--text-primary) !important;
}

/* Ambient orbs */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 15% 10%,  rgba(10,132,255,0.09)  0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 88% 75%,  rgba(94,92,230,0.07)   0%, transparent 60%),
        radial-gradient(ellipse 45% 45% at 52% 52%,  rgba(48,209,88,0.04)   0%, transparent 70%);
    pointer-events: none; z-index: 0;
}

.main .block-container,
section.main .block-container {
    padding: 28px 36px 60px !important;
    max-width: 1440px !important;
    position: relative; z-index: 1;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
p, span, div, li { color: var(--text-primary); }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.12);
    border-radius: var(--r-pill);
}
::-webkit-scrollbar-thumb:hover { background: rgba(10,132,255,0.50); }

/* ═══════════════════════════════════════════════════════════════════
   3. SIDEBAR
   ═══════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--glass-sidebar) !important;
    backdrop-filter: var(--blur-lg) !important;
    -webkit-backdrop-filter: var(--blur-lg) !important;
    border-right: 1px solid var(--border-mid) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.60),
                inset -1px 0 0 rgba(255,255,255,0.06) !important;
}

[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] .block-container { padding: 0 !important; }

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span:not(.badge):not(.card-badge),
[data-testid="stSidebar"] .stMarkdown { color: var(--text-secondary) !important; }

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--text-primary) !important;
    border-radius: var(--r-sm) !important;
    font-size: 13px !important;
    backdrop-filter: blur(8px) !important;
}

[data-testid="stSidebar"] label {
    color: var(--text-tertiary) !important;
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 0.08em; text-transform: uppercase;
}

/* Brand Block */
.brand-block {
    padding: 28px 20px 22px;
    border-bottom: 1px solid var(--border-dim);
    background: linear-gradient(160deg,rgba(10,132,255,0.10) 0%,rgba(94,92,230,0.06) 60%,transparent 100%);
    position: relative; overflow: hidden;
}
.brand-block::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: var(--rim-top);
}
.brand-icon {
    width: 50px; height: 50px;
    background: linear-gradient(145deg,#1a6ef7 0%,#0055d4 100%);
    border-radius: 15px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; margin-bottom: 12px;
    box-shadow: 0 8px 24px rgba(10,132,255,0.40),
                0 2px 6px rgba(0,0,0,0.50),
                inset 0 1px 0 rgba(255,255,255,0.25);
}
.brand-name {
    font-family: 'DM Serif Display',serif !important;
    font-size: 21px; font-weight: 400;
    color: var(--text-primary) !important;
    line-height: 1.1; margin-bottom: 4px; letter-spacing: -0.3px;
}
.brand-tagline {
    font-size: 11px; color: var(--text-tertiary) !important;
    letter-spacing: 0.08em; text-transform: uppercase; font-weight: 500;
}

/* Nav */
.nav-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--text-tertiary) !important;
    padding: 16px 20px 6px;
}

[data-testid="stSidebar"] .stButton > button {
    width: calc(100% - 16px) !important; text-align: left !important;
    background: transparent !important; border: 1px solid transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--r-md) !important; padding: 10px 14px !important;
    font-size: 13px !important; font-weight: 500 !important;
    transition: all 0.2s var(--spring) !important; margin: 2px 8px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--glass-02) !important; border-color: var(--border-mid) !important;
    color: var(--text-primary) !important; transform: scale(1.01) !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(10,132,255,0.15) !important;
    border-color: rgba(10,132,255,0.35) !important;
    color: var(--blue) !important; font-weight: 700 !important;
    box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(255,255,255,0.10),
                var(--shadow-glow-blue) !important;
}

/* Pipeline */
.pipeline-container {
    padding: 16px; margin: 10px 12px;
    background: var(--glass-02); border: 1px solid var(--border-dim);
    border-radius: var(--r-lg); backdrop-filter: var(--blur-sm); position: relative;
}
.pipeline-container::before {
    content: ''; position: absolute;
    top: 0; left: 10px; right: 10px; height: 1px; background: var(--rim-top);
}
.pipeline-title {
    font-size: 9px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--text-tertiary) !important; margin-bottom: 12px;
}
.pipeline-step { display: flex; align-items: center; gap: 10px; padding: 4px 0; }
.pipeline-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; background: rgba(255,255,255,0.12); }
.pipeline-dot.done   { background: var(--green); box-shadow: var(--shadow-glow-green); }
.pipeline-dot.active { background: var(--blue);  box-shadow: var(--shadow-glow-blue); animation: lg-pulse 1.6s ease-in-out infinite; }
.pipeline-connector { width: 1px; height: 11px; background: var(--border-dim); margin-left: 3.5px; }
.pipeline-step-label { font-size: 11px; color: var(--text-tertiary) !important; }
.pipeline-step-label.done   { color: var(--text-secondary) !important; font-weight: 600; }
.pipeline-step-label.active { color: var(--blue) !important; font-weight: 700; }

@keyframes lg-pulse {
    0%,100% { opacity:1;  box-shadow:0 0 8px  rgba(10,132,255,0.80); }
    50%      { opacity:.5; box-shadow:0 0 16px rgba(10,132,255,0.35); }
}

/* ═══════════════════════════════════════════════════════════════════
   4. PAGE HEADERS
   ═══════════════════════════════════════════════════════════════════ */
.page-header { padding-bottom: 20px; margin-bottom: 24px; border-bottom: 1px solid var(--border-dim); }
.page-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--blue); margin-bottom: 6px; }
.page-title { font-family: 'DM Serif Display',serif !important; font-size: 34px; font-weight: 400; color: var(--text-primary); line-height: 1.1; margin-bottom: 6px; letter-spacing: -0.5px; }
.page-subtitle { font-size: 14px; color: var(--text-secondary); font-weight: 400; line-height: 1.6; max-width: 560px; }

/* ═══════════════════════════════════════════════════════════════════
   5. STAGE BAR
   ═══════════════════════════════════════════════════════════════════ */
.stage-bar {
    display: flex; align-items: center;
    background: var(--glass-02); backdrop-filter: var(--blur-md);
    -webkit-backdrop-filter: var(--blur-md);
    border: 1px solid var(--border-mid); border-radius: var(--r-xl);
    padding: 12px 20px; margin-bottom: 24px; overflow-x: auto;
    box-shadow: var(--shadow-md), inset 0 1px 0 var(--rim-top); position: relative;
}
.stage-bar::before {
    content: ''; position: absolute; top: 0; left: 16px; right: 16px; height: 1px;
    background: var(--rim-strong); border-radius: var(--r-pill); pointer-events: none;
}
.stage-item { display: flex; flex-direction: column; align-items: center; gap: 5px; flex: 1; min-width: 68px; }
.stage-icon {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 13px;
    background: rgba(255,255,255,0.04); color: var(--text-tertiary);
    border: 1px solid var(--border-dim); transition: all 0.3s var(--ease);
}
.stage-icon.done   { background: var(--fill-green); color: var(--green); border-color: rgba(48,209,88,0.40); box-shadow: var(--shadow-glow-green); }
.stage-icon.active { background: var(--fill-blue);  color: var(--blue);  border-color: rgba(10,132,255,0.50); animation: stage-glow 2s var(--ease) infinite; }
.stage-label { font-size: 9px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-tertiary); text-align: center; }
.stage-label.done   { color: var(--green); }
.stage-label.active { color: var(--blue);  }
.stage-connector { flex: 1; height: 1px; background: var(--border-dim); margin-bottom: 18px; }
.stage-connector.done { background: linear-gradient(90deg,rgba(48,209,88,.55),rgba(48,209,88,.15)); }

@keyframes stage-glow {
    0%,100% { box-shadow:0 0 0 3px rgba(10,132,255,.18),0 0 14px rgba(10,132,255,.35); }
    50%      { box-shadow:0 0 0 5px rgba(10,132,255,.10),0 0 26px rgba(10,132,255,.55); }
}

/* ═══════════════════════════════════════════════════════════════════
   6. HERO CARD
   ═══════════════════════════════════════════════════════════════════ */
.hero-card {
    position: relative; padding: 34px 38px 30px; border-radius: var(--r-xl);
    background: var(--glass-04); backdrop-filter: var(--blur-lg);
    -webkit-backdrop-filter: var(--blur-lg);
    border: 1px solid var(--border-bright);
    box-shadow: var(--shadow-lg), inset 0 1px 0 var(--rim-strong);
    margin-bottom: 24px; overflow: hidden;
}
.hero-card::before {
    content: ''; position: absolute; top: 0; left: 24px; right: 24px; height: 1px;
    background: var(--rim-strong); border-radius: var(--r-pill);
}
.hero-card::after {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle,rgba(10,132,255,.14) 0%,transparent 70%);
    border-radius: 50%; pointer-events: none;
}
.hero-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--blue); margin-bottom: 8px; position: relative; z-index: 1; }
.hero-heading  { font-family: 'DM Serif Display',serif !important; font-size: 30px; font-weight: 400; color: var(--text-primary); line-height: 1.15; margin-bottom: 10px; letter-spacing: -0.4px; position: relative; z-index: 1; }
.hero-description { font-size: 14px; color: var(--text-secondary); line-height: 1.7; max-width: 580px; margin-bottom: 26px; position: relative; z-index: 1; }
.hero-stats { display: flex; gap: 12px; flex-wrap: wrap; position: relative; z-index: 1; }
.hero-stat {
    background: var(--glass-02); border: 1px solid var(--border-mid);
    border-radius: var(--r-lg); padding: 14px 20px; flex: 1; min-width: 110px;
    text-align: center;
    box-shadow: var(--shadow-sm), inset 0 1px 0 var(--rim-top);
    transition: transform 0.3s var(--spring), box-shadow 0.3s var(--ease);
    cursor: default; position: relative; overflow: hidden;
}
.hero-stat::before { content:''; position:absolute; top:0; left:8px; right:8px; height:1px; background:var(--rim-top); }
.hero-stat:hover   { transform: translateY(-4px) scale(1.03); box-shadow: var(--shadow-md), inset 0 1px 0 var(--rim-strong); }
.hero-stat.danger  { border-color: rgba(255,69,58,.35);  background: rgba(255,69,58,.10); }
.hero-stat.warning { border-color: rgba(255,159,10,.30); background: rgba(255,159,10,.08); }
.hero-stat.success { border-color: rgba(48,209,88,.30);  background: rgba(48,209,88,.08); }
.hero-stat-value   { font-family:'DM Serif Display',serif !important; font-size: 28px; font-weight: 400; color: var(--text-primary); line-height: 1.1; margin-bottom: 5px; }
.hero-stat.danger  .hero-stat-value { color: var(--red);    }
.hero-stat.warning .hero-stat-value { color: var(--orange); }
.hero-stat.success .hero-stat-value { color: var(--green);  }
.hero-stat-label { font-size: 11px; color: var(--text-tertiary); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }

/* ═══════════════════════════════════════════════════════════════════
   7. GLASS CARDS
   ═══════════════════════════════════════════════════════════════════ */
.card {
    background: var(--glass-02); backdrop-filter: var(--blur-md);
    -webkit-backdrop-filter: var(--blur-md);
    border: 1px solid var(--border-mid); border-radius: var(--r-xl);
    margin-bottom: 20px; overflow: hidden;
    box-shadow: var(--shadow-md), inset 0 1px 0 var(--rim-top);
    transition: transform 0.3s var(--spring), box-shadow 0.3s var(--ease);
    position: relative;
}
.card::before { content:''; position:absolute; top:0; left:12px; right:12px; height:1px; background:var(--rim-top); pointer-events:none; }
.card:hover   { transform: translateY(-4px); box-shadow: var(--shadow-lg), inset 0 1px 0 var(--rim-strong); }
.card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 22px 13px; border-bottom: 1px solid var(--border-dim);
    background: linear-gradient(180deg,rgba(255,255,255,.04) 0%,transparent 100%);
}
.card-title { font-size: 15px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.1px; }
.card-badge { display:inline-flex; align-items:center; padding:4px 12px; border-radius:var(--r-pill); font-size:10px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; background:var(--fill-blue); border:1px solid rgba(10,132,255,.30); color:var(--blue); backdrop-filter:blur(6px); }
.card-badge.success { background:var(--fill-green);  border-color:rgba(48,209,88,.30);  color:var(--green);  }
.card-badge.warning { background:var(--fill-orange); border-color:rgba(255,159,10,.30); color:var(--orange); }
.card-badge.danger  { background:var(--fill-red);    border-color:rgba(255,69,58,.30);  color:var(--red);    }

/* ═══════════════════════════════════════════════════════════════════
   8. LAB TABLE  (v5.1 + fix patch + numeric alignment)
   ═══════════════════════════════════════════════════════════════════ */
.lab-table-wrap { overflow-x: auto; padding: 2px 4px 8px; }
.lab-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 2px;
    font-size: 13px;
    table-layout: fixed;
    color: #e2e8f0;
}
.lab-table thead th {
    padding: 10px 14px 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .10em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    border-bottom: 1px solid var(--border-dim);
    white-space: nowrap;
    background: transparent;
    text-align: left;
}
.lab-table thead th:nth-child(1) { width: 32%; }
.lab-table thead th:nth-child(2) { width: 13%; }
.lab-table thead th:nth-child(3) { width: 11%; }
.lab-table thead th:nth-child(4) { width: 22%; }
.lab-table thead th:nth-child(5) { width: 22%; }
.lab-table tbody tr { transition: background 0.15s ease; }
.lab-table td {
    padding: 14px 12px;
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,.05);
    vertical-align: middle;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.lab-table tbody tr:last-child td { border-bottom: none; }
.lab-table tbody tr:hover td,
.lab-table tr:hover { background: rgba(255,255,255,.04); }

/* Cell variants */
.test-name-cell {
    font-weight: 600;
    color: var(--text-primary) !important;
    font-size: 13.5px;
}
.value-cell { font-size: 14px; font-weight: 700; color: var(--text-primary) !important; }
.unit-cell  { font-size: 12px; color: var(--text-tertiary); }
.ref-cell   { font-size: 12px; color: var(--text-secondary); font-family: 'JetBrains Mono', monospace !important; }
.status-cell { white-space: nowrap; }

/* ── Numeric column alignment (clinical dashboard style) ────────── */
.lab-table td:nth-child(2),
.lab-table th:nth-child(2) { text-align: right; padding-right: 20px; }

.lab-table td:nth-child(3),
.lab-table th:nth-child(3) { text-align: right; padding-right: 16px; }

/* Status row border accents */
.row-normal td:first-child { border-left: 3px solid var(--green); padding-left: 12px; }
.row-high   td:first-child { border-left: 3px solid var(--red);   padding-left: 12px; }
.row-low    td:first-child { border-left: 3px solid var(--blue);  padding-left: 12px; }

/* ═══════════════════════════════════════════════════════════════════
   9. STATUS BADGES
   ═══════════════════════════════════════════════════════════════════ */
.badge { display:inline-flex; align-items:center; gap:5px; padding:4px 12px; border-radius:var(--r-pill); font-size:11px; font-weight:700; letter-spacing:.04em; backdrop-filter:blur(8px); }
.badge-normal  { background:var(--fill-green);  color:var(--green);            border:1px solid rgba(48,209,88,.35); }
.badge-high    { background:var(--fill-red);    color:var(--red);              border:1px solid rgba(255,69,58,.35); }
.badge-low     { background:var(--fill-blue);   color:var(--blue);             border:1px solid rgba(10,132,255,.30); }
.badge-unknown { background:rgba(255,255,255,.06); color:var(--text-tertiary); border:1px solid var(--border-dim); }

/* ═══════════════════════════════════════════════════════════════════
   10. RISK BARS
   ═══════════════════════════════════════════════════════════════════ */
.risk-body { padding: 4px 0; }
.risk-row { display:flex; align-items:center; gap:14px; padding:13px 22px; border-bottom:1px solid rgba(255,255,255,.04); transition:background .18s ease; }
.risk-row:last-child { border-bottom: none; }
.risk-row:hover { background: rgba(255,255,255,.03); border-radius: var(--r-md); }
.risk-info { flex: 0 0 190px; }
.risk-name { font-size:13px; font-weight:600; color:var(--text-primary); margin-bottom:2px; }
.risk-sub  { font-size:11px; color:var(--text-tertiary); }
.risk-track { flex:1; height:7px; background:rgba(255,255,255,.06); border-radius:var(--r-pill); overflow:hidden; }
.risk-fill  { height:100%; border-radius:var(--r-pill); transition:width .85s var(--ease); }
.risk-fill.low    { background: linear-gradient(90deg,#30D158,#34C759); }
.risk-fill.medium { background: linear-gradient(90deg,#FF9F0A,#FFD60A); box-shadow:0 0 8px rgba(255,159,10,.40); }
.risk-fill.high   { background: linear-gradient(90deg,#FF453A,#FF6961); box-shadow:0 0 8px rgba(255,69,58,.50); }
.risk-pct { font-size:13px; font-weight:700; min-width:40px; text-align:right; }
.risk-pct.low    { color: var(--green);  }
.risk-pct.medium { color: var(--orange); }
.risk-pct.high   { color: var(--red);    }

/* ═══════════════════════════════════════════════════════════════════
   11. ✦ PROFESSIONAL AI CHATBOT
   ═══════════════════════════════════════════════════════════════════ */
.chat-shell {
    display: flex; flex-direction: column; height: 680px;
    background: var(--chat-bg); border: 1px solid var(--chat-border);
    border-radius: var(--r-xl); overflow: hidden;
    box-shadow: var(--shadow-lg), inset 0 1px 0 var(--rim-top); position: relative;
}
.chat-shell::before {
    content: ''; position: absolute; top: 0; left: 16px; right: 16px; height: 1px;
    background: var(--rim-strong); border-radius: var(--r-pill); z-index: 10;
}
.chat-topbar {
    display: flex; align-items: center; gap: 14px; padding: 16px 20px;
    background: rgba(255,255,255,0.05); border-bottom: 1px solid var(--chat-border);
    backdrop-filter: blur(20px); flex-shrink: 0; position: relative; z-index: 5;
}
.chat-topbar-left { display: flex; align-items: center; gap: 12px; flex: 1; }
.chat-ai-avatar {
    width: 42px; height: 42px; background: linear-gradient(145deg,#1a7ffc,#0055d4);
    border-radius: 14px; display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(10,132,255,0.50), inset 0 1px 0 rgba(255,255,255,0.25);
    position: relative;
}
.chat-ai-avatar::after {
    content: ''; position: absolute; inset: -3px; border-radius: 17px;
    border: 2px solid rgba(10,132,255,0.40); animation: avatar-ring 3s ease-in-out infinite;
}
@keyframes avatar-ring {
    0%,100% { border-color: rgba(10,132,255,0.40); box-shadow: 0 0 0 0 rgba(10,132,255,0.15); }
    50%      { border-color: rgba(10,132,255,0.70); box-shadow: 0 0 0 5px rgba(10,132,255,0.05); }
}
.chat-ai-info { display: flex; flex-direction: column; gap: 2px; }
.chat-ai-name  { font-size: 15px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.1px; }
.chat-ai-status { display: flex; align-items: center; gap: 5px; font-size: 11px; color: var(--green); font-weight: 500; }
.chat-ai-status::before {
    content: ''; width: 6px; height: 6px; background: var(--green);
    border-radius: 50%; box-shadow: 0 0 6px rgba(48,209,88,.70);
    animation: status-blink 2.5s ease-in-out infinite;
}
@keyframes status-blink {
    0%,100% { box-shadow: 0 0 4px rgba(48,209,88,.60); opacity:1; }
    50%      { box-shadow: 0 0 10px rgba(48,209,88,.90); opacity:.7; }
}
.chat-topbar-right { display: flex; align-items: center; gap: 10px; }
.chat-context-pill {
    display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px;
    border-radius: var(--r-pill); background: var(--fill-blue);
    border: 1px solid rgba(10,132,255,.30); font-size: 11px; font-weight: 600; color: var(--blue);
}
.chat-context-pill.active { background: var(--fill-green); border-color: rgba(48,209,88,.30); color: var(--green); }
.chat-viewport {
    flex: 1; overflow-y: auto; padding: 20px 20px 10px;
    display: flex; flex-direction: column; gap: 16px; scroll-behavior: smooth;
}
.chat-viewport::-webkit-scrollbar { width: 4px; }
.chat-viewport::-webkit-scrollbar-track { background: transparent; }
.chat-viewport::-webkit-scrollbar-thumb { background: rgba(255,255,255,.10); border-radius:4px; }
.chat-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 4px 0; color: var(--text-tertiary); font-size: 11px; font-weight: 600;
}
.chat-divider::before, .chat-divider::after { content: ''; flex: 1; height: 1px; background: var(--border-dim); }
.chat-row { display: flex; gap: 10px; align-items: flex-end; animation: msg-in 0.28s var(--ease) both; }
@keyframes msg-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-row.user-row { flex-direction: row-reverse; }
.row-avatar { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.row-avatar.ai   { background: linear-gradient(145deg,#1a7ffc,#0055d4); box-shadow:0 2px 8px rgba(10,132,255,.45); }
.row-avatar.user { background: rgba(255,255,255,.10); border:1px solid var(--border-mid); }
.chat-bubble-wrap { display: flex; flex-direction: column; gap: 4px; max-width: 80%; }
.user-row .chat-bubble-wrap { align-items: flex-end; }
.chat-sender { font-size: 10px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-tertiary); padding: 0 4px; }
.chat-bubble { padding: 13px 16px; border-radius: 18px; font-size: 14px; line-height: 1.65; color: var(--text-primary); position: relative; word-break: break-word; }
.chat-bubble.ai-bubble {
    background: var(--chat-ai-bubble); border: 1px solid var(--chat-border);
    border-bottom-left-radius: 6px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,.06);
    backdrop-filter: blur(12px);
}
.chat-bubble.user-bubble {
    background: var(--chat-user-bubble); border-bottom-right-radius: 6px;
    box-shadow: 0 6px 20px rgba(10,132,255,0.30), inset 0 1px 0 rgba(255,255,255,0.20);
    color: #ffffff;
}
.chat-meta { display: flex; align-items: center; gap: 6px; font-size: 10px; color: var(--text-tertiary); padding: 0 4px; }
.user-row .chat-meta { justify-content: flex-end; }
.chat-tick { color: var(--blue); font-size: 11px; }
.chat-typing {
    display: flex; align-items: center; gap: 10px; padding: 10px 16px;
    background: var(--chat-ai-bubble); border: 1px solid var(--chat-border);
    border-radius: 18px; border-bottom-left-radius: 6px;
    width: fit-content; box-shadow: 0 4px 12px rgba(0,0,0,.30);
}
.typing-label { font-size: 11px; color: var(--text-tertiary); }
.typing-dots { display: flex; gap: 5px; }
.typing-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--blue); opacity: 0.5; animation: dot-bounce 1.4s ease-in-out infinite; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce {
    0%,80%,100% { transform: translateY(0);    opacity: 0.5; }
    40%          { transform: translateY(-6px); opacity: 1.0; }
}
.chip-bar { padding: 10px 20px 14px; display: flex; flex-wrap: wrap; gap: 8px; border-top: 1px solid var(--border-dim); background: rgba(8,14,30,0.60); flex-shrink: 0; }
.chat-chip {
    display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px;
    border-radius: var(--r-pill); background: var(--glass-02); border: 1px solid var(--border-mid);
    color: var(--text-secondary); font-size: 12px; font-weight: 500;
    cursor: pointer; transition: all 0.2s var(--spring); white-space: nowrap; user-select: none;
}
.chat-chip:hover { background: var(--fill-blue); border-color: rgba(10,132,255,.35); color: var(--blue); transform: translateY(-2px); box-shadow: 0 4px 14px rgba(10,132,255,.20); }
.chat-inputbar { padding: 12px 16px; background: rgba(8,14,30,0.80); border-top: 1px solid var(--chat-border); backdrop-filter: blur(20px); flex-shrink: 0; }
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.07) !important; backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.14) !important; border-radius: var(--r-xl) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 0 0 0 transparent !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(10,132,255,0.50) !important;
    box-shadow: 0 0 0 4px rgba(10,132,255,0.12), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
[data-testid="stChatInput"] textarea { color: var(--text-primary) !important; font-size: 14px !important; background: transparent !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-tertiary) !important; }
.chat-input-hint { font-size: 10px; color: var(--text-tertiary); text-align: center; margin-top: 6px; letter-spacing: 0.04em; }
.ai-card { background: rgba(255,255,255,.06); border: 1px solid var(--border-dim); border-radius: var(--r-md); padding: 12px 14px; margin-top: 8px; font-size: 13px; }
.ai-card-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em; color: var(--text-tertiary); margin-bottom: 8px; }
.ai-card-row { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,.04); font-size: 12px; }
.ai-card-row:last-child { border-bottom: none; }
.ai-card-key   { color: var(--text-secondary); }
.ai-card-value { font-weight: 600; color: var(--text-primary); }
div[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 0 !important; margin: 0 !important; box-shadow: none !important; }
div[data-testid="stChatMessage"] p { color: var(--text-primary) !important; }
.chat-empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 40px; }
.chat-empty-icon { width: 64px; height: 64px; background: linear-gradient(145deg,#1a7ffc,#0055d4); border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 8px 28px rgba(10,132,255,.40), inset 0 1px 0 rgba(255,255,255,.25); }
.chat-empty-title { font-size: 18px; font-weight: 700; color: var(--text-primary); }
.chat-empty-sub   { font-size: 13px; color: var(--text-tertiary); text-align: center; max-width: 280px; line-height: 1.6; }
.qa-grid { display: flex; flex-direction: column; gap: 8px; width: 100%; max-width: 380px; }
.qa-btn { display: flex; align-items: center; gap: 10px; padding: 11px 16px; border-radius: var(--r-md); background: var(--glass-02); border: 1px solid var(--border-mid); color: var(--text-secondary); font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s var(--spring); text-align: left; }
.qa-btn:hover { background: var(--fill-blue); border-color: rgba(10,132,255,.35); color: var(--blue); transform: translateX(4px); box-shadow: var(--shadow-glow-blue); }
.qa-icon { font-size: 16px; flex-shrink: 0; }

/* ═══════════════════════════════════════════════════════════════════
   12. UPLOAD ZONE
   ═══════════════════════════════════════════════════════════════════ */
.upload-hint { text-align: center; padding: 44px 20px; border: 2px dashed rgba(10,132,255,.30); border-radius: var(--r-xl); background: var(--glass-01); backdrop-filter: var(--blur-sm); margin-bottom: 16px; transition: all 0.28s var(--spring); }
.upload-hint:hover { border-color: rgba(10,132,255,.60); background: var(--fill-blue); transform: scale(1.01); box-shadow: var(--shadow-glow-blue); }
.upload-hint-icon  { font-size: 44px; margin-bottom: 12px; filter: drop-shadow(0 4px 8px rgba(10,132,255,.35)); }
.upload-hint-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 5px; }
.upload-hint-sub   { font-size: 12px; color: var(--text-tertiary); letter-spacing: 0.04em; }
[data-testid="stFileUploader"] { background: var(--glass-02) !important; backdrop-filter: var(--blur-sm) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--r-lg) !important; padding: 8px !important; }

/* ═══════════════════════════════════════════════════════════════════
   13. FINDINGS & EXPLANATION
   ═══════════════════════════════════════════════════════════════════ */
.finding-item { display:flex; gap:14px; padding:14px 22px; border-bottom:1px solid rgba(255,255,255,.04); transition:background .18s ease; }
.finding-item:last-child { border-bottom: none; }
.finding-item:hover { background: rgba(255,255,255,.03); border-radius: var(--r-md); }
.finding-icon { width:36px; height:36px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0; }
.finding-icon.high   { background:var(--fill-red);   border:1px solid rgba(255,69,58,.30); }
.finding-icon.low    { background:var(--fill-blue);  border:1px solid rgba(10,132,255,.25); }
.finding-icon.normal { background:var(--fill-green); border:1px solid rgba(48,209,88,.25); }
.finding-text { flex: 1; }
.finding-name { font-size:14px; font-weight:700; color:var(--text-primary); margin-bottom:3px; }
.finding-meta { font-size:11px; font-weight:400; color:var(--text-tertiary); margin-left:10px; }
.finding-desc { font-size:13px; color:var(--text-secondary); line-height:1.6; }
.finding-expl { margin-top:6px; font-size:12px; color:var(--text-tertiary); line-height:1.6; background:var(--glass-01); border-radius:var(--r-sm); padding:8px 12px; border:1px solid var(--border-dim); }
.tips-body { padding: 6px 0; }
.tip-row { display:flex; align-items:flex-start; gap:10px; padding:11px 22px; border-bottom:1px solid var(--border-dim); font-size:13px; color:var(--text-secondary); line-height:1.6; }
.tip-row:last-child { border-bottom: none; }
.tip-bullet { color:var(--blue); font-weight:700; flex-shrink:0; margin-top:1px; }

/* ═══════════════════════════════════════════════════════════════════
   14. DISCLAIMER
   ═══════════════════════════════════════════════════════════════════ */
.disclaimer { background: rgba(255,159,10,.08); backdrop-filter: blur(12px); border: 1px solid rgba(255,159,10,.22); border-left: 4px solid var(--orange); border-radius: var(--r-md); padding: 13px 18px; font-size: 12px; color: #e0a050; line-height: 1.6; margin: 16px 0; box-shadow: inset 0 1px 0 rgba(255,255,255,.04); }

/* ═══════════════════════════════════════════════════════════════════
   15. DOCTOR PANEL
   ═══════════════════════════════════════════════════════════════════ */
.doctor-panel { background: rgba(5,10,25,.85); backdrop-filter: var(--blur-sm); border: 1px solid var(--border-mid); border-radius: var(--r-lg); padding: 18px 20px; margin: 0 22px 18px; font-family: 'JetBrains Mono','SF Mono','Courier New',monospace !important; font-size: 12px; color: #7dd3fc; line-height: 1.7; white-space: pre-wrap; word-break: break-all; max-height: 340px; overflow-y: auto; box-shadow: inset 0 1px 0 rgba(255,255,255,.06); }

/* ═══════════════════════════════════════════════════════════════════
   16. EMPTY STATES
   ═══════════════════════════════════════════════════════════════════ */
.empty-state { text-align: center; padding: 44px 20px; }
.empty-icon  { font-size: 38px; margin-bottom: 10px; opacity: .5; }
.empty-title { font-size: 15px; font-weight: 600; color: var(--text-secondary); margin-bottom: 5px; }
.empty-sub   { font-size: 13px; color: var(--text-tertiary); }

/* ═══════════════════════════════════════════════════════════════════
   17. TABLE FOOTER / LEGEND
   ═══════════════════════════════════════════════════════════════════ */
.table-footer { padding:11px 22px 14px; font-size:11px; color:var(--text-tertiary); border-top:1px solid var(--border-dim); display:flex; align-items:center; gap:14px; flex-wrap:wrap; }
.legend-dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:4px; }
.legend-dot.green { background:var(--green); box-shadow:var(--shadow-glow-green); }
.legend-dot.red   { background:var(--red);   box-shadow:var(--shadow-glow-red);   }
.legend-dot.blue  { background:var(--blue);  box-shadow:var(--shadow-glow-blue);  }
.sev-tag { display:inline-block; font-size:10px; padding:2px 8px; border-radius:var(--r-pill); background:var(--glass-02); border:1px solid var(--border-dim); color:var(--text-tertiary); margin-left:8px; vertical-align:middle; }
.section-divider { height:1px; background:linear-gradient(90deg,transparent,rgba(10,132,255,.25) 30%,rgba(94,92,230,.20) 70%,transparent); margin:24px 0; }
.section-eyebrow { font-size:13px; font-weight:700; color:var(--text-secondary); margin-bottom:12px; letter-spacing:.02em; }
.info-pill { display:inline-flex; align-items:center; gap:7px; padding:6px 14px; border-radius:var(--r-pill); background:var(--fill-blue); border:1px solid rgba(10,132,255,.30); color:var(--blue); font-size:12px; font-weight:600; backdrop-filter:blur(8px); box-shadow:inset 0 1px 0 rgba(255,255,255,.08); }

/* ═══════════════════════════════════════════════════════════════════
   18. VERIFIED BANNER
   ═══════════════════════════════════════════════════════════════════ */
.verified-banner { background:rgba(48,209,88,.08); border:1px solid rgba(48,209,88,.28); border-radius:var(--r-lg); padding:16px 22px; margin-bottom:20px; box-shadow:inset 0 1px 0 rgba(255,255,255,.06),var(--shadow-glow-green); }
.verified-title  { font-size:14px; font-weight:700; color:var(--green); margin-bottom:4px; }
.rx-tag { display:inline-flex; align-items:center; padding:4px 12px; border-radius:var(--r-pill); background:rgba(48,209,88,.12); border:1px solid rgba(48,209,88,.28); color:var(--green); font-size:12px; font-weight:600; }

/* ═══════════════════════════════════════════════════════════════════
   19. STREAMLIT OVERRIDES
   ═══════════════════════════════════════════════════════════════════ */
.stButton > button[kind="primary"] {
    background: linear-gradient(145deg,#1a7ffc,#0055d4) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--r-pill) !important; padding: 10px 26px !important;
    font-size: 14px !important; font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(10,132,255,.45), inset 0 1px 0 rgba(255,255,255,.25) !important;
    transition: all 0.25s var(--spring) !important;
}
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) scale(1.03) !important; box-shadow: 0 12px 30px rgba(10,132,255,.60), inset 0 1px 0 rgba(255,255,255,.30) !important; }
.stButton > button[kind="primary"]:active { transform: scale(0.97) !important; }
.stButton > button[kind="secondary"],
.stButton > button:not([kind]) { background: var(--glass-02) !important; backdrop-filter: blur(10px) !important; border: 1px solid var(--border-mid) !important; color: var(--blue) !important; border-radius: var(--r-pill) !important; font-size: 13px !important; font-weight: 600 !important; transition: all 0.2s var(--ease) !important; box-shadow: inset 0 1px 0 var(--rim-top) !important; }
.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind]):hover { background: var(--glass-03) !important; border-color: rgba(10,132,255,.40) !important; transform: translateY(-1px) !important; box-shadow: var(--shadow-glow-blue), inset 0 1px 0 var(--rim-top) !important; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > textarea { background: var(--glass-02) !important; backdrop-filter: blur(8px) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--r-md) !important; color: var(--text-primary) !important; font-size: 14px !important; box-shadow: inset 0 1px 3px rgba(0,0,0,.30) !important; transition: all 0.2s ease !important; }
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > textarea:focus { border-color: rgba(10,132,255,.55) !important; box-shadow: 0 0 0 4px rgba(10,132,255,.15), inset 0 1px 3px rgba(0,0,0,.30) !important; background: var(--glass-03) !important; }
[data-testid="stSelectbox"] > div > div { background: var(--glass-02) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--r-md) !important; color: var(--text-primary) !important; font-size: 13px !important; backdrop-filter: blur(8px) !important; }
label[data-testid="stWidgetLabel"] { color: var(--text-secondary) !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.04em; }
[data-testid="stMetric"] { background: var(--glass-02) !important; backdrop-filter: var(--blur-md) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--r-lg) !important; padding: 14px 18px !important; box-shadow: var(--shadow-md), inset 0 1px 0 var(--rim-top) !important; }
[data-testid="stMetricLabel"] { color:var(--text-tertiary) !important; font-size:10px !important; text-transform:uppercase !important; letter-spacing:.10em !important; font-weight:700 !important; }
[data-testid="stMetricValue"] { font-family:'DM Serif Display',serif !important; font-size:26px !important; color:var(--text-primary) !important; }
[data-testid="stAlert"] { background:var(--glass-02) !important; backdrop-filter:blur(12px) !important; border-radius:var(--r-md) !important; border-left-width:4px !important; font-size:13px !important; box-shadow:inset 0 1px 0 var(--rim-top) !important; }
[data-testid="stExpander"] { background:var(--glass-02) !important; backdrop-filter:var(--blur-sm) !important; border:1px solid var(--border-dim) !important; border-radius:var(--r-lg) !important; margin-bottom:8px !important; box-shadow:inset 0 1px 0 var(--rim-top) !important; }
[data-testid="stExpander"] summary { font-size:13px !important; color:var(--blue) !important; font-weight:600 !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--glass-02) !important; backdrop-filter:var(--blur-md) !important; border-radius:var(--r-lg) !important; border:1px solid var(--border-mid) !important; padding:4px !important; gap:2px !important; box-shadow:inset 0 1px 0 var(--rim-top) !important; }
.stTabs [data-baseweb="tab"] { border-radius:var(--r-md) !important; font-size:13px !important; font-weight:600 !important; padding:8px 18px !important; color:var(--text-secondary) !important; background:transparent !important; border:none !important; transition:all 0.22s var(--spring) !important; }
.stTabs [aria-selected="true"] { background:rgba(10,132,255,.18) !important; color:var(--blue) !important; box-shadow:0 0 14px rgba(10,132,255,.20),inset 0 1px 0 rgba(255,255,255,.10) !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
[data-testid="stDownloadButton"] > button { background:var(--glass-02) !important; border:1px solid var(--border-mid) !important; color:var(--blue) !important; border-radius:var(--r-pill) !important; font-size:12px !important; font-weight:600 !important; backdrop-filter:blur(8px) !important; box-shadow:inset 0 1px 0 var(--rim-top) !important; transition:all .2s ease !important; }
[data-testid="stDownloadButton"] > button:hover { background:var(--glass-03) !important; box-shadow:var(--shadow-glow-blue),inset 0 1px 0 var(--rim-top) !important; transform:translateY(-1px) !important; }
[data-testid="stProgress"] > div > div > div { background:linear-gradient(90deg,var(--blue),var(--green)) !important; border-radius:var(--r-pill) !important; }
[data-testid="stDataFrame"] { background:var(--glass-02) !important; backdrop-filter:var(--blur-sm) !important; border:1px solid var(--border-mid) !important; border-radius:var(--r-lg) !important; overflow:hidden !important; box-shadow:var(--shadow-md) !important; }
[data-testid="stToggle"] label { color:var(--text-secondary) !important; font-size:13px !important; font-weight:500 !important; }

</style>
"""
