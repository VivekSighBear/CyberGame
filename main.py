import streamlit as st

# Game imports
from game_johns_password import render_game as render_john_game
from game_phishing import render_game as render_phishing_game

def render_landing_page() -> None:
    """Render the main landing page with game options."""

    # Custom CSS for landing page
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --bg0: #050815;
            --bg1: #0b1026;
            --panel: #0e1a2b;
            --panel2: rgba(14,26,43,.72);
            --text: #d7e3ff;
            --muted: #8ea3d1;
            --cyan: #22d3ee;
            --mag: #a855f7;
            --green: #22c55e;
            --red: #fb7185;
            --blue: #3b82f6;
            --border: rgba(34,211,238,.28);
            --shadow: 0 10px 30px rgba(0,0,0,.45);
            --glow: 0 0 18px rgba(34,211,238,.35);
        }

        /* Base styles */
        .stApp, [data-testid="stAppViewContainer"] {
            background: radial-gradient(1200px 700px at 20% 10%, rgba(168,85,247,.18), transparent 55%),
                        radial-gradient(900px 600px at 85% 20%, rgba(34,211,238,.14), transparent 60%),
                        linear-gradient(180deg, var(--bg0), var(--bg1));
            color: var(--text);
            font-family: 'JetBrains Mono', ui-monospace, monospace;
        }

        /* Cyber grid */
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
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
            opacity: .55;
            animation: gridShift 18s linear infinite;
        }

        @keyframes gridShift {
            from { transform: translateY(0); }
            to { transform: translateY(80px); }
        }

        /* Hide Streamlit branding */
        [data-testid="stHeader"] { display: none; }
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

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

        /* Main container */
        .main-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }

        /* Hero section */
        .hero-section {
            text-align: center;
            margin-bottom: 4rem;
            position: relative;
        }

        .hero-title {
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 5rem;
            font-weight: 700;
            color: var(--cyan);
            text-shadow: 0 0 20px rgba(34,211,238,.4);
            margin-bottom: 1rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            position: relative;
            display: inline-block;
        }

        .hero-title::before,
        .hero-title::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        .hero-title::before {
            animation: glitch1 2s infinite;
            color: var(--mag);
            z-index: -1;
            transform: translate(-2px, -2px);
        }

        .hero-title::after {
            animation: glitch2 3s infinite;
            color: var(--cyan);
            z-index: -2;
            transform: translate(2px, 2px);
        }

        @keyframes glitch1 {
            0% { clip-path: inset(0 0 90% 0); transform: translate(-2px, -1px); }
            18% { clip-path: inset(10% 0 60% 0); transform: translate(-3px, -2px); }
            36% { clip-path: inset(35% 0 35% 0); transform: translate(1px, -3px); }
            54% { clip-path: inset(60% 0 10% 0); transform: translate(-1px, 2px); }
            72% { clip-path: inset(85% 0 5% 0); transform: translate(2px, 1px); }
            100% { clip-path: inset(0 0 90% 0); transform: translate(-2px, -1px); }
        }

        @keyframes glitch2 {
            0% { clip-path: inset(85% 0 5% 0); transform: translate(2px, 1px); }
            22% { clip-path: inset(55% 0 20% 0); transform: translate(3px, 1px); }
            44% { clip-path: inset(20% 0 55% 0); transform: translate(-2px, 3px); }
            66% { clip-path: inset(5% 0 85% 0); transform: translate(2px, -2px); }
            100% { clip-path: inset(85% 0 5% 0); transform: translate(2px, 1px); }
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: var(--muted);
            margin-top: 1rem;
            letter-spacing: 0.05em;
        }

        /* Game cards grid */
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2.5rem;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Game card */
        .game-card {
            background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.72));
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
        }

        .game-card::before {
            content: "";
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--cyan), var(--mag), var(--cyan));
            border-radius: 22px;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: -1;
        }

        .game-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: var(--glow), var(--shadow);
        }

        .game-card:hover::before {
            opacity: 0.3;
        }

        .game-card.coming-soon {
            opacity: 0.8;
            filter: grayscale(0.5);
        }

        .game-card.coming-soon:hover {
            transform: translateY(-5px) scale(1.01);
        }

        .game-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            padding: 0.3rem 1rem;
            background: linear-gradient(45deg, var(--cyan), var(--mag));
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            color: var(--bg0);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 0 15px rgba(34,211,238,.3);
        }

        .game-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            text-align: center;
            filter: drop-shadow(0 0 10px rgba(34,211,238,.3));
        }

        .game-title {
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--cyan);
            margin-bottom: 1rem;
            text-align: center;
            letter-spacing: 0.05em;
        }

        .game-description {
            color: var(--text);
            margin-bottom: 1.5rem;
            line-height: 1.6;
            text-align: center;
            flex-grow: 1;
        }

        .game-stats {
            background: rgba(34,211,238,.1);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid rgba(34,211,238,.2);
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            color: var(--muted);
        }

        .stat-row:last-child {
            margin-bottom: 0;
        }

        .stat-value {
            color: var(--cyan);
            font-weight: bold;
        }

        .play-button {
            background: linear-gradient(45deg, var(--cyan), var(--mag));
            border: none;
            border-radius: 12px;
            padding: 1rem;
            color: var(--bg0);
            font-family: 'Orbitron', system-ui, sans-serif;
            font-weight: bold;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 1rem;
            text-align: center;
            text-decoration: none;
            display: block;
            box-shadow: 0 0 20px rgba(34,211,238,.2);
        }

        .play-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(34,211,238,.4);
        }

        .play-button.coming-soon {
            background: linear-gradient(45deg, #4a5568, #2d3748);
            cursor: not-allowed;
            opacity: 0.7;
        }

        .play-button.coming-soon:hover {
            transform: none;
            box-shadow: none;
        }

        /* Features section */
        .features-section {
            max-width: 1200px;
            margin: 4rem auto;
            padding: 2rem;
        }

        .features-title {
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 2rem;
            color: var(--cyan);
            text-align: center;
            margin-bottom: 2rem;
            text-transform: uppercase;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .feature-item {
            text-align: center;
            padding: 1.5rem;
            background: rgba(14,26,43,.5);
            border-radius: 15px;
            border: 1px solid rgba(34,211,238,.1);
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .feature-title {
            font-family: 'Orbitron', system-ui, sans-serif;
            color: var(--mag);
            margin-bottom: 0.5rem;
        }

        .feature-description {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            color: var(--muted);
            border-top: 1px solid rgba(34,211,238,.1);
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
    render_landing_content()

def render_landing_content():
    """Render the landing page content."""
    
    # Hero section
    st.markdown("""
    <div class="main-container">
        <div class="hero-section">
            <h1 class="hero-title" data-text="CYBER SECURITY GAMES">CYBER SECURITY GAMES</h1>
            <p class="hero-subtitle">Train your ethical hacking skills through interactive challenges</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Games grid
    st.markdown('<div class="games-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <div class="game-badge">NEW</div>
            <div class="game-icon">🔐</div>
            <div class="game-title">Crack John's Password</div>
            <div class="game-description">
                Investigate John's digital footprint and crack his passwords across 5 challenging levels. 
                Learn about password vulnerabilities and social engineering through hands-on gameplay.
            </div>
            <div class="game-stats">
                <div class="stat-row">
                    <span>Levels</span>
                    <span class="stat-value">5</span>
                </div>
                <div class="stat-row">
                    <span>Focus</span>
                    <span class="stat-value">Password/OSINT</span>
                </div>
                <div class="stat-row">
                    <span>Game Mode</span>
                    <span class="stat-value">Attacker</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("PLAY NOW", key="play_game1", use_container_width=True):
            st.session_state.current_page = 'game1'
            st.session_state.selected_game = 'game1'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="game-card">
            <div class="game-badge">NEW</div>
            <div class="game-icon">🛡️</div>
            <div class="game-title">Phishing Awareness</div>
            <div class="game-description">
                Learn to spot suspicious senders, malicious links, dangerous attachments, and deceptive messages. 
                Master 4 levels of comprehensive phishing detection skills.
            </div>
            <div class="game-stats">
                <div class="stat-row">
                    <span>Levels</span>
                    <span class="stat-value">4 (SLAM)</span>
                </div>
                <div class="stat-row">
                    <span>Focus</span>
                    <span class="stat-value">Email Phishing</span>
                </div>
                <div class="stat-row">
                    <span>Game Mode</span>
                    <span class="stat-value">Defensive</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("PLAY NOW", key="play_game2", use_container_width=True):
            st.session_state.current_page = 'game2'
            st.session_state.selected_game = 'game2'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Developed by Sighbear Technology Private Limited</p>
        
    </div>
    """, unsafe_allow_html=True)

def render_game2_placeholder():
    """Render a placeholder for Game 2."""
    
    st.markdown("""
    <style>
        .back-button {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: linear-gradient(45deg, var(--cyan), var(--mag));
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            color: var(--bg0);
            font-family: 'Orbitron', system-ui, sans-serif;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            border: 1px solid rgba(255,255,255,.1);
        }
        .back-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(34,211,238,.3);
        }
        .placeholder-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
        }
        .placeholder-title {
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 3rem;
            color: var(--cyan);
            margin-bottom: 1rem;
            text-shadow: 0 0 20px rgba(34,211,238,.3);
        }
        .placeholder-subtitle {
            font-size: 1.2rem;
            color: var(--muted);
            margin-bottom: 2rem;
            max-width: 600px;
        }
        .construction-icon {
            font-size: 8rem;
            margin-bottom: 2rem;
            filter: drop-shadow(0 0 20px rgba(34,211,238,.3));
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← BACK TO GAMES", key="back_to_landing"):
        st.session_state.current_page = 'landing'
        st.session_state.selected_game = None
        st.rerun()

    # Placeholder content
    st.markdown("""
    <div class="placeholder-container">
        <div class="construction-icon">🛠️</div>
        <h1 class="placeholder-title">GAME 2</h1>
        <p class="placeholder-subtitle">This game is currently under construction. Our team is working hard to bring you an exciting new cybersecurity challenge. Stay tuned!</p>
        <div style="margin-top: 3rem; color: var(--muted);">
            <p>Expected features:</p>
            <p style="margin-top: 1rem;">• Network Security Challenges</p>
            <p>• Penetration Testing Scenarios</p>
            <p>• Multi-level Difficulty</p>
            <p>• Real-world Simulations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    """Main application entry point."""
    
    # Check if we're on landing page or game page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'

    # Set page config once (Streamlit requirement)
    st.set_page_config(
        page_title="Cyber Security Games Hub",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if st.session_state.current_page == 'landing':
        render_landing_page()
    elif st.session_state.current_page == 'game1':
        render_john_game()
    elif st.session_state.current_page == 'game2':
        render_phishing_game()

if __name__ == "__main__":
    main()