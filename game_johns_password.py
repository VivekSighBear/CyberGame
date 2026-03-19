import streamlit as st

def render_game() -> None:
    """Render the Password Cracking Game page with 5 levels of hints about John."""

    # Back to hub (only works when launched from main.py)
    top_left, _, _ = st.columns([2, 6, 2])
    with top_left:
        if st.button("← Back to main menu", use_container_width=True, key="back_to_main_menu"):
            st.session_state.current_page = "landing"
            st.session_state.selected_game = None
            st.rerun()

    # Custom CSS: cyber-game theme (neon + grid + glow)
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@400;600&family=Share+Tech+Mono&display=swap');

        :root{
            --bg0:#050815;
            --bg1:#0b1026;
            --panel:#0e1a2b;
            --panel2:rgba(14,26,43,.72);
            --text:#d7e3ff;
            --muted:#8ea3d1;
            --cyan:#22d3ee;
            --mag:#a855f7;
            --green:#22c55e;
            --red:#fb7185;
            --blue:#3b82f6;
            --border:rgba(34,211,238,.28);
            --shadow: 0 10px 30px rgba(0,0,0,.45);
            --glow: 0 0 18px rgba(34,211,238,.35);
        }

        /* =========================================================
           Visual hierarchy tiers
           Primary   : current level + main action
           Secondary : hints + supporting info
           Tertiary  : navigation/decorative
        ========================================================= */
        .tier-primary{
            border-color: rgba(34,211,238,.55) !important;
            outline: 1px solid rgba(168,85,247,.22) !important;
            box-shadow: 0 22px 70px rgba(0,0,0,.46), 0 0 34px rgba(34,211,238,.16) !important;
        }
        .tier-secondary{
            border-color: rgba(34,211,238,.22) !important;
            outline: 1px solid rgba(168,85,247,.10) !important;
            box-shadow: 0 14px 42px rgba(0,0,0,.34), 0 0 18px rgba(34,211,238,.08) !important;
        }
        .tier-tertiary{
            border-color: rgba(34,211,238,.14) !important;
            outline: 1px solid rgba(168,85,247,.06) !important;
            box-shadow: 0 10px 26px rgba(0,0,0,.26) !important;
            opacity: .92;
        }

        /* Streamlit base containers */
        .stApp, [data-testid="stAppViewContainer"]{
            background: radial-gradient(1200px 700px at 20% 10%, rgba(168,85,247,.18), transparent 55%),
                        radial-gradient(900px 600px at 85% 20%, rgba(34,211,238,.14), transparent 60%),
                        linear-gradient(180deg, var(--bg0), var(--bg1));
            color: var(--text);
            font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        }

        /* Cyber grid + scanlines */
        [data-testid="stAppViewContainer"]::before{
            content:"";
            position: fixed;
            inset: 0;
            pointer-events:none;
            background:
                linear-gradient(to bottom, rgba(255,255,255,.05), rgba(255,255,255,0) 60%),
                repeating-linear-gradient(
                    90deg,
                    rgba(34,211,238,.08) 0px,
                    rgba(34,211,238,.08) 1px,
                    transparent 1px,
                    transparent 80px
                ),
                repeating-linear-gradient(
                    0deg,
                    rgba(34,211,238,.06) 0px,
                    rgba(34,211,238,.06) 1px,
                    transparent 1px,
                    transparent 80px
                );
            mix-blend-mode: screen;
            opacity: .55;
            filter: drop-shadow(0 0 12px rgba(34,211,238,.18));
            animation: gridShift 18s linear infinite;
        }
        [data-testid="stAppViewContainer"]::after{
            content:"";
            position: fixed;
            inset: 0;
            pointer-events:none;
            background: repeating-linear-gradient(
                180deg,
                rgba(255,255,255,.04) 0px,
                rgba(255,255,255,.04) 1px,
                rgba(0,0,0,0) 3px,
                rgba(0,0,0,0) 7px
            );
            opacity:.18;
            animation: scan 7.5s linear infinite;
        }
        @keyframes gridShift{ from{ transform: translateY(0);} to{ transform: translateY(80px);} }
        @keyframes scan{ from{ transform: translateY(-20px);} to{ transform: translateY(20px);} }

        /* Reduce Streamlit default padding slightly for a tighter "HUD" feel */
        section.main > div { padding-top: 1.25rem; }

        /* Remove Streamlit top header bar (black space + Deploy) */
        [data-testid="stHeader"] { display: none; }
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }
        [data-testid="stStatusWidget"] { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        /* Some themes keep reserved top padding; remove it */
        .stApp { padding-top: 0rem; }

        /* Global button system: outlined neon buttons (hub + games) */
        .stButton > button{
            width: 100%;
            background: rgba(15,23,42,.92) !important;
            color: var(--cyan) !important;
            border: 1px solid rgba(34,211,238,.70) !important;
            border-radius: 12px !important;
            padding: 0.9rem 1rem !important;
            font-family: 'Orbitron', system-ui, sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: .06em !important;
            text-transform: uppercase !important;
            box-shadow: 0 14px 34px rgba(0,0,0,.40), 0 0 16px rgba(34,211,238,.18) !important;
            transition: transform .16s ease, box-shadow .16s ease, background .16s ease, border-color .16s ease !important;
        }
        .stButton > button:hover{
            transform: translateY(-2px) scale(1.01) !important;
            background: linear-gradient(135deg, rgba(15,23,42,1), rgba(8,47,73,1)) !important;
            border-color: rgba(56,189,248,.95) !important;
            box-shadow: 0 20px 46px rgba(0,0,0,.55), 0 0 22px rgba(34,211,238,.35), 0 0 18px rgba(168,85,247,.16) !important;
        }
        .stButton > button:active{
            transform: translateY(0px) scale(.995) !important;
        }
        .stButton > button:disabled,
        .stButton > button[disabled]{
            opacity: .55 !important;
            cursor: not-allowed !important;
            box-shadow: none !important;
            transform: none !important;
        }

        /* Section spacing helpers */
        .section-gap-lg{ height: 26px; }
        .section-gap-md{ height: 18px; }
        .section-gap-sm{ height: 10px; }

        /* Sidebar - make it feel like a terminal panel */
        [data-testid="stSidebar"]{
            background: linear-gradient(180deg, rgba(5,8,21,.92), rgba(11,16,38,.92));
            border-right: 1px solid rgba(34,211,238,.18);
        }
        [data-testid="stSidebar"] *{
            color: var(--text);
        }
        [data-testid="stSidebar"] a{
            color: var(--cyan) !important;
        }
        [data-testid="stSidebar"] hr{
            border-color: rgba(34,211,238,.16) !important;
        }
        
        /* Card styling matching reference */
        .info-card {
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.72));
            color: var(--text);
            padding: 20px 15px;
            border-radius: 12px;
            box-shadow: var(--shadow);
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            border: 1px solid var(--border);
            outline: 1px solid rgba(168,85,247,.12);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow), var(--glow);
        }
        
        .definition-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
            color: var(--cyan);
            margin-bottom: 10px;
            text-shadow: 0 0 14px rgba(34,211,238,.25);
        }
        .definition-content{
            color: var(--text);
            opacity: .92;
            text-align: center;
            line-height: 1.5;
        }
        .definition-id{
            margin-top: 10px;
            font-size: 12px;
            color: var(--muted);
            opacity: .9;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px dashed rgba(34,211,238,.22);
            background: rgba(34,211,238,.06);
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, rgba(14,26,43,.95), rgba(14,26,43,.70));
            color: var(--cyan);
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            margin: 30px 0 20px 0;
            border-left: 5px solid var(--cyan);
            box-shadow: var(--shadow);
            text-transform: uppercase;
            letter-spacing: .06em;
            font-family: 'Orbitron', system-ui, sans-serif;
            position: relative;
            overflow: hidden;
        }
        .section-header::after{
            content:"";
            position:absolute;
            inset:0;
            background: linear-gradient(120deg, transparent 35%, rgba(34,211,238,.18), transparent 65%);
            transform: translateX(-120%);
            animation: sheen 6s ease-in-out infinite;
        }
        @keyframes sheen{
            0%, 40% { transform: translateX(-120%); }
            60%, 100% { transform: translateX(120%); }
        }
        
        .subsection-header {
            background: rgba(14,26,43,.72);
            color: #a5b4fc;
            padding: 12px 18px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            margin: 25px 0 15px 0;
            border-left: 4px solid rgba(168,85,247,.75);
            box-shadow: 0 10px 24px rgba(0,0,0,.22);
            font-family: 'Orbitron', system-ui, sans-serif;
            letter-spacing: .04em;
        }
        
        /* Content styling */
        .content-box {
            background: rgba(14,26,43,.75);
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border: 1px solid rgba(34,211,238,.18);
            color: var(--text);
            line-height: 1.6;
            box-shadow: 0 10px 28px rgba(0,0,0,.25);
        }
        
        /* Game hint cards */
        .hint-card {
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.66));
            padding: 25px 20px;
            border-radius: 12px;
            margin: 10px;
            border: 1px solid rgba(34,211,238,.18);
            color: var(--text);
            height: 100%;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }
        .hint-card::before{
            content:"";
            position:absolute;
            inset:-2px;
            background: conic-gradient(from 180deg, rgba(34,211,238,.0), rgba(34,211,238,.35), rgba(168,85,247,.28), rgba(34,211,238,.0));
            opacity:.35;
            filter: blur(12px);
        }
        .hint-card > *{ position: relative; }
        
        .hint-title {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 8px;
            color: var(--muted);
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .hint-content {
            font-size: 18px;
            line-height: 1.5;
            margin-bottom: 12px;
            color: var(--cyan);
            font-weight: bold;
            text-shadow: 0 0 14px rgba(34,211,238,.18);
            font-family: 'Share Tech Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            letter-spacing: .02em;
        }

        /* Main hints container (make hints the focus) */
        .hints-panel{
            background: linear-gradient(180deg, rgba(14,26,43,.86), rgba(5,8,21,.45));
            border: 1px solid rgba(168,85,247,.32);
            outline: 1px solid rgba(34,211,238,.18);
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 18px 50px rgba(0,0,0,.35), 0 0 26px rgba(168,85,247,.10);
            position: relative;
            overflow: hidden;
        }
        .hints-panel::before{
            content:"";
            position:absolute;
            inset:0;
            background:
                radial-gradient(700px 220px at 50% 0%, rgba(168,85,247,.16), transparent 62%),
                linear-gradient(120deg, transparent 25%, rgba(34,211,238,.10), transparent 60%);
            opacity:.95;
            pointer-events:none;
        }
        .hints-panel > *{ position: relative; }
        .hints-panel-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 12px;
            letter-spacing: .14em;
            text-transform: uppercase;
            color: rgba(167,243,255,.88);
            margin: 0 0 10px 0;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px dashed rgba(34,211,238,.22);
            background: rgba(34,211,238,.06);
            display: inline-block;
        }
        .hint-card.primary{
            margin: 0;
            padding: 34px 26px;
            border-width: 2px;
            border-color: rgba(168,85,247,.50);
            outline: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 18px 55px rgba(0,0,0,.34), 0 0 26px rgba(168,85,247,.14);
        }
        .hint-card.primary .hint-content{
            font-size: 24px;
            color: rgba(167,243,255,.98);
            text-shadow: 0 0 18px rgba(34,211,238,.20);
            font-family: 'Share Tech Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            letter-spacing: .02em;
        }
        .hint-card.primary .hint-title{
            color: rgba(215,227,255,.85);
        }

        /* Social-media style quote panel (Level 2) */
        .quote-card{
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.62));
            border: 1px solid rgba(168,85,247,.34);
            outline: 1px solid rgba(34,211,238,.14);
            border-radius: 14px;
            padding: 22px 18px;
            box-shadow: 0 18px 55px rgba(0,0,0,.34), 0 0 26px rgba(168,85,247,.12);
            position: relative;
            overflow: hidden;
        }
        .quote-card::before{
            content:"";
            position:absolute;
            inset:-2px;
            background: conic-gradient(from 180deg, rgba(168,85,247,.0), rgba(168,85,247,.35), rgba(34,211,238,.18), rgba(168,85,247,.0));
            opacity:.28;
            filter: blur(14px);
        }
        .quote-card > *{ position: relative; }
        .quote-header{
            display:flex;
            align-items:center;
            gap:10px;
            margin: 0 0 12px 0;
            opacity: .95;
        }
        .quote-avatar{
            width: 34px;
            height: 34px;
            border-radius: 999px;
            background: radial-gradient(circle at 30% 30%, rgba(34,211,238,.55), rgba(168,85,247,.35));
            border: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 10px 22px rgba(0,0,0,.35), 0 0 18px rgba(34,211,238,.12);
        }
        .quote-handle{
            font-family: 'Share Tech Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            letter-spacing: .04em;
            color: rgba(215,227,255,.88);
            font-size: 12px;
            text-transform: uppercase;
        }
        .quote-line{
            font-family: 'Share Tech Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 20px;
            line-height: 1.55;
            color: rgba(167,243,255,.96);
            text-shadow: 0 0 16px rgba(34,211,238,.14);
            padding: 12px 12px;
            margin: 10px 0;
            border-radius: 12px;
            border: 1px dashed rgba(34,211,238,.20);
            background: rgba(34,211,238,.05);
        }
        .quote-meta{
            margin-top: 10px;
            font-size: 12px;
            color: rgba(142,163,209,.92);
            opacity: .95;
        }

        /* One big container around all hints */
        .hints-master{
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(5,8,21,.42));
            border: 3px solid rgba(34,211,238,.38);
            outline: 1px solid rgba(168,85,247,.28);
            border-radius: 16px;
            padding: 44px;
            margin: 22px 0 34px 0;
            box-shadow: 0 28px 90px rgba(0,0,0,.50), 0 0 44px rgba(34,211,238,.16);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(4px);
            animation: hintsPulse 3.6s ease-in-out infinite;
        }
        .hints-master::before{
            content:"";
            position:absolute;
            inset:0;
            background:
                radial-gradient(900px 240px at 50% 0%, rgba(34,211,238,.14), transparent 62%),
                linear-gradient(120deg, transparent 25%, rgba(168,85,247,.10), transparent 60%);
            opacity:.95;
            pointer-events:none;
        }
        .hints-master > *{ position: relative; }
        .hints-master-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 14px;
            letter-spacing: .16em;
            text-transform: uppercase;
            color: rgba(167,243,255,.92);
            margin: 0 0 6px 0;
        }
        .hints-master-level{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 34px;
            font-weight: 700;
            letter-spacing: .10em;
            text-transform: uppercase;
            margin: 6px 0 2px 0;
            color: rgba(167,243,255,.96);
            text-shadow: 0 0 22px rgba(34,211,238,.20);
        }
        .hints-master-sub{
            color: rgba(215,227,255,.75);
            font-size: 13px;
            margin: 0 0 12px 0;
        }
        .hints-grid{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 26px;
        }
        @media (max-width: 1100px){
            .hints-grid{ grid-template-columns: 1fr; }
        }

        @keyframes hintsPulse{
            0%,100%{
                box-shadow: 0 28px 90px rgba(0,0,0,.50), 0 0 38px rgba(34,211,238,.14);
            }
            50%{
                box-shadow: 0 32px 110px rgba(0,0,0,.56), 0 0 54px rgba(34,211,238,.20);
            }
        }
        
        .hint-id {
            font-size: 12px;
            opacity: 0.7;
            background: rgba(34, 211, 238, 0.08);
            padding: 4px 10px;
            border-radius: 10px;
            margin-top: 8px;
            color: rgba(167, 243, 255, 0.92);
            display: inline-block;
            border: 1px solid rgba(34, 211, 238, 0.18);
        }
        
        .level-badge {
            font-size: 12px;
            opacity: 0.8;
            background: rgba(34, 197, 94, 0.10);
            padding: 4px 10px;
            border-radius: 10px;
            margin-top: 8px;
            color: #a7f3d0;
            display: inline-block;
            border: 1px solid rgba(34, 197, 94, 0.22);
        }
        
        /* Level cards */
        .level-card {
            background: rgba(14,26,43,.72);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: var(--shadow);
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid rgba(34,211,238,.18);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .level-card.compact{
            height: 122px;
            padding: 14px 12px;
        }
        .level-card.tier-tertiary{
            background: rgba(14,26,43,.56);
        }
        .level-card.tier-tertiary .level-number{
            color: rgba(165,180,252,.82);
        }
        .level-card.tier-tertiary .level-status{
            opacity: .68;
        }
        .level-card.tier-tertiary .level-button{
            opacity: .78;
        }
        .level-card::after{
            content:"";
            position:absolute;
            inset:0;
            background: radial-gradient(500px 120px at 50% -10%, rgba(34,211,238,.18), transparent 60%);
            opacity:.7;
            pointer-events:none;
        }
        
        .level-card:hover {
            background: rgba(14,26,43,.86);
            transform: translateY(-3px);
            box-shadow: var(--shadow), var(--glow);
        }
        
        .level-number {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #a5b4fc;
            font-family: 'Orbitron', system-ui, sans-serif;
            letter-spacing: .06em;
        }
        .level-card.compact .level-number{
            font-size: 14px;
            margin-bottom: 6px;
        }
        
        .level-status {
            font-size: 13px;
            opacity: 0.8;
            color: var(--text);
            margin-bottom: 15px;
        }
        .level-card.compact .level-status{
            font-size: 12px;
            margin-bottom: 10px;
        }
        
        .level-button {
            background: rgba(34, 211, 238, 0.10);
            color: rgba(167, 243, 255, 0.92);
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid rgba(34, 211, 238, 0.28);
            transition: all 0.3s ease;
            box-shadow: 0 0 0 rgba(34,211,238,0);
        }
        .level-card.compact .level-button{
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 10px;
        }

        /* Footer */
        .app-footer{
            margin-top: 28px;
            padding: 14px 16px;
            border-radius: 14px;
            text-align: center;
            color: rgba(215,227,255,.72);
            background: rgba(14,26,43,.55);
            border: 1px solid rgba(34,211,238,.18);
            box-shadow: 0 16px 40px rgba(0,0,0,.28);
        }
        
        .level-button:hover {
            background: rgba(34, 211, 238, 0.16);
            box-shadow: 0 0 18px rgba(34,211,238,.18);
        }
        
        /* Progress cards */
        .progress-card {
            background: rgba(14,26,43,.72);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: var(--shadow);
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid rgba(34,211,238,.18);
            position: relative;
            overflow: hidden;
        }
        .progress-card.compact{
            height: 130px;
            padding: 14px 14px;
        }
        .progress-card::before{
            content:"";
            position:absolute;
            inset:0;
            background: radial-gradient(600px 120px at 50% 0%, rgba(168,85,247,.18), transparent 55%);
            opacity:.9;
            pointer-events:none;
        }
        .progress-card > *{ position: relative; }
        
        .progress-label {
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 8px;
            color: var(--muted);
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        
        .progress-value {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 12px;
            color: var(--cyan);
            font-family: 'Orbitron', system-ui, sans-serif;
            text-shadow: 0 0 14px rgba(34,211,238,.18);
        }
        .progress-card.compact .progress-value{
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .progress-description {
            font-size: 14px;
            opacity: 0.8;
            color: var(--text);
            line-height: 1.4;
        }
        .progress-card.compact .progress-description{
            font-size: 12px;
            line-height: 1.35;
        }
        
        .attempt-badge {
            font-size: 11px;
            opacity: 0.7;
            background: rgba(34, 211, 238, 0.08);
            padding: 3px 8px;
            border-radius: 8px;
            margin-top: 10px;
            color: rgba(167, 243, 255, 0.92);
            border: 1px solid rgba(34, 211, 238, 0.18);
        }
        .progress-card.compact .attempt-badge{
            margin-top: 8px;
            font-size: 10px;
        }

        /* Emphasize current level / reduce noise elsewhere */
        .progress-card.tier-primary .progress-value{
            font-size: 18px;
        }
        .progress-card.tier-primary .progress-label{
            color: rgba(167,243,255,.92);
        }
        .progress-card.tier-secondary .progress-value{
            color: rgba(167,243,255,.82);
            text-shadow: none;
        }
        .progress-card.tier-secondary .progress-description{
            opacity: .72;
        }
        
        /* Success message */
        .success-message {
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #a7f3d0;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 0 24px rgba(34,197,94,.12), var(--shadow);
        }

        /* Streamlit widgets (buttons + inputs) */
        div.stButton > button{
            border-radius: 12px !important;
            border: 1px solid rgba(34,211,238,.35) !important;
            color: var(--text) !important;
            background: linear-gradient(180deg, rgba(14,26,43,.88), rgba(5,8,21,.72)) !important;
            box-shadow: 0 14px 34px rgba(0,0,0,.26), 0 0 18px rgba(34,211,238,.10) !important;
            font-family: 'Orbitron', system-ui, sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: .04em !important;
            text-transform: none !important;
            font-size: 15px !important;
            transition: transform .12s ease, box-shadow .18s ease, border-color .18s ease !important;
            height: 60px !important;
            padding: 0 18px !important;
        }
        /* Ensure nested label nodes inherit the button font */
        div.stButton > button *{
            font-family: 'Orbitron', system-ui, sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: .04em !important;
            text-transform: none !important;
        }
        div.stButton > button:hover{
            transform: translateY(-1px);
            border-color: rgba(168,85,247,.55) !important;
            box-shadow: 0 18px 40px rgba(0,0,0,.34), 0 0 24px rgba(168,85,247,.14) !important;
        }
        div.stButton > button:active{
            transform: translateY(0px) scale(.99);
        }
        /* Classy accent strip for buttons */
        div.stButton > button{
            position: relative !important;
            overflow: hidden !important;
        }
        div.stButton > button::before{
            content: "" !important;
            position: absolute !important;
            inset: 0 !important;
            background: linear-gradient(90deg, rgba(34,211,238,.22), rgba(168,85,247,.18), rgba(34,211,238,.22)) !important;
            opacity: .65 !important;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,.0), rgba(0,0,0,.85) 45%, rgba(0,0,0,.0)) !important;
            transform: translateX(-60%) !important;
            transition: transform .35s ease !important;
            pointer-events: none !important;
        }
        div.stButton > button:hover::before{
            transform: translateX(60%) !important;
        }
        div.stButton > button > div{
            position: relative !important;
            z-index: 1 !important;
        }

        /* Primary vs secondary button differentiation */
        div.stButton > button[kind="primary"]{
            border-color: rgba(34,211,238,.55) !important;
            background: linear-gradient(180deg, rgba(34,211,238,.14), rgba(14,26,43,.78)) !important;
            box-shadow: 0 18px 46px rgba(0,0,0,.32), 0 0 26px rgba(34,211,238,.16) !important;
        }
        div.stButton > button[kind="secondary"]{
            border-color: rgba(142,163,209,.26) !important;
        }

        [data-testid="stTextInput"] input{
            border-radius: 12px !important;
            border: 1px solid rgba(34,211,238,.28) !important;
            background: rgba(5,8,21,.55) !important;
            color: var(--text) !important;
            box-shadow: inset 0 0 0 1px rgba(168,85,247,.12), 0 0 0 rgba(34,211,238,0) !important;
        }
        [data-testid="stTextInput"] input:focus{
            border-color: rgba(34,211,238,.55) !important;
            box-shadow: 0 0 0 3px rgba(34,211,238,.12) !important;
        }

        /* Make the main password input feel "primary" (wrapper + input) */
        [data-testid="stTextInput"] div[data-baseweb="input"]{
            height: 60px !important;
            border-radius: 12px !important;
            background: linear-gradient(180deg, rgba(5,8,21,.70), rgba(14,26,43,.55)) !important;
            border: 2px solid rgba(34,211,238,.55) !important;
            box-shadow: 0 0 0 1px rgba(168,85,247,.18), 0 0 26px rgba(34,211,238,.16) !important;
        }
        input[placeholder="Type password guess…"]{
            height: 58px !important;
            font-size: 19px !important;
            letter-spacing: .02em !important;
            padding: 0 14px !important;
            line-height: normal !important;
            box-sizing: border-box !important;
        }
        input[placeholder="Type password guess…"]:focus{
            outline: none !important;
        }
        /* Focus state on wrapper (Streamlit applies focus to wrapper) */
        [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within{
            border-color: rgba(168,85,247,.60) !important;
            box-shadow: 0 0 0 3px rgba(168,85,247,.18), 0 0 30px rgba(34,211,238,.18) !important;
        }
        input[placeholder="Type password guess…"]::placeholder{
            color: rgba(142,163,209,.85) !important;
        }

        /* Slightly tighter input label spacing (we hide label anyway) */
        [data-testid="stTextInput"]{
            margin-top: 4px;
        }

        /* Buttons are height-locked above; keep no extra overrides here */

        /* Toast/alerts tend to be bright; keep them cyber-themed */
        [data-testid="stAlert"]{
            border-radius: 12px !important;
            border: 1px solid rgba(34,211,238,.18) !important;
            box-shadow: var(--shadow) !important;
        }

        /* Styled popup (custom "toast") */
        .cyber-popup{
            position: fixed;
            right: 18px;
            top: 18px;
            z-index: 99999;
            width: min(520px, calc(100vw - 36px));
            pointer-events: none;
        }
        .cyber-popup-inner{
            pointer-events: none;
            display: flex;
            gap: 12px;
            align-items: center;
            padding: 14px 16px;
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(5,8,21,.58));
            border: 1px solid rgba(34,211,238,.26);
            outline: 1px solid rgba(168,85,247,.12);
            box-shadow: 0 18px 50px rgba(0,0,0,.40), 0 0 22px rgba(34,211,238,.10);
            animation: popupIn .20s ease-out, popupOut .45s ease-in 2.6s forwards;
        }
        .cyber-popup-icon{
            font-size: 18px;
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: rgba(34,211,238,.08);
            border: 1px solid rgba(34,211,238,.18);
            box-shadow: 0 0 18px rgba(34,211,238,.10);
            flex: 0 0 auto;
        }
        .cyber-popup-text{
            font-size: 13px;
            color: rgba(215,227,255,.92);
            line-height: 1.35;
        }
        .cyber-popup.success .cyber-popup-inner{
            border-color: rgba(34,197,94,.35);
            box-shadow: 0 18px 50px rgba(0,0,0,.40), 0 0 22px rgba(34,197,94,.10);
        }
        .cyber-popup.success .cyber-popup-icon{
            background: rgba(34,197,94,.10);
            border-color: rgba(34,197,94,.22);
            box-shadow: 0 0 18px rgba(34,197,94,.10);
        }
        .cyber-popup.error .cyber-popup-inner{
            border-color: rgba(251,113,133,.35);
            box-shadow: 0 18px 50px rgba(0,0,0,.40), 0 0 22px rgba(251,113,133,.10);
        }
        .cyber-popup.error .cyber-popup-icon{
            background: rgba(251,113,133,.10);
            border-color: rgba(251,113,133,.22);
            box-shadow: 0 0 18px rgba(251,113,133,.10);
        }
        .cyber-popup.warning .cyber-popup-inner{
            border-color: rgba(250,204,21,.28);
        }
        .cyber-popup.warning .cyber-popup-icon{
            background: rgba(250,204,21,.10);
            border-color: rgba(250,204,21,.22);
        }
        @keyframes popupIn{
            from{ transform: translateY(-8px); opacity: 0; }
            to{ transform: translateY(0); opacity: 1; }
        }
        @keyframes popupOut{
            to{ transform: translateY(-6px); opacity: 0; }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Initialize session state for game progress
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'completed_levels' not in st.session_state:
        st.session_state.completed_levels = []
    if 'game_completed' not in st.session_state:
        st.session_state.game_completed = False
    if "popup" not in st.session_state:
        st.session_state.popup = None

    # Styled popup feedback (cyber toast)
    if st.session_state.popup:
        popup = st.session_state.popup
        st.session_state.popup = None
        kind = popup.get("kind", "info")
        icon = popup.get("icon", "ℹ️")
        message = popup.get("message", "")
        st.markdown(
            f"""
            <div class="cyber-popup {kind}">
              <div class="cyber-popup-inner">
                <div class="cyber-popup-icon">{icon}</div>
                <div class="cyber-popup-text">{message}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Header Section (cyber HUD + subtle glitch)
    st.markdown("""
    <style>
      .hud-header{
        background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.62));
        padding: 38px 22px;
        border-radius: 16px;
        margin-bottom: 30px;
        border: 1px solid rgba(34,211,238,.30);
        outline: 1px solid rgba(168,85,247,.14);
        text-align: center;
        box-shadow: 0 14px 40px rgba(0,0,0,.35), 0 0 24px rgba(34,211,238,.10);
        position: relative;
        overflow: hidden;
      }
      .hud-header::before{
        content:"";
        position:absolute;
        inset:0;
        background:
          radial-gradient(700px 180px at 50% 0%, rgba(34,211,238,.20), transparent 65%),
          linear-gradient(120deg, transparent 25%, rgba(168,85,247,.10), transparent 60%);
        opacity:.9;
        pointer-events:none;
      }
      .hud-title{
        position: relative;
        display: inline-block;
        font-family: Orbitron, system-ui, sans-serif;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin: 0;
        font-size: 38px;
        font-weight: 700;
        color: #d7e3ff;
        text-shadow: 0 0 18px rgba(34,211,238,.18);
      }
      /* Animated/glitch title (same font family) */
      .hud-title.glitch::before, .hud-title.glitch::after{
        content: attr(data-text);
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        overflow: hidden;
        opacity: .62;
      }
      .hud-title.glitch::before{
        transform: translate(2px, -1px);
        color: rgba(34,211,238,.85);
        animation: glitch1 3.2s infinite linear alternate-reverse;
      }
      .hud-title.glitch::after{
        transform: translate(-2px, 1px);
        color: rgba(168,85,247,.75);
        animation: glitch2 2.6s infinite linear alternate-reverse;
      }
      @keyframes glitch1{
        0%{ clip-path: inset(0 0 90% 0); }
        18%{ clip-path: inset(10% 0 60% 0); }
        36%{ clip-path: inset(35% 0 35% 0); }
        54%{ clip-path: inset(60% 0 10% 0); }
        72%{ clip-path: inset(85% 0 5% 0); }
        100%{ clip-path: inset(0 0 90% 0); }
      }
      @keyframes glitch2{
        0%{ clip-path: inset(85% 0 5% 0); }
        22%{ clip-path: inset(55% 0 20% 0); }
        44%{ clip-path: inset(20% 0 55% 0); }
        66%{ clip-path: inset(5% 0 85% 0); }
        100%{ clip-path: inset(85% 0 5% 0); }
      }
      .hud-sub{
        position: relative;
        margin: 12px 0 0 0;
        font-size: 16px;
        color: rgba(167,243,255,.88);
        opacity: .92;
      }
      .hud-sub code{
        color: rgba(167,243,255,.92);
        background: rgba(34,211,238,.08);
        border: 1px solid rgba(34,211,238,.16);
        padding: 2px 8px;
        border-radius: 999px;
      }
    </style>
    <div class="hud-header">
      <h1 class="hud-title glitch" data-text="Crack John's Password">🔐 Crack John's Password</h1>
      <p class="hud-sub">Think like an attacker</p>
    </div>
    """, unsafe_allow_html=True)

    # Game progress and stats
    if not st.session_state.game_completed:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='progress-card compact tier-primary'>
                <div class='progress-label'>CURRENT LEVEL</div>
                <div class='progress-value'>Level {st.session_state.current_level}/5</div>
                <div class='progress-description'>Progress: {len(st.session_state.completed_levels)}/5 completed</div>
                <div class='attempt-badge'>Attempts: {st.session_state.attempts}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='progress-card compact tier-secondary'>
                <div class='progress-label'>GAME RULES</div>
                <div class='progress-value'>How to Play</div>
                <div class='progress-description'>Read each hint and guess John's password. Progress through 5 levels!</div>
                <div class='attempt-badge'>Case sensitive</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            completed_count = len(st.session_state.completed_levels)
            if completed_count == 0:
                status_text = "Not started"
                status_color = "#94a3b8"
            elif completed_count == 5:
                status_text = "COMPLETE!"
                status_color = "#22c55e"
            else:
                status_text = f"{completed_count}/5 Done"
                status_color = "#60a5fa"
            
            st.markdown(f"""
            <div class='progress-card compact tier-secondary'>
                <div class='progress-label'>GAME STATUS</div>
                <div class='progress-value' style='color: {status_color};'>{status_text}</div>
                <div class='progress-description'>Completed levels: {', '.join(map(str, st.session_state.completed_levels)) if st.session_state.completed_levels else 'None'}</div>
                <div class='attempt-badge'>Keep going!</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Level Navigation
    st.markdown("<div class='section-gap-lg'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Game Levels</div>', unsafe_allow_html=True)
    
    level_col1, level_col2, level_col3, level_col4, level_col5 = st.columns(5)
    
    levels = [
        {"num": 1, "title": "Default Password", "status": "Easy"},
        {"num": 2, "title": "Social Media Clues", "status": "Getting Warmer"},
        {"num": 3, "title": "Birthday Leak", "status": "Medium"},
        {"num": 4, "title": "Music Obsession", "status": "Hard"},
        {"num": 5, "title": "Password Manager", "status": "Expert"}
    ]
    
    columns = [level_col1, level_col2, level_col3, level_col4, level_col5]
    
    for col, level in zip(columns, levels):
        is_completed = level["num"] in st.session_state.completed_levels
        is_current = level["num"] == st.session_state.current_level and not st.session_state.game_completed
        
        border_color = "#22c55e" if is_completed else "#3b82f6" if is_current else "#475569"
        status_text = "✅ COMPLETED" if is_completed else "🎯 CURRENT" if is_current else "🔒 LOCKED"
        
        with col:
            st.markdown(f"""
            <div class='level-card compact tier-tertiary' style='border-color: {border_color};'>
                <div class='level-number'>Level {level['num']}</div>
                <div class='level-status'>{level['title']}</div>
                <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed else "rgba(59, 130, 246, 0.2)" if is_current else "rgba(71, 85, 105, 0.2)"};'>{status_text}</div>
            </div>
            """, unsafe_allow_html=True)

    # Hints Section - Only show current level if game not completed
    if not st.session_state.game_completed and st.session_state.current_level <= 5:
        st.markdown(f'<div class="subsection-header">Level {st.session_state.current_level} Hints - About John</div>', unsafe_allow_html=True)
        
        # Hints based on current level
        hints = {
            1: [
                {
                    "title": "Default Password",
                    "content": "John just set up a brand-new Wi-Fi router at home. Excited to get online, he rushed through the setup, clicked “Next” on every step, and left everything exactly as it was—including the admin login. The internet worked, Netflix streamed, and life moved on… but behind the scenes, his network sat wide open.\n\nWhat John ignored, an attacker looks for first.\nWhat he left unchanged is no longer just a setting… it’s an opportunity.\n\nNow his mistake is your treasure. Can you guess the admin password? 🔐"
                }
            ],
            2: [
                {
                    "title": "Oversharing on Social Media",
                    "content": "John loves sharing moments from his life online, but there’s one thing he talks about more than anything else—his dog. Scroll through his profile and you’ll see it everywhere: pictures, stories, captions full of love and pride.\nTo John, it’s just harmless posts. But to someone watching closely, it’s a pattern… a clue hiding in plain sight. The name he repeats, the emotion he attaches, the habit of adding simple numbers—everything starts forming a predictable secret.\n\nWhat John shared with the world has now become your advantage. Can you guess his password? 🔐",
                    "quotes": [
                        "“Rocky having a cute moment with me ❤️🐶”",
                        "“Happy birthday Rocky 🎉”",
                        "“Rocky is my whole world ❤️”",
                        "“Best day ever with Rocky 🐾”"
                    ]
                }
            ],
            3: [
                {
                    "title": "Birthday Post = Data Leak",
                    "content": "John recently celebrated his birthday and, like always, shared the moment online with friends and followers. In the excitement, he didn’t just post pictures—he revealed just enough information without realizing it. A simple birthday post, a mention of his age, and the exact date of celebration… small details that seem harmless on their own. But when combined, they start telling a bigger story—one that an attacker can piece together to uncover something far more sensitive.",
                    "caption": "“Finally turned 26 today! 🎉🥳 Feeling grateful for everything ❤️”",
                    "posted": "12th March",
                    "age": "26"
                }
            ],
            4: [
                {
                    "title": "Music Clue: Album + Year",
                    "content": "John has always been passionate about music, but recently he’s been obsessing over one particular artist. His feed is filled with posts about songs, lyrics, and admiration for what he calls the greatest album he has ever heard. In one post, he finally gives away more than he realizes—mentioning both the album and a key achievement tied to it. It may look like just another fan moment, but for someone paying attention, it’s the missing piece needed to uncover his password.\n\nHint: password is combination of alphabets, one special character and 4 numbers\n\nNow connect the dots… can you guess his password? 🔐",
                    "caption": "“I love this Eminem album the most ❤️🔥 He even won a Grammy for this in 2011! 🏆🎧”"
                }
            ],
            5: [
                {
                    "title": "No More Clues",
                    "content": "After a series of close calls and realizing how easily his passwords could be guessed, John finally understood the risk he had been taking. Each time his patterns were uncovered, it became clear that using personal information was no longer safe. Determined to fix this, he completely changed his approach. Instead of relying on memory or habits, he switched to using a password manager that generates strong, random passwords with no connection to his personal life. Now, there are no clues, no patterns, and nothing to trace back.\n\nThis time, there are no hints to rely on. Can you still crack it? 🔐",
                    "caption": "“Time to level up my security 🔐 No more easy passwords… using a password manager now!”"
                }
            ]
        }
        
        current_hints = hints[st.session_state.current_level]
        
        if st.session_state.current_level == 1:
            level1_story_html = current_hints[0]["content"].replace("\n", "<br/>")
            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'>Mission briefing</div>
                  <div class='hints-grid'>
                    <div class='hint-card primary' style='grid-column: 1 / -1;'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content' style='font-size: 18px; line-height: 1.75; font-weight: 650; text-align: left;'>
                        {level1_story_html}
                      </div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.session_state.current_level == 2:
            level2_story_html = current_hints[0]["content"].replace("\n", "<br/>")
            level2_quotes = current_hints[0].get("quotes", [])
            quotes_html = "\n".join([f"<div class='quote-line'>{q}</div>" for q in level2_quotes])

            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'>Social footprint analysis</div>
                  <div class='hints-grid'>
                    <div class='hint-card primary' style='grid-column: 1 / span 2;'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content' style='font-size: 18px; line-height: 1.75; font-weight: 650; text-align: left;'>
                        {level2_story_html}
                      </div>
                    </div>
                    <div class='quote-card' style='grid-column: 3 / 4;'>
                      <div class='quote-header'>
                        <div class='quote-avatar'></div>
                        <div class='quote-handle'>@johns_profile // captions</div>
                      </div>
                      {quotes_html}
                      <div class='quote-meta'>Pattern: repeated name + emotion + simple numbers</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.session_state.current_level == 3:
            level3_story_html = current_hints[0]["content"].replace("\n", "<br/>")
            level3_caption = current_hints[0].get("caption", "")
            level3_posted = current_hints[0].get("posted", "")
            level3_age = current_hints[0].get("age", "")

            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'>Timeline correlation</div>
                  <div class='hints-grid'>
                    <div class='hint-card primary' style='grid-column: 1 / span 2;'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content' style='font-size: 18px; line-height: 1.75; font-weight: 650; text-align: left;'>
                        {level3_story_html}
                      </div>
                    </div>
                    <div class='quote-card' style='grid-column: 3 / 4;'>
                      <div class='quote-header'>
                        <div class='quote-avatar'></div>
                        <div class='quote-handle'>@johns_profile // birthday post</div>
                      </div>
                      <div class='quote-line'>{level3_caption}</div>
                      <div class='quote-meta'>Posted: {level3_posted} · Age: {level3_age}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.session_state.current_level == 4:
            level4_story_html = current_hints[0]["content"].replace("\n", "<br/>")
            level4_caption = current_hints[0].get("caption", "")

            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'>Open-source intelligence</div>
                  <div class='hints-grid'>
                    <div class='hint-card primary' style='grid-column: 1 / span 2;'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content' style='font-size: 18px; line-height: 1.75; font-weight: 650; text-align: left;'>
                        {level4_story_html}
                      </div>
                    </div>
                    <div class='quote-card' style='grid-column: 3 / 4;'>
                      <div class='quote-header'>
                        <div class='quote-avatar'></div>
                        <div class='quote-handle'>@johns_profile // music post</div>
                      </div>
                      <div class='quote-line'>{level4_caption}</div>
                      <div class='quote-meta'>Clue: album name + special char + year</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.session_state.current_level == 5:
            level5_story_html = current_hints[0]["content"].replace("\n", "<br/>")
            level5_caption = current_hints[0].get("caption", "")

            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'>Zero-signal challenge</div>
                  <div class='hints-grid'>
                    <div class='hint-card primary' style='grid-column: 1 / span 2;'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content' style='font-size: 18px; line-height: 1.75; font-weight: 650; text-align: left;'>
                        {level5_story_html}
                      </div>
                    </div>
                    <div class='quote-card' style='grid-column: 3 / 4;'>
                      <div class='quote-header'>
                        <div class='quote-avatar'></div>
                        <div class='quote-handle'>@johns_profile // security update</div>
                      </div>
                      <div class='quote-line'>{level5_caption}</div>
                      <div class='quote-meta'>No patterns. No personal data. Pure randomness.</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class='hints-master tier-secondary'>
                  <div class='hints-master-title'>PRIMARY INTEL // LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-level'>LEVEL {st.session_state.current_level}</div>
                  <div class='hints-master-sub'></div>
                  <div class='hints-master-sub'></div>
                  <div class='hints-grid'>
                    <div class='hint-card primary'>
                      <div class='hint-title'>{current_hints[0]['title']}</div>
                      <div class='hint-content'>{current_hints[0]['content']}</div>
                    </div>
                    <div class='hint-card primary'>
                      <div class='hint-title'>{current_hints[1]['title']}</div>
                      <div class='hint-content'>{current_hints[1]['content']}</div>
                    </div>
                    <div class='hint-card primary'>
                      <div class='hint-title'>{current_hints[2]['title']}</div>
                      <div class='hint-content'>{current_hints[2]['content']}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Correct passwords for each level (for demo purposes)
        correct_passwords = {
            1: "admin",
            2: "Rocky123",
            3: "John12032000",
            4: "Recovery@2011",
            5: "G7#kP2!vQ9$xL"
        }

        # Password input row (immediately after hints)
        input_col, submit_col, reset_col = st.columns([6, 2, 2], vertical_alignment="bottom")

        with input_col:
            password_guess = st.text_input(
                "Password guess",
                type="password",
                key=f"guess_{st.session_state.current_level}",
                label_visibility="collapsed",
                placeholder="Type password guess…",
            )

        with submit_col:
            if st.button("🔓 Submit", use_container_width=True, type="primary"):
                if password_guess:
                    st.session_state.attempts += 1
                    if password_guess == correct_passwords[st.session_state.current_level]:
                        if st.session_state.current_level not in st.session_state.completed_levels:
                            st.session_state.completed_levels.append(st.session_state.current_level)

                        if st.session_state.current_level == 5:
                            st.session_state.game_completed = True
                            st.session_state.popup = {
                                "kind": "success",
                                "icon": "🏆",
                                "message": "LEVEL CLEARED! You cracked all 5 levels."
                            }
                        else:
                            st.session_state.current_level += 1
                            st.session_state.popup = {
                                "kind": "success",
                                "icon": "✅",
                                "message": f"ACCESS GRANTED. Moving to Level {st.session_state.current_level}."
                            }
                        st.rerun()
                    else:
                        st.session_state.popup = {
                            "kind": "error",
                            "icon": "❌",
                            "message": "ACCESS DENIED. Incorrect password."
                        }
                        st.rerun()
                else:
                    st.session_state.popup = {
                        "kind": "warning",
                        "icon": "⚠️",
                        "message": "Type a password guess first."
                    }
                    st.rerun()

        with reset_col:
            if st.button("🔄 Reset", use_container_width=True, type="secondary"):
                st.rerun()

        st.markdown("<div class='section-gap-lg'></div>", unsafe_allow_html=True)

    # Game completion screen
    elif st.session_state.game_completed:
        st.markdown("""
        <div class='success-message'>
            🏆 GAME COMPLETE! 🏆<br><br>
            You've successfully cracked all 5 levels and discovered John's password!<br>
            Total attempts: {}<br><br>
            🎮 Great detective work! 🎮
        </div>
        """.format(st.session_state.attempts), unsafe_allow_html=True)
        
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.current_level = 1
            st.session_state.attempts = 0
            st.session_state.completed_levels = []
            st.session_state.game_completed = False
            st.rerun()
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    # Game rules and tips
    st.markdown('<div class="section-header">Game Tips</div>', unsafe_allow_html=True)

    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.markdown("""
        <div class='info-card'>
            <div class='definition-title'>🎯 TIP 1</div>
            <div class='definition-content'>Pay attention to all hints - they build on each other!</div>
            <div class='definition-id'>Combine clues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col2:
        st.markdown("""
        <div class='info-card'>
            <div class='definition-title'>🔍 TIP 2</div>
            <div class='definition-content'>Passwords are case-sensitive. Watch for capital letters!</div>
            <div class='definition-id'>Check case</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col3:
        st.markdown("""
        <div class='info-card'>
            <div class='definition-title'>💡 TIP 3</div>
            <div class='definition-content'>Think like John - what would he choose based on his life?</div>
            <div class='definition-id'>Profile-based</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div class='app-footer'>Developed by Sighbear technology Private Limited</div>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    render_game()