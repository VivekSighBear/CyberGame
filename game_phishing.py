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

PHISHING_LINK_SCENARIOS = [
    {
        "id": 1,
        "title": "Mismatch Link (Essential)",
        "displayed_text": "Reset your password here",
        "displayed_url": "https://google.com",
        "actual_url": "https://google-account-security-alert.com",
        "correct": "phishing",
        "feedback": "The anchor text says 'google.com' but the actual URL (shown on hover) redirects to 'google-account-security-alert.com'. Attackers use this technique to trick users into thinking they're clicking a legitimate link.",
        "tip": "Always hover over links to see the actual URL before clicking. The displayed text and the real destination often don't match in phishing emails.",
    },
    {
        "id": 2,
        "title": "Legitimate Link (Safe)",
        "displayed_text": "View your Google Account security settings",
        "displayed_url": "https://accounts.google.com/security",
        "actual_url": "https://accounts.google.com/security",
        "correct": "safe",
        "feedback": "This is a legitimate Google URL. The domain 'accounts.google.com' is owned and controlled by Google. The path '/security' leads to real security settings. This link is safe to click.",
        "tip": "Legitimate company URLs typically use their official domain names (like accounts.google.com, login.paypal.com). If you're unsure, visit the company's website directly instead of clicking emails.",
    },
    {
        "id": 3,
        "title": "Domain Spoofing (Phishing)",
        "displayed_text": "Login to your Microsoft account",
        "displayed_url": "https://microsoft.online-login.com",
        "actual_url": "https://microsoft.online-login.com/malware/steal-credentials",
        "correct": "phishing",
        "feedback": "This uses a fake domain that looks like Microsoft but isn't official. The domain 'microsoft.online-login.com' is designed to trick users into thinking it's legitimate, but it's controlled by attackers.",
        "tip": "Check the full domain carefully. Official Microsoft domains end in microsoft.com, not variations like microsoft.online-login.com.",
    },
    {
        "id": 4,
        "title": "Secure Banking Link (Safe)",
        "displayed_text": "Check your account balance",
        "displayed_url": "https://online.chase.com/account/summary",
        "actual_url": "https://online.chase.com/account/summary",
        "correct": "safe",
        "feedback": "This is a legitimate Chase banking URL. The domain 'online.chase.com' is an official Chase domain for online banking services. The URL structure matches typical banking site patterns.",
        "tip": "Legitimate banking sites use official domains and have consistent URL patterns. Always verify the full domain before entering credentials.",
    },
    {
        "id": 5,
        "title": "URL Shortener Attack (Phishing)",
        "displayed_text": "Download your invoice immediately",
        "displayed_url": "https://bit.ly/3xY7zK9",
        "actual_url": "https://bit.ly/3xY7zK9",
        "correct": "phishing",
        "feedback": "URL shorteners hide the real destination. While bit.ly is legitimate, attackers use it to mask malicious URLs. You can't see where you're actually going without clicking.",
        "tip": "Be cautious with shortened URLs from unknown senders. Legitimate companies typically use full URLs for important communications.",
    },
]

PHISHING_MESSAGE_SCENARIOS = [
    {
        "id": 1,
        "title": "Digital Arrest Notice",
        "message": "This is to inform you that your Aadhaar credentials have been flagged in a financial investigation linked to suspicious transactions across multiple accounts. As per instructions from the Cyber Crime Division, you are required to remain available on this line while we complete verification. Failure to cooperate may result in immediate legal action including account freeze and physical arrest. To proceed with verification, you must transfer the refundable security amount to the government-authorized account provided below.",
        "correct": "phishing",
        "feedback": "This is a classic authority impersonation scam using fear tactics. Real government agencies never demand money transfers over phone calls for 'verification'. The urgency, isolation tactics ('stay on call'), and payment request are clear red flags.",
        "tip": "Government agencies never ask for money transfers for verification. Real officials provide proper documentation and follow legal procedures, not immediate payment demands.",
    },
    {
        "id": 2,
        "title": "Bank Transaction Alert",
        "message": "We noticed a declined transaction attempt of ₹45,000 on your account today. If you initiated this, no further action is needed. If you do not recognize this activity, we recommend reviewing recent transactions and contacting support through your bank's official app or registered customer care number.",
        "correct": "safe",
        "feedback": "This is a legitimate bank alert. It provides factual information without creating urgency, doesn't ask for sensitive data or payments, and directs you to official channels for verification.",
        "tip": "Legitimate bank alerts typically inform without demanding immediate action. They direct you to official channels rather than asking for personal information or payments.",
    },
    {
        "id": 3,
        "title": "Courier Delivery Issue",
        "message": "Dear Customer, your shipment scheduled for delivery today could not be processed due to an address validation issue in our system. To avoid return or cancellation, please confirm your delivery details within 2 hours using the secure link below: delivery-update-support.com/track. Failure to respond may result in additional charges.",
        "correct": "phishing",
        "feedback": "This scam uses urgency and fake domains. The domain 'delivery-update-support.com' looks official but isn't real. Real courier services don't use external links for address verification or charge for basic delivery updates.",
        "tip": "Always verify courier domains through official websites. Real delivery services use their official domains and rarely charge for basic address verification or create artificial urgency.",
    },
    {
        "id": 4,
        "title": "Loan Approval Notification",
        "message": "Dear Applicant, your personal loan request has been conditionally approved based on your submitted details. To proceed with disbursement, a one-time refundable processing and verification fee of ₹2,999 is required. This ensures compliance with RBI guidelines and account validation. The amount will be adjusted in your first EMI.",
        "correct": "phishing",
        "feedback": "This is a common loan scam. Legitimate lenders never charge processing fees before loan disbursement. The 'refundable fee' trick and misuse of RBI authority name are classic scam tactics.",
        "tip": "Legitimate lenders deduct fees from the loan amount, never ask for upfront payments. RBI doesn't require individual verification fees for loan processing.",
    },
    {
        "id": 5,
        "title": "Shipment Delay Update",
        "message": "Your shipment is currently delayed due to operational constraints at the local hub. No action is required from your side at this time. You may track the updated delivery schedule through the official courier website or mobile application.",
        "correct": "safe",
        "feedback": "This is a legitimate courier update. It provides information without urgency, doesn't request payments or personal data, and directs you to official platforms for tracking.",
        "tip": "Legitimate courier notifications typically provide information without demanding immediate action or external links. They direct you to official apps or websites for tracking.",
    },
]

PHISHING_ATTACHMENT_SCENARIOS = [
    {
        "id": 1,
        "title": "Obvious Malicious Attachment (Phishing)",
        "sender": "courier-service@delivery-tracking.net",
        "subject": "Urgent: Package Delivery Failed",
        "message": "Your package delivery failed. Please see attached invoice and reschedule delivery.",
        "attachment": "Invoice_Receipt.zip",
        "correct": "phishing",
        "feedback": "This email contains multiple red flags: ZIP attachments are commonly used to hide malware, the sender domain is suspicious, and legitimate courier services rarely send invoices as ZIP files for delivery issues.",
        "tip": "Legitimate companies rarely send ZIP attachments for delivery updates. Always verify before opening compressed files from unknown senders.",
    },
    {
        "id": 2,
        "title": "Legitimate Document (Safe)",
        "sender": "documents@secure-storage.com",
        "subject": "Your Monthly Statement is Ready",
        "message": "Hello,\nYour monthly account statement is now available for download. Please review your transactions and let us know if you have any questions.",
        "attachment": "Monthly_Statement_March_2026.pdf",
        "correct": "safe",
        "feedback": "This is a legitimate email with a standard PDF attachment. The sender domain appears professional, the subject is appropriate, and PDF files are generally safe when they don't require additional actions.",
        "tip": "Legitimate PDF attachments from known services are typically safe. Always verify the sender and context before opening any attachment.",
    },
    {
        "id": 3,
        "title": "Disguised File Type (Phishing)",
        "sender": "hr.team@company-corporate.com",
        "subject": "Updated Salary Structure - Immediate Action Required",
        "message": "Please review updated salary structure effective immediately.",
        "attachment": "Salary_Update_2026.pdf.exe",
        "correct": "phishing",
        "feedback": "This is a double extension attack. The file appears to be a PDF but actually ends with .exe, making it an executable program. Attackers use this technique to trick users into running malware.",
        "tip": "Attackers hide malware using double extensions. Always check the full file name, not just the icon or first extension.",
    },
    {
        "id": 4,
        "title": "Safe Office Document (Safe)",
        "sender": "project.team@company-internal.com",
        "subject": "Project Timeline Update",
        "message": "Team,\nPlease find the updated project timeline for Q2. Review and let me know if you have any concerns about the deadlines.",
        "attachment": "Project_Timeline_Q2_2026.docx",
        "correct": "safe",
        "feedback": "This is a safe internal business email with a standard Word document (.docx). The sender appears to be internal, the context is appropriate for business communication, and .docx files don't contain macros by default.",
        "tip": "Internal business documents with standard extensions (.docx, .xlsx, .pptx) are generally safe. Be cautious with macro-enabled versions (.docm, .xlsm, .pptm).",
    },
    {
        "id": 5,
        "title": "Realistic Business Attack (Phishing)",
        "sender": "accounting@vendor-services.biz",
        "subject": "Invoice March 2026 - Payment Processing",
        "message": "Hi,\nPlease find attached invoice for last month's services. Kindly process payment today.",
        "attachment": "Invoice_March_2026.docm",
        "correct": "phishing",
        "feedback": "While this appears legitimate, .docm files contain macros that can execute malicious code. Even in business contexts, unexpected macro-enabled documents should be treated with suspicion.",
        "tip": "Macro-enabled documents (.docm, .xlsm) can contain malicious code. Verify the sender through another channel before enabling macros or opening such files.",
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

        /* Hide deploy button and toolbar */
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }
        [data-testid="stStatusWidget"] { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
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
            font-family: 'Aptos', 'Segoe UI', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 24px;
            color: rgba(167,243,255,.98);
            letter-spacing: .02em;
            text-shadow: 0 0 18px rgba(34,211,238,.20);
            font-weight: 500;
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

        .phish-link-card{
            margin-top: 0.75rem;
            padding: 1.5rem 1.25rem;
            border-radius: 14px;
            background: rgba(13,23,42,.90);
            border: 1px solid rgba(148,163,184,.45);
        }

        .phish-link-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            color: rgba(167,243,255,.96);
            font-size: 1.1rem;
            margin-bottom: .75rem;
        }

        .phish-url-display{
            border-radius: 10px;
            padding: 1rem 1rem;
            margin-bottom: 0.75rem;
            background: rgba(14,26,43,.88);
            border: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 18px 45px rgba(0,0,0,.45);
        }

        .phish-url-label{
            font-size: .75rem;
            text-transform: uppercase;
            letter-spacing: .12em;
            color: rgba(148,163,184,.95);
            margin-bottom: .5rem;
        }

        .phish-url-content{
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 18px;
            color: rgba(167,243,255,.98);
            word-break: break-all;
            line-height: 1.4;
        }

        .phish-url-actual{
            margin-top: 0.75rem;
            padding: 0.75rem;
            background: rgba(251,113,133,.10);
            border: 1px dashed rgba(251,113,133,.35);
            border-radius: 8px;
        }

        .phish-url-actual-label{
            font-size: .7rem;
            text-transform: uppercase;
            letter-spacing: .1em;
            color: rgba(251,113,133,.92);
            font-weight: 600;
            margin-bottom: .35rem;
        }

        .phish-url-actual-content{
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 15px;
            color: rgba(251,113,133,.96);
            word-break: break-all;
        }

        /* Interactive phishing link styles */
        .phishing-link {
            color: rgba(167,243,255,.98) !important;
            text-decoration: underline;
            text-decoration-color: rgba(34,211,238,.6);
            text-underline-offset: 4px;
            transition: all 0.3s ease;
            cursor: pointer;
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 18px;
            word-break: break-all;
            line-height: 1.4;
            position: relative;
        }

        .phishing-link:hover {
            color: rgba(34,211,238,1) !important;
            text-decoration-color: rgba(34,211,238,1);
            text-shadow: 0 0 8px rgba(34,211,238,.4);
        }

        .url-reveal-box {
            margin-top: 0.75rem;
            padding: 0.75rem;
            background: rgba(251,113,133,.10);
            border: 1px dashed rgba(251,113,133,.35);
            border-radius: 8px;
            animation: fadeIn 0.3s ease-in;
        }

        .url-reveal-label {
            font-size: .7rem;
            text-transform: uppercase;
            letter-spacing: .1em;
            color: rgba(251,113,133,.92);
            font-weight: 600;
            margin-bottom: .35rem;
        }

        .url-reveal-content {
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 15px;
            color: rgba(251,113,133,.96);
            word-break: break-all;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Attachment level styles */
        .phish-attachment-card{
            margin-top: 0.75rem;
            padding: 1.5rem 1.25rem;
            border-radius: 14px;
            background: rgba(13,23,42,.90);
            border: 1px solid rgba(148,163,184,.45);
        }

        .phish-attachment-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            color: rgba(167,243,255,.96);
            font-size: 1.1rem;
            margin-bottom: .75rem;
        }

        .phish-email-display{
            border-radius: 10px;
            padding: 1rem 1rem;
            margin-bottom: 0.75rem;
            background: rgba(14,26,43,.88);
            border: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 18px 45px rgba(0,0,0,.45);
        }

        .phish-email-header{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(34,211,238,.15);
        }

        .phish-email-sender{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: rgba(251,113,133,.96);
            font-weight: 600;
        }

        .phish-email-subject{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: rgba(167,243,255,.96);
            font-weight: 600;
        }

        .phish-email-body{
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 16px;
            color: rgba(167,243,255,.92);
            line-height: 1.5;
            margin-bottom: 1rem;
            white-space: pre-line;
        }

        .phish-attachment-display{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: rgba(251,113,133,.08);
            border: 1px dashed rgba(251,113,133,.35);
            border-radius: 8px;
            margin-top: 0.75rem;
        }

        .phish-attachment-icon{
            font-size: 24px;
            min-width: 24px;
        }

        .phish-attachment-name{
            font-family: 'JetBrains Mono', monospace;
            font-size: 16px;
            color: rgba(251,113,133,.96);
            font-weight: 600;
            word-break: break-all;
        }

        .phish-attachment-warning{
            font-size: 12px;
            color: rgba(251,113,133,.85);
            margin-top: 0.25rem;
            font-style: italic;
        }

        /* Message level styles */
        .phish-message-card{
            margin-top: 0.75rem;
            padding: 1.5rem 1.25rem;
            border-radius: 14px;
            background: rgba(13,23,42,.90);
            border: 1px solid rgba(148,163,184,.45);
        }

        .phish-message-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            color: rgba(167,243,255,.96);
            font-size: 1.1rem;
            margin-bottom: .75rem;
        }

        .phish-message-display{
            border-radius: 10px;
            padding: 1.5rem 1.25rem;
            margin-bottom: 0.75rem;
            background: rgba(14,26,43,.88);
            border: 1px solid rgba(34,211,238,.22);
            box-shadow: 0 18px 45px rgba(0,0,0,.45);
        }

        .phish-message-content{
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 16px;
            color: rgba(167,243,255,.92);
            line-height: 1.6;
            white-space: pre-line;
        }

        /* Password game style for Level 4 */
        .hints-master{
            background: rgba(14,26,43,.85);
            border: 1px solid rgba(34,211,238,.18);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,.45);
            padding: 20px;
            margin-bottom: 20px;
        }
        .hints-master.tier-secondary{
            border-color: rgba(168,85,247,.22);
        }
        .hints-master-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: rgba(34,211,238,.92);
            letter-spacing: .06em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .hints-master-level{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: rgba(167,243,255,.96);
            margin-bottom: 4px;
        }
        .hints-master-sub{
            font-size: 13px;
            color: rgba(148,163,184,.88);
            margin-bottom: 20px;
        }
        .hints-grid{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 20px;
        }
        .hint-card{
            background: rgba(14,26,43,.72);
            border: 1px solid rgba(34,211,238,.15);
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,.45);
        }
        .hint-card.primary{
            border-color: rgba(34,211,238,.22);
            background: rgba(14,26,43,.78);
        }
        .hint-title{
            font-family: 'Orbitron', system-ui, sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: rgba(34,211,238,.96);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: .06em;
        }
        .hint-content{
            font-family: 'Aptos', 'Segoe UI', ui-sans-serif;
            font-size: 14px;
            color: rgba(167,243,255,.92);
            line-height: 1.5;
        }
    </style>
    """
    st.markdown(cyber_css, unsafe_allow_html=True)

    # Add JavaScript for interactive link functionality
    js_code = """
    <script>
    function showActualUrl(element, actualUrl) {
        const revealBox = document.getElementById('url-reveal');
        const contentDiv = revealBox.querySelector('.url-reveal-content');
        contentDiv.textContent = actualUrl;
        revealBox.style.display = 'block';
    }
    
    function hideActualUrl(element) {
        const revealBox = document.getElementById('url-reveal');
        revealBox.style.display = 'none';
    }
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

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
    if "phishing_link_index" not in st.session_state:
        st.session_state.phishing_link_index = 0
    if "phishing_completed_links" not in st.session_state:
        st.session_state.phishing_completed_links = []
    if "phishing_attachment_index" not in st.session_state:
        st.session_state.phishing_attachment_index = 0
    if "phishing_completed_attachments" not in st.session_state:
        st.session_state.phishing_completed_attachments = []
    if "phishing_message_index" not in st.session_state:
        st.session_state.phishing_message_index = 0
    if "phishing_completed_messages" not in st.session_state:
        st.session_state.phishing_completed_messages = []
    if "phishing_game_mode" not in st.session_state:
        st.session_state.phishing_game_mode = 1  # 1 = Sender Pairs, 2 = Link Detection, 3 = Attachment Detection, 4 = Message Detection

    pair_index = st.session_state.phishing_pair_index
    link_index = st.session_state.phishing_link_index
    attachment_index = st.session_state.phishing_attachment_index
    message_index = st.session_state.phishing_message_index
    game_mode = st.session_state.phishing_game_mode
    
    pair = PHISHING_SENDER_PAIRS[pair_index] if game_mode == 1 else None
    link = PHISHING_LINK_SCENARIOS[link_index] if game_mode == 2 else None
    attachment = PHISHING_ATTACHMENT_SCENARIOS[attachment_index] if game_mode == 3 else None
    message = PHISHING_MESSAGE_SCENARIOS[message_index] if game_mode == 4 else None

    # Level navigation (6 sender pairs as Level 1, 5 links as Level 2, 5 attachments as Level 3, 5 messages as Level 4)
    current_level = pair_index + 1 if game_mode == 1 else link_index + 1 if game_mode == 2 else attachment_index + 1 if game_mode == 3 else message_index + 1
    level_title = "Level 1 - Sender Pairs" if game_mode == 1 else "Level 2 - Link Detection" if game_mode == 2 else "Level 3 - Attachment Detection" if game_mode == 3 else "Level 4 - Message Detection"
    completed_l1 = set(st.session_state.phishing_completed_pairs)
    completed_l2 = set(st.session_state.phishing_completed_links)
    completed_l3 = set(st.session_state.phishing_completed_attachments)
    completed_l4 = set(st.session_state.phishing_completed_messages)

    # Manual level switching - players choose their path

    # Header Section with title and subtitle
    st.markdown(
        """
        <style>
            .phish-hud-header{
                background: linear-gradient(180deg, rgba(14,26,43,.92), rgba(14,26,43,.62));
                padding: 38px 22px;
                border-radius: 16px;
                margin-bottom: 30px;
                margin-top: 0;
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
            <p class="phish-hud-sub">Choose your path! Level 1: <strong>Legitimate senders</strong>. Level 2: <strong>Hover links</strong> to check destinations. Level 3: <strong>Analyze attachments</strong> for malware risks. First sublevel of each level is always unlocked!</p>
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
            <div class='progress-value'>{level_title}</div>
            <div class='progress-description'>Progress: {len(completed_l1 | completed_l2 | completed_l3 | completed_l4)}/21 completed</div>
            <div class='attempt-badge'>Challenge {current_level}/{6 if game_mode == 1 else 5 if game_mode == 2 else 5 if game_mode == 3 else 5}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        st.markdown("""
        <div class='progress-card compact tier-secondary'>
            <div class='progress-label'>GAME RULES</div>
            <div class='progress-value'>How to Play</div>
            <div class='progress-description'>Choose any level! First sublevel of each level unlocked. Complete sublevels in order within each level.</div>
            <div class='attempt-badge'>Free exploration</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        total_completed = len(completed_l1) + len(completed_l2) + len(completed_l3) + len(completed_l4)
        if total_completed == 0:
            status_text = "Not started"
            status_color = "#94a3b8"
        elif total_completed == 21:
            status_text = "COMPLETE!"
            status_color = "#22c55e"
        else:
            status_text = f"{total_completed}/21 Done"
            status_color = "#60a5fa"
        
        st.markdown(f"""
        <div class='progress-card compact tier-secondary'>
            <div class='progress-label'>GAME STATUS</div>
            <div class='progress-value' style='color: {status_color};'>{status_text}</div>
            <div class='progress-description'>L1: {len(completed_l1)}/6 | L2: {len(completed_l2)}/5 | L3: {len(completed_l3)}/5 | L4: {len(completed_l4)}/5</div>
            <div class='attempt-badge'>Keep going!</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Level Navigation - Level 1
    st.markdown('<div class="section-header">Level 1 - Email Sender Pairs</div>', unsafe_allow_html=True)
    
    level_cols_l1 = st.columns(6)
    for i, col in enumerate(level_cols_l1, start=1):
        is_completed = i in completed_l1
        is_current = (i == current_level) and (game_mode == 1) and (len(completed_l1) < 6)
        is_unlocked = (i == 1) or (is_completed) or (i - 1 in completed_l1)
        border_color = "#22c55e" if is_completed else "#3b82f6" if (is_current or is_unlocked) else "#475569"
        if is_completed:
            status_text = "✅ COMPLETED"
        elif is_current and is_unlocked:
            status_text = "🎯 CURRENT"
        elif is_unlocked:
            status_text = "🟡 READY"
        else:
            status_text = "🔒 LOCKED"
        
        level_info = PHISHING_SENDER_PAIRS[i-1]
        
        with col:
            if is_unlocked and game_mode != 1:
                # Display card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color};'>
                        <div class='level-number'>L1-{i}</div>
                        <div class='level-status'>{level_info['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(59, 130, 246, 0.2)" if is_unlocked else "rgba(71, 85, 105, 0.2)"};'>{status_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Button inside the card area
                if st.button("Start", key=f"l1_card_{i}", use_container_width=True):
                    st.session_state.phishing_game_mode = 1
                    st.session_state.phishing_pair_index = i - 1
                    st.rerun()
            else:
                # Display-only card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color};'>
                        <div class='level-number'>L1-{i}</div>
                        <div class='level-status'>{level_info['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed else "rgba(59, 130, 246, 0.2)" if is_unlocked else "rgba(71, 85, 105, 0.2)"};'>{status_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # LEVEL 1 GAME/CHALLENGE
    if game_mode == 1:
        st.markdown(
            f"""
            <div class="phish-pair-card">
                <div class="phish-pair-title">Level 1 - Challenge {pair_index + 1}: {pair['title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2, vertical_alignment="top")

        # Container for feedback so it appears under the buttons with some spacing
        feedback_placeholder = st.container()

        def handle_choice_sender(choice: str) -> None:
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

                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(34,197,94,.92), rgba(34,197,94,.72)); border: 2px solid rgba(34,197,94,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(34,197,94,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #a7f3d0; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">✅ Correct Answer!</div>
                        <div style="color: rgba(167,243,255,.92); font-size: 14px; margin-top: 8px;">Great job! Moving to the next challenge...</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                if st.session_state.phishing_pair_index < len(PHISHING_SENDER_PAIRS) - 1:
                    st.session_state.phishing_pair_index += 1
                    st.rerun()
                else:
                    st.info("🎉 You completed all Level 1 challenges! Now unlock Level 2! 🚀")
            else:
                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(251,113,133,.92), rgba(251,113,133,.72)); border: 2px solid rgba(251,113,133,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(251,113,133,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #fca5a5; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">❌ Incorrect</div>
                        <div style="color: rgba(255,255,255,.92); font-size: 14px; margin-top: 8px;">Read the feedback and try again!</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

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
                handle_choice_sender("A")

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
                handle_choice_sender("B")

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # Level Navigation - Level 2
    st.markdown('<div class="section-header">Level 2 - Link Detection</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    level_cols_l2 = st.columns(5)
    for i, col in enumerate(level_cols_l2, start=1):
        is_completed_l2 = i in completed_l2
        is_current_l2 = (i == current_level) and (game_mode == 2) and (len(completed_l2) < 5)
        is_unlocked_l2 = (i == 1) or (is_completed_l2) or (i - 1 in completed_l2)
        border_color_l2 = "#22c55e" if is_completed_l2 else "#3b82f6" if (is_current_l2 or is_unlocked_l2) else "#475569"
        if is_completed_l2:
            status_text_l2 = "✅ COMPLETED"
        elif is_current_l2 and is_unlocked_l2:
            status_text_l2 = "🎯 CURRENT"
        elif is_unlocked_l2:
            status_text_l2 = "🟡 READY"
        else:
            status_text_l2 = "🔒 LOCKED"
        
        level_info_l2 = PHISHING_LINK_SCENARIOS[i-1]
        
        with col:
            if is_unlocked_l2 and game_mode != 2:
                # Display card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l2};'>
                        <div class='level-number'>L2-{i}</div>
                        <div class='level-status'>{level_info_l2['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(59, 130, 246, 0.2)" if is_unlocked_l2 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l2}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Button inside the card area
                if st.button("Start", key=f"l2_card_{i}", use_container_width=True):
                    st.session_state.phishing_game_mode = 2
                    st.session_state.phishing_link_index = i - 1
                    st.rerun()
            else:
                # Display-only card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l2};'>
                        <div class='level-number'>L2-{i}</div>
                        <div class='level-status'>{level_info_l2['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed_l2 else "rgba(59, 130, 246, 0.2)" if is_unlocked_l2 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l2}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # LEVEL 2 GAME/CHALLENGE
    if game_mode == 2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="phish-link-card">
                <div class="phish-link-title">Level 2 - Challenge {link_index + 1}: {link['title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="phish-url-display">
                <div class="phish-url-label">📧 Message says:</div>
                <div class="phish-url-content" style="color: rgba(167,243,255,.92); margin-bottom: 0.5rem;">{link['displayed_text']}</div>
                <div class="phish-url-label" style="margin-top: 0.75rem;">🔗 Interactive Link (hover to check real destination):</div>
                <div class="phish-url-content">
                    <a href="{link['actual_url']}" 
                       target="_blank" 
                       class="phishing-link"
                       onmouseover="showActualUrl(this, '{link['actual_url']}')"
                       onmouseout="hideActualUrl(this)">
                        {link['displayed_url']}
                    </a>
                    <div id="url-reveal" class="url-reveal-box" style="display: none;">
                        <div class="url-reveal-label">⚠️ Actual destination:</div>
                        <div class="url-reveal-content"></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_safe, col_phish = st.columns(2, vertical_alignment="center")
        feedback_placeholder_l2 = st.container()

        def handle_choice_link(choice: str) -> None:
            correct = link["correct"]
            is_correct = choice == correct
            with feedback_placeholder_l2:
                st.markdown(
                    f"""
                    <div class="phish-feedback">
                        <div class="phish-feedback-card {'ok' if is_correct else 'bad'}">
                            <div class="phish-feedback-title">
                                {"✅ Correct choice" if is_correct else "❌ Not quite, read the clues"}
                            </div>
                            <div class="phish-feedback-body">
                                {link['feedback']}
                            </div>
                            <div class="phish-feedback-tip">
                                <strong>Security tip:</strong> {link.get('tip', '')}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if is_correct:
                if current_level not in st.session_state.phishing_completed_links:
                    st.session_state.phishing_completed_links.append(current_level)

                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(34,197,94,.92), rgba(34,197,94,.72)); border: 2px solid rgba(34,197,94,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(34,197,94,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #a7f3d0; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">✅ Correct Answer!</div>
                        <div style="color: rgba(167,243,255,.92); font-size: 14px; margin-top: 8px;">Excellent! Moving to the next challenge...</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                if st.session_state.phishing_link_index < len(PHISHING_LINK_SCENARIOS) - 1:
                    st.session_state.phishing_link_index += 1
                    st.rerun()
                else:
                    st.info("🎉 You completed all Level 2 challenges! You're a phishing detection expert!")
            else:
                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(251,113,133,.92), rgba(251,113,133,.72)); border: 2px solid rgba(251,113,133,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(251,113,133,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #fca5a5; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">❌ Incorrect</div>
                        <div style="color: rgba(255,255,255,.92); font-size: 14px; margin-top: 8px;">Read the feedback and try again!</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

        with col_safe:
            if st.button("🟢 SAFE - Legitimate link", key=f"phish_safe_{link['id']}", use_container_width=True):
                handle_choice_link("safe")

        with col_phish:
            if st.button("🔴 PHISHING - Harmful link", key=f"phish_phishing_{link['id']}", use_container_width=True):
                handle_choice_link("phishing")

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # Level Navigation - Level 3
    st.markdown('<div class="section-header">Level 3 - Attachment Detection</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    level_cols_l3 = st.columns(5)
    for i, col in enumerate(level_cols_l3, start=1):
        is_completed_l3 = i in completed_l3
        is_current_l3 = (i == current_level) and (game_mode == 3) and (len(completed_l3) < 5)
        is_unlocked_l3 = (i == 1) or (is_completed_l3) or (i - 1 in completed_l3)
        border_color_l3 = "#22c55e" if is_completed_l3 else "#3b82f6" if (is_current_l3 or is_unlocked_l3) else "#475569"
        if is_completed_l3:
            status_text_l3 = "✅ COMPLETED"
        elif is_current_l3 and is_unlocked_l3:
            status_text_l3 = "🎯 CURRENT"
        elif is_unlocked_l3:
            status_text_l3 = "🟡 READY"
        else:
            status_text_l3 = "🔒 LOCKED"
        
        level_info_l3 = PHISHING_ATTACHMENT_SCENARIOS[i-1]
        
        with col:
            if is_unlocked_l3 and game_mode != 3:
                # Display card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l3};'>
                        <div class='level-number'>L3-{i}</div>
                        <div class='level-status'>{level_info_l3['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(59, 130, 246, 0.2)" if is_unlocked_l3 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l3}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Button inside the card area
                if st.button("Start", key=f"l3_card_{i}", use_container_width=True):
                    st.session_state.phishing_game_mode = 3
                    st.session_state.phishing_attachment_index = i - 1
                    st.rerun()
            else:
                # Display-only card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l3};'>
                        <div class='level-number'>L3-{i}</div>
                        <div class='level-status'>{level_info_l3['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed_l3 else "rgba(59, 130, 246, 0.2)" if is_unlocked_l3 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l3}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # LEVEL 3 GAME/CHALLENGE
    if game_mode == 3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="phish-attachment-card">
                <div class="phish-attachment-title">Level 3 - Challenge {attachment_index + 1}: {attachment['title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        # Determine file icon based on extension
        file_ext = attachment['attachment'].split('.')[-1].lower()
        file_icon = "📄"  # default
        if file_ext == 'zip':
            file_icon = "🗜️"
        elif file_ext == 'exe':
            file_icon = "⚠️"
        elif file_ext == 'docm':
            file_icon = "📝"
        elif file_ext == 'pdf':
            file_icon = "📋"
        elif file_ext == 'docx':
            file_icon = "📄"

        st.markdown(
            f"""
            <div class="phish-email-display">
                <div class="phish-email-header">
                    <div class="phish-email-sender">From: {attachment['sender']}</div>
                    <div class="phish-email-subject">{attachment['subject']}</div>
                </div>
                <div class="phish-email-body">{attachment['message']}</div>
                <div class="phish-attachment-display">
                    <div class="phish-attachment-icon">{file_icon}</div>
                    <div>
                        <div class="phish-attachment-name">{attachment['attachment']}</div>
                        <div class="phish-attachment-warning">⚠️ Exercise caution with email attachments</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_safe_att, col_phish_att = st.columns(2, vertical_alignment="center")
        feedback_placeholder_l3 = st.container()

        def handle_choice_attachment(choice: str) -> None:
            correct = attachment["correct"]
            is_correct = choice == correct
            with feedback_placeholder_l3:
                st.markdown(
                    f"""
                    <div class="phish-feedback">
                        <div class="phish-feedback-card {'ok' if is_correct else 'bad'}">
                            <div class="phish-feedback-title">
                                {"✅ Correct choice" if is_correct else "❌ Not quite, read the clues"}
                            </div>
                            <div class="phish-feedback-body">
                                {attachment['feedback']}
                            </div>
                            <div class="phish-feedback-tip">
                                <strong>Security tip:</strong> {attachment.get('tip', '')}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if is_correct:
                if current_level not in st.session_state.phishing_completed_attachments:
                    st.session_state.phishing_completed_attachments.append(current_level)

                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(34,197,94,.92), rgba(34,197,94,.72)); border: 2px solid rgba(34,197,94,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(34,197,94,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #a7f3d0; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">✅ Correct Answer!</div>
                        <div style="color: rgba(167,243,255,.92); font-size: 14px; margin-top: 8px;">Perfect! Moving to the next challenge...</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                if st.session_state.phishing_attachment_index < len(PHISHING_ATTACHMENT_SCENARIOS) - 1:
                    st.session_state.phishing_attachment_index += 1
                    st.rerun()
                else:
                    st.info("🎉 You completed all Level 3 challenges! You're now a complete phishing defense expert!")
            else:
                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(251,113,133,.92), rgba(251,113,133,.72)); border: 2px solid rgba(251,113,133,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(251,113,133,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #fca5a5; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">❌ Incorrect</div>
                        <div style="color: rgba(255,255,255,.92); font-size: 14px; margin-top: 8px;">Read the feedback and try again!</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

        with col_safe_att:
            if st.button("🟢 SAFE - Legitimate attachment", key=f"phish_safe_att_{attachment['id']}", use_container_width=True):
                handle_choice_attachment("safe")

        with col_phish_att:
            if st.button("🔴 PHISHING - Dangerous attachment", key=f"phish_phishing_att_{attachment['id']}", use_container_width=True):
                handle_choice_attachment("phishing")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Level Navigation - Level 4
    st.markdown('<div class="section-header">Level 4 - Message Detection</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    level_cols_l4 = st.columns(5)
    for i, col in enumerate(level_cols_l4, start=1):
        is_completed_l4 = i in completed_l4
        is_current_l4 = (i == current_level) and (game_mode == 4) and (len(completed_l4) < 5)
        is_unlocked_l4 = (i == 1) or (is_completed_l4) or (i - 1 in completed_l4)
        border_color_l4 = "#22c55e" if is_completed_l4 else "#3b82f6" if (is_current_l4 or is_unlocked_l4) else "#475569"
        if is_completed_l4:
            status_text_l4 = "✅ COMPLETED"
        elif is_current_l4 and is_unlocked_l4:
            status_text_l4 = "🎯 CURRENT"
        elif is_unlocked_l4:
            status_text_l4 = "🟡 READY"
        else:
            status_text_l4 = "🔒 LOCKED"
        
        level_info_l4 = PHISHING_MESSAGE_SCENARIOS[i-1]
        
        with col:
            if is_unlocked_l4 and game_mode != 4:
                # Display card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l4};'>
                        <div class='level-number'>L4-{i}</div>
                        <div class='level-status'>{level_info_l4['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(59, 130, 246, 0.2)" if is_unlocked_l4 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l4}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Button inside the card area
                if st.button("Start", key=f"l4_card_{i}", use_container_width=True):
                    st.session_state.phishing_game_mode = 4
                    st.session_state.phishing_message_index = i - 1
                    st.rerun()
            else:
                # Display-only card
                st.markdown(
                    f"""
                    <div class='level-card compact tier-tertiary' style='border-color: {border_color_l4};'>
                        <div class='level-number'>L4-{i}</div>
                        <div class='level-status'>{level_info_l4['title'].split('(')[0].strip()}</div>
                        <div class='level-button' style='background: {"rgba(34, 197, 94, 0.2)" if is_completed_l4 else "rgba(59, 130, 246, 0.2)" if is_unlocked_l4 else "rgba(71, 85, 105, 0.2)"};'>{status_text_l4}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # LEVEL 4 GAME/CHALLENGE
    if game_mode == 4:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='hints-master tier-secondary'>
              <div class='hints-master-title'>MESSAGE ANALYSIS // LEVEL {message_index + 1}</div>
              <div class='hints-master-level'>LEVEL {message_index + 1}</div>
              <div class='hints-master-sub'>Phishing detection challenge</div>
              <div class='hints-grid'>
                <div class='hint-card primary' style='grid-column: 1 / span 3;'>
                  <div class='hint-title'>{message['title']}</div>
                  <div class='hint-content' style='font-size: 18px; line-height: 1.6; text-align: left; white-space: pre-line;'>
                    {message['message']}
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_safe_msg, col_phish_msg = st.columns(2, vertical_alignment="center")
        feedback_placeholder_l4 = st.container()

        def handle_choice_message(choice: str) -> None:
            correct = message["correct"]
            is_correct = choice == correct
            with feedback_placeholder_l4:
                st.markdown(
                    f"""
                    <div class="phish-feedback">
                        <div class="phish-feedback-card {'ok' if is_correct else 'bad'}">
                            <div class="phish-feedback-title">
                                {"✅ Correct analysis" if is_correct else "❌ Not quite, review the message"}
                            </div>
                            <div class="phish-feedback-body">
                                {message['feedback']}
                            </div>
                            <div class="phish-feedback-tip">
                                <strong>Security tip:</strong> {message.get('tip', '')}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if is_correct:
                if current_level not in st.session_state.phishing_completed_messages:
                    st.session_state.phishing_completed_messages.append(current_level)

                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(34,197,94,.92), rgba(34,197,94,.72)); border: 2px solid rgba(34,197,94,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(34,197,94,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #a7f3d0; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">✅ Excellent Analysis!</div>
                        <div style="color: rgba(167,243,255,.92); font-size: 14px; margin-top: 8px;">You've mastered message detection! Moving to next challenge...</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                if st.session_state.phishing_message_index < len(PHISHING_MESSAGE_SCENARIOS) - 1:
                    st.session_state.phishing_message_index += 1
                    st.rerun()
                else:
                    st.info("🎉 Congratulations! You've completed ALL levels! You are now a complete phishing defense expert! 🏆")
            else:
                st.markdown(
                    """
                    <div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(180deg, rgba(251,113,133,.92), rgba(251,113,133,.72)); border: 2px solid rgba(251,113,133,.8); padding: 20px 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.5), 0 0 20px rgba(251,113,133,.3); z-index: 9999; animation: slideIn 0.3s ease-out;">
                        <div style="color: #fca5a5; font-size: 18px; font-weight: bold; font-family: Orbitron; letter-spacing: .06em; text-transform: uppercase;">❌ Analysis Error</div>
                        <div style="color: rgba(255,255,255,.92); font-size: 14px; margin-top: 8px;">Review the feedback and try again!</div>
                    </div>
                    <style>
                        @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

        with col_safe_msg:
            if st.button("🟢 LEGITIMATE - Safe message", key=f"phish_safe_msg_{message['id']}", use_container_width=True):
                handle_choice_message("safe")

        with col_phish_msg:
            if st.button("🔴 PHISHING - Scam message", key=f"phish_phishing_msg_{message['id']}", use_container_width=True):
                handle_choice_message("phishing")

