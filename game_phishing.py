import streamlit as st


PHISHING_SENDER_PAIRS = [
    {
        "id": 1,
        "title": "Typosquatting (Easy)",
        "option_a": "support@paypal.com",
        "option_b": "support@paypaI.com",
        "correct": "A",
        "feedback": "The fake address swaps the lowercase 'l' in paypal.com with a capital 'I' (paypaI.com). Attackers register look‑alike domains so that, at a glance, users think they are on the real site.",
        "tip": "Always read the domain slowly, character by character. Pay special attention to letters that look similar, like l vs I, rn vs m, or 0 vs O.",
    },
    {
        "id": 2,
        "title": "Numeric Substitution",
        "option_a": "security@google.com",
        "option_b": "security@g00gle.com",
        "correct": "A",
        "feedback": "The attacker replaced the two 'o' characters in google.com with zeros (g00gle.com). The email looks correct at first glance, but it points to a completely different domain.",
        "tip": "In security‑sensitive emails (login alerts, password resets, invoices), double‑check that letters are not silently replaced with numbers (0/1/3) or similar characters.",
    },
    {
        "id": 3,
        "title": "Subdomain Attack (Important)",
        "option_a": "alerts@paypal.com.security-update.net",
        "option_b": "alerts@paypal.com",
        "correct": "B",
        "feedback": "In 'alerts@paypal.com.security-update.net', the real domain is security-update.net. 'paypal.com' is only a subdomain prefix, so this email does NOT come from PayPal.",
        "tip": "Browsers and mail clients read domains from right to left. The part immediately before the first slash (or after the last @) and just before the TLD (.com, .net, etc.) is the real domain owner.",
    },
    {
        "id": 4,
        "title": "Hyphen Trick",
        "option_a": "support@paypal.com",
        "option_b": "support@secure-paypal.com",
        "correct": "A",
        "feedback": "Adding words like 'secure', 'login' or 'verify' in front of a brand name (secure-paypal.com) creates a new, unrelated domain. It feels more trustworthy, but it is not owned by the real company.",
        "tip": "Real brands usually use short, simple domains (paypal.com, google.com). Be suspicious of extra marketing words before or after the brand in the domain name.",
    },
    {
        "id": 5,
        "title": "Free Email Abuse",
        "option_a": "paypal.support@gmail.com",
        "option_b": "support@paypal.com",
        "correct": "B",
        "feedback": "Large companies almost never use free email providers (like Gmail, Yahoo, Outlook) for official customer support. 'paypal.support@gmail.com' could be created by anyone.",
        "tip": "When an email claims to be from a big brand, look for a domain that the company actually owns (like @paypal.com), not a generic free mailbox domain.",
    },
    {
        "id": 6,
        "title": "Legit Subdomain (Hard)",
        "option_a": "accounts.google.com",
        "option_b": "google.accounts-security.com",
        "correct": "A",
        "feedback": "In 'accounts.google.com', 'google.com' is the base domain and 'accounts' is a subdomain owned by Google. In 'google.accounts-security.com', the true domain is accounts-security.com and 'google' is just a misleading subdomain.",
        "tip": "A legitimate subdomain will still end in the company’s real domain name (like something.google.com). If the company name is in the middle and the ending is different, treat it as suspicious.",
    },
]


def render_game() -> None:
    """Render the phishing awareness game (Level 1: Sender pairs)."""

    # Apply cyber-game theme similar to Game 1
    cyber_css = """
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

        .stApp, [data-testid="stAppViewContainer"]{
            background: radial-gradient(1200px 700px at 20% 10%, rgba(168,85,247,.18), transparent 55%),
                        radial-gradient(900px 600px at 85% 20%, rgba(34,211,238,.14), transparent 60%),
                        linear-gradient(180deg, var(--bg0), var(--bg1));
            color: var(--text);
            font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        }

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
        .phish-shell{
            max-width: 1100px;
            margin: 1.5rem auto 2.5rem auto;
            padding: 1.75rem 1.5rem 1.5rem 1.5rem;
            border-radius: 16px;
            border: 3px solid rgba(34,211,238,.35);
            outline: 1px solid rgba(168,85,247,.25);
            box-shadow: 0 28px 90px rgba(0,0,0,.65), 0 0 40px rgba(34,211,238,.22);
            background: radial-gradient(900px 260px at 50% 0%, rgba(34,211,238,.25), transparent 60%),
                        linear-gradient(180deg, rgba(14,26,43,.96), rgba(5,8,21,.80));
        }

        .phish-header{
            display:flex;
            justify-content: space-between;
            align-items:flex-end;
            gap: 1.5rem;
            margin-bottom: 0.75rem;
        }
        .phish-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 1.9rem;
            letter-spacing: .14em;
            text-transform: uppercase;
            color: var(--cyan);
            text-shadow: 0 0 12px rgba(34,211,238,.32);
            position: relative;
            display: inline-block;
        }
        /* Very subtle glitch sheen, not full displacement (keeps text readable) */
        .phish-title.glitch::before,
        .phish-title.glitch::after{
            content: "";
            position: absolute;
            inset: 0;
            pointer-events: none;
            border-radius: 999px;
            opacity: .16;
        }
        .phish-title.glitch::before{
            background: linear-gradient(120deg, transparent 40%, rgba(168,85,247,.45), transparent 60%);
            mix-blend-mode: screen;
            animation: phishSheen 4s ease-in-out infinite;
        }
        .phish-title.glitch::after{
            display: none;
        }
        @keyframes phishSheen{
            0%, 100%{ transform: translateX(-140%); }
            50%{ transform: translateX(140%); }
        }
        .phish-level-pill{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: .8rem;
            padding: .35rem .85rem;
            border-radius: 999px;
            border: 1px solid rgba(34,211,238,.5);
            background: rgba(34,211,238,.08);
            color: rgba(167,243,255,.92);
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .phish-subtitle{
            color: var(--muted);
            font-size: .95rem;
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
        }

        .phish-pair-card{
            margin-top: 0.75rem;
            padding: 1.25rem 1rem;
            border-radius: 14px;
            background: rgba(13,23,42,.90);
            border: 1px solid rgba(148,163,184,.45);
        }

        .phish-pair-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            color: rgba(167,243,255,.96);
            font-size: 1.1rem;
            margin-bottom: .5rem;
        }

        .phish-option-card{
            border-radius: 12px;
            padding: 1.5rem 1.25rem;
            margin-bottom: 0.5rem;
            background: rgba(14,26,43,.88);
            border: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 18px 45px rgba(0,0,0,.45);
            min-height: 150px;
        }

        .phish-option-label{
            font-size: .75rem;
            text-transform: uppercase;
            letter-spacing: .12em;
            color: rgba(148,163,184,.95);
            margin-bottom: .35rem;
        }

        .phish-option-address{
            font-family: 'Share Tech Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 24px;
            color: rgba(167,243,255,.98);
            letter-spacing: .02em;
            text-shadow: 0 0 18px rgba(34,211,238,.20);
        }

        .phish-feedback{
            margin-top: 1.25rem;
        }
        .phish-feedback-card{
            border-radius: 12px;
            padding: 1rem 1.1rem;
            background: linear-gradient(180deg, rgba(15,23,42,.96), rgba(15,23,42,.88));
            border: 1px solid rgba(34,211,238,.30);
            box-shadow: 0 14px 40px rgba(0,0,0,.55);
        }
        .phish-feedback-card.ok{
            border-color: rgba(34,197,94,.60);
        }
        .phish-feedback-card.bad{
            border-color: rgba(248,113,113,.70);
        }
        .phish-feedback-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: .9rem;
            letter-spacing: .14em;
            text-transform: uppercase;
            color: rgba(167,243,255,.92);
            margin-bottom: .35rem;
        }
        .phish-feedback-body{
            font-size: .9rem;
            color: var(--text);
            line-height: 1.6;
        }
        .phish-feedback-tip{
            margin-top: .6rem;
            font-size: .85rem;
            color: var(--muted);
        }
    </style>
    """
    st.markdown(cyber_css, unsafe_allow_html=True)

    # Back to hub
    top_left, _, _ = st.columns([2, 6, 2])
    with top_left:
        if st.button("← Back to main menu", use_container_width=True, key="phish_back_to_main"):
            st.session_state.current_page = "landing"
            st.session_state.selected_game = None
            st.rerun()

    if "phishing_pair_index" not in st.session_state:
        st.session_state.phishing_pair_index = 0
    if "phishing_completed_pairs" not in st.session_state:
        st.session_state.phishing_completed_pairs = []

    pair_index = st.session_state.phishing_pair_index
    pair = PHISHING_SENDER_PAIRS[pair_index]

    # Level navigation (6 sender pairs as levels)
    current_level = pair_index + 1
    completed = set(st.session_state.phishing_completed_pairs)

    # Header Section with title and subtitle
    st.markdown(
        """
        <style>
            .phish-hud-header{
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
            .phish-hud-header::before{
                content:"";
                position:absolute;
                inset:0;
                background:
                    radial-gradient(700px 180px at 50% 0%, rgba(34,211,238,.20), transparent 65%),
                    linear-gradient(120deg, transparent 25%, rgba(168,85,247,.10), transparent 60%);
                opacity:.9;
                pointer-events:none;
            }
            .phish-title-main{
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
            .phish-title-main.glitch::before, .phish-title-main.glitch::after{
                content: attr(data-text);
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                overflow: hidden;
                opacity: .62;
            }
            .phish-title-main.glitch::before{
                transform: translate(2px, -1px);
                color: rgba(34,211,238,.85);
                animation: phishGlitch1 3.2s infinite linear alternate-reverse;
            }
            .phish-title-main.glitch::after{
                transform: translate(-2px, 1px);
                color: rgba(168,85,247,.75);
                animation: phishGlitch2 2.6s infinite linear alternate-reverse;
            }
            @keyframes phishGlitch1{
                0%{ clip-path: inset(0 0 90% 0); }
                18%{ clip-path: inset(10% 0 60% 0); }
                36%{ clip-path: inset(35% 0 35% 0); }
                54%{ clip-path: inset(60% 0 10% 0); }
                72%{ clip-path: inset(85% 0 5% 0); }
                100%{ clip-path: inset(0 0 90% 0); }
            }
            @keyframes phishGlitch2{
                0%{ clip-path: inset(85% 0 5% 0); }
                22%{ clip-path: inset(55% 0 20% 0); }
                44%{ clip-path: inset(20% 0 55% 0); }
                66%{ clip-path: inset(5% 0 85% 0); }
                100%{ clip-path: inset(85% 0 5% 0); }
            }
            .phish-hud-sub{
                position: relative;
                margin: 12px 0 0 0;
                font-size: 16px;
                color: rgba(167,243,255,.88);
                opacity: .92;
            }
            .section-header {
                background: linear-gradient(90deg, rgba(14,26,43,.95), rgba(14,26,43,.70));
                color: var(--cyan);
                padding: 15px 20px;
                border-radius: 10px;
                font-size: 24px;
                font-weight: bold;
                margin: 30px 0 20px 0;
                border-left: 5px solid var(--cyan);
                box-shadow: 0 10px 30px rgba(0,0,0,.45);
                text-transform: uppercase;
                letter-spacing: .06em;
                font-family: 'Orbitron', system-ui, sans-serif;
                position: relative;
                overflow: hidden;
            }
            .level-card {
                background: rgba(14,26,43,.72);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,.45);
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
                box-shadow: 0 10px 30px rgba(0,0,0,.45), 0 0 18px rgba(34,211,238,.35);
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
            .level-button:hover {
                background: rgba(34, 211, 238, 0.16);
                box-shadow: 0 0 18px rgba(34,211,238,.18);
            }
        </style>
        <div class="phish-hud-header">
            <h1 class="phish-title-main glitch" data-text="PHISHING AWARENESS">🛡️ PHISHING AWARENESS</h1>
            <p class="phish-hud-sub">Select the <strong>legitimate sender</strong> from each pair. Watch out for typos, swapped letters, fake subdomains and free-mail abuse.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Game progress stats
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown(f"""
        <div class='progress-card compact tier-primary'>
            <div class='progress-label'>CURRENT LEVEL</div>
            <div class='progress-value'>Level {current_level}/6</div>
            <div class='progress-description'>Progress: {len(completed)}/6 completed</div>
            <div class='attempt-badge'>Sender Check</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        st.markdown("""
        <div class='progress-card compact tier-secondary'>
            <div class='progress-label'>GAME RULES</div>
            <div class='progress-value'>How to Play</div>
            <div class='progress-description'>Identify legitimate senders vs phishing attempts. Progress through 6 levels!</div>
            <div class='attempt-badge'>Read carefully</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        if len(completed) == 0:
            status_text = "Not started"
            status_color = "#94a3b8"
        elif len(completed) == 6:
            status_text = "COMPLETE!"
            status_color = "#22c55e"
        else:
            status_text = f"{len(completed)}/6 Done"
            status_color = "#60a5fa"
        
        st.markdown(f"""
        <div class='progress-card compact tier-secondary'>
            <div class='progress-label'>GAME STATUS</div>
            <div class='progress-value' style='color: {status_color};'>{status_text}</div>
            <div class='progress-description'>Completed levels: {', '.join(map(str, sorted(completed))) if completed else 'None'}</div>
            <div class='attempt-badge'>Keep going!</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Level Navigation Card Display
    st.markdown('<div class="section-header">Game Levels</div>', unsafe_allow_html=True)
    
    level_cols = st.columns(6)
    for i, col in enumerate(level_cols, start=1):
        is_completed = i in completed
        is_current = (i == current_level) and (len(completed) < len(PHISHING_SENDER_PAIRS))
        border_color = "#22c55e" if is_completed else "#3b82f6" if is_current else "#475569"
        status_text = "✅ COMPLETED" if is_completed else "🎯 CURRENT" if is_current else "🔒 LOCKED"
        
        level_info = PHISHING_SENDER_PAIRS[i-1]
        
        with col:
            st.markdown(
                f"""
                <div class='level-card compact tier-tertiary' style='border-color: {border_color};'>
                    <div class='level-number'>Level {i}</div>
                    <div class='level-status'>{level_info['title'].split('(')[0].strip()}</div>
                    <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed else "rgba(59, 130, 246, 0.2)" if is_current else "rgba(71, 85, 105, 0.2)"};'>{status_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="phish-pair-card">
            <div class="phish-pair-title">Level {pair['id']}: {pair['title']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2, vertical_alignment="top")

    # Container for feedback so it appears under the buttons with some spacing
    feedback_placeholder = st.container()

    def handle_choice(choice: str) -> None:
        correct = pair["correct"]
        is_correct = choice == correct
        with feedback_placeholder:
            st.markdown(
                f"""
                <div class="phish-feedback">
                    <div class="phish-feedback-card {'ok' if is_correct else 'bad'}">
                        <div class="phish-feedback-title">
                            {"✅ Correct choice" if is_correct else "❌ Not quite, read the clues"}
                        </div>
                        <div class="phish-feedback-body">
                            {pair['feedback']}
                        </div>
                        <div class="phish-feedback-tip">
                            <strong>Security tip:</strong> {pair.get('tip', '')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if is_correct:
            if current_level not in st.session_state.phishing_completed_pairs:
                st.session_state.phishing_completed_pairs.append(current_level)

            # Small popup/toast for positive feedback
            st.toast("✅ Correct! Moving to the next level.", icon="✅")

            if st.session_state.phishing_pair_index < len(PHISHING_SENDER_PAIRS) - 1:
                st.session_state.phishing_pair_index += 1
                st.rerun()
            else:
                st.info("🎉 You completed all sender pairs for Level 1!")

    with col_a:
        st.markdown(
            f"""
            <div class="phish-option-card">
                <div class="phish-option-label">Option A — candidate sender</div>
                <div class="phish-option-address">{pair['option_a']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Choose A", key=f"phish_A_{pair['id']}", use_container_width=True):
            handle_choice("A")

    with col_b:
        st.markdown(
            f"""
            <div class="phish-option-card">
                <div class="phish-option-label">Option B — candidate sender</div>
                <div class="phish-option-address">{pair['option_b']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Choose B", key=f"phish_B_{pair['id']}", use_container_width=True):
            handle_choice("B")

