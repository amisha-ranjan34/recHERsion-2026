import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote

import streamlit as st
from modules.threat_analyzer import analyze_message

st.set_page_config(
    page_title="HERShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- DESIGN SYSTEM ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{color-scheme:dark;--bg:#070b18;--panel:#0d1428;--panel2:#111b34;--line:#26345b;--ink:#f4f6ff;--muted:#c0c9e4;--violet:#a78bfa;--violet2:#7c3aed;--cyan:#67e8f9;--pink:#f0abfc;--danger:#fb7185;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 10% 0%,rgba(91,33,182,.23),transparent 36%),radial-gradient(ellipse at 90% 8%,rgba(8,145,178,.13),transparent 30%),#070b18;color:var(--ink)}
[data-testid="stAppViewContainer"]{background:transparent}
[data-testid="stHeader"]{background:rgba(7,11,24,.75)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c1225 0%,#080d1b 100%);border-right:1px solid #26345b}
[data-testid="stSidebar"] > div:first-child{padding-top:1.4rem}
[data-testid="stSidebar"] h1{font-family:'Space Grotesk',sans-serif!important;font-size:1.55rem!important;color:#e9ddff!important;letter-spacing:-.7px}
[data-testid="stSidebar"] [data-testid="stRadio"]>label{color:#a9b8df!important;font-size:.72rem!important;font-weight:800!important;letter-spacing:1.4px;text-transform:uppercase}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"]{gap:5px}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border:1px solid transparent;border-radius:10px;padding:8px 10px;transition:all .18s ease}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#141f3b;border-color:#354675}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{color:#e2e8ff!important;font-weight:600}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){background:linear-gradient(90deg,rgba(124,58,237,.25),rgba(34,211,238,.08));border-color:#7354cf}
h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif!important;color:#f7f8ff;letter-spacing:-.45px}
h1{font-size:clamp(2rem,3vw,2.8rem)!important;font-weight:700!important}
h2{font-weight:650!important}
p,li,label,[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#e3e9ff}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p,.muted{color:var(--muted)!important}
.eyebrow{color:#a5b4fc;letter-spacing:2.2px;font-size:10px;font-weight:800;text-transform:uppercase}
.hero{position:relative;overflow:hidden;padding:clamp(24px,4vw,42px);border-radius:26px;background:linear-gradient(115deg,rgba(20,28,59,.98),rgba(37,24,80,.96) 55%,rgba(16,51,83,.95));border:1px solid #4b3c87;margin:8px 0 24px;box-shadow:0 20px 60px rgba(0,0,0,.25)}
.hero:after{content:'✦';position:absolute;right:5%;top:-28px;font-size:190px;line-height:1;color:rgba(165,180,252,.09);pointer-events:none}
.hero h1{color:#fff;font-size:clamp(2.2rem,4.5vw,3.45rem)!important;line-height:1.06;margin:12px 0 14px;max-width:850px}
.hero p{color:#e0e7ff;font-size:1rem;line-height:1.75;max-width:760px}
.card{background:linear-gradient(145deg,rgba(17,27,52,.97),rgba(11,17,34,.98));border:1px solid #29385f;border-radius:18px;padding:21px;min-height:160px;margin-bottom:12px;box-shadow:0 10px 28px rgba(0,0,0,.12);transition:transform .18s ease,border-color .18s ease}
.card:hover{border-color:#6d5bd0;transform:translateY(-2px)}
.card .emoji{font-size:28px;filter:drop-shadow(0 0 10px rgba(167,139,250,.18))}.card h3{font-size:18px;margin:11px 0 8px;color:#f7f8ff}.card p{color:#cbd5f1;font-size:13px;line-height:1.65}
.pill{display:inline-block;border:1px solid #5b4ca3;background:rgba(124,58,237,.16);color:#e9ddff;border-radius:99px;padding:4px 10px;font-size:10px;font-weight:800;letter-spacing:.8px}
.muted{color:#c0c9e4!important;font-size:13px;line-height:1.7}
div[data-testid="stMetric"]{background:linear-gradient(145deg,#111b34,#0d1428);border:1px solid #2b3a62;border-radius:16px;padding:17px 18px;box-shadow:0 10px 28px rgba(0,0,0,.12)}
div[data-testid="stMetricLabel"] p{color:#b9c7f0!important;font-size:12px!important;font-weight:700!important}
div[data-testid="stMetricValue"]{color:#fff!important;font-family:'Space Grotesk',sans-serif}
div[data-testid="stMetricDelta"]{color:#67e8f9!important}
.stButton>button,.stDownloadButton>button,.stLinkButton> a{border-radius:11px;min-height:43px;font-weight:700;border:1px solid #4b5c8b;background:#141f3b;color:#f7f8ff!important;transition:all .16s ease}
.stButton>button:hover,.stDownloadButton>button:hover,.stLinkButton> a:hover{border-color:#a78bfa;background:#20294b;color:white!important;box-shadow:0 0 0 1px rgba(167,139,250,.12)}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:linear-gradient(100deg,#6d28d9,#7c3aed 55%,#0891b2);color:#fff!important;border:1px solid #9b87f5;box-shadow:0 8px 22px rgba(124,58,237,.18)}
.stButton>button[kind="primary"]:hover{filter:brightness(1.12);box-shadow:0 0 22px rgba(124,58,237,.25)}
[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,[data-baseweb="select"]>div,[data-baseweb="select"] input{background:#0b1225!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border-color:#3b4b75!important;border-radius:10px!important}
[data-baseweb="input"] input::placeholder,[data-baseweb="textarea"] textarea::placeholder{color:#aab7d6!important;opacity:1!important}
[data-testid="stWidgetLabel"] p,[data-testid="stTextInput"] label,[data-testid="stTextArea"] label,[data-testid="stSelectbox"] label,[data-testid="stNumberInput"] label,[data-testid="stCheckbox"] label,[data-testid="stRadio"] label{color:#e6ebff!important;font-weight:600}
[data-testid="stAlert"]{border-radius:13px;border:1px solid #3b4b75;background:#111b34}
[data-testid="stAlert"] p{color:#f0f4ff!important}
[data-testid="stExpander"]{border:1px solid #2e3e67;border-radius:13px;background:rgba(13,20,40,.75)}
[data-testid="stExpander"] summary p{color:#f0f4ff!important}
[data-testid="stProgressBar"]>div{background:#202c4a;border-radius:99px}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#8b5cf6,#22d3ee);border-radius:99px}
hr{border-color:#28385e!important}
[data-testid="stDataFrame"],[data-testid="stTable"]{color:#f4f6ff}
:focus-visible{outline:2px solid #67e8f9!important;outline-offset:2px!important}
@media(max-width:768px){.hero{padding:24px;border-radius:20px}.card{padding:17px;min-height:140px}}
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
DEFAULTS = {
    "page": "Overview",
    "notes": [],
    "timer": None,
    "walk": None,
    "history": [],
    "last_scan": None,
    "sos_demo_count": 0,
    "fake_call": None,
    "digital_checks": {},
    "safety_plan": None,
    "trusted_contacts": [],
    "codeword_messages": {},
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

PAGES = [
    "Overview", "SOS Demo", "Safe Walk", "Fake Call",
    "Threat Scanner", "Evidence Vault", "Digital Safety",
    "Safety Plan", "Trusted Circle", "Codeword Signals",
    "Incident Insights", "Nearby Help", "Complaint Draft", "Privacy & Help"
]

def goto(page):
    st.session_state.page = page
    st.rerun()

def page_header(kicker, title, subtitle):
    st.markdown(f'<div class="eyebrow">{kicker}</div><h1 style="margin:5px 0">{title}</h1><p class="muted">{subtitle}</p>', unsafe_allow_html=True)

def card(icon, title, description, tag="SAFETY TOOL"):
    st.markdown(f'<div class="card"><div class="emoji">{icon}</div><h3>{title}</h3><p>{description}</p><span class="pill">{tag}</span></div>', unsafe_allow_html=True)

def add_note(text, category="Incident", priority="Medium"):
    st.session_state.notes.insert(0, {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "category": category,
        "priority": priority,
        "text": text.strip(),
    })

def analyze_local(text):
    """Combine existing analyzer with extra English/Hinglish safety signals."""
    base = analyze_message(text)
    patterns = [
        (r"(photo|video|pic|nude|mms).{0,50}(leak|viral|expose|upload|post)|blackmail|nangi|paise do|pay me or", 30, "Blackmail or intimate-image threat"),
        (r"\b(kill|rape|acid|maar daal|jaan se|dekh lunga|dekh lungi|ghar aa jaunga|ghar aa jaungi)\b", 30, "Threat of violence"),
        (r"(following you|watching you|tracking you|peechha|peecha|location bhej|where are you)", 20, "Possible stalking or location pressure"),
        (r"(don't tell|do not tell|kisi ko mat batana|warna|or else|keep it secret)", 15, "Coercion or secrecy pressure"),
        (r"(otp|aadhaar|aadhar|pan card|kyc|verify now|account.{0,20}(blocked|suspended)|password)", 20, "Possible phishing or identity misuse"),
        (r"(send (me )?(pics?|photos?|nudes?)|sexy|figure|rate you|raat ko mil)", 15, "Possible sexual harassment"),
    ]
    hits = []
    score = int(base.get("score", 0))
    for pattern, points, label in patterns:
        if re.search(pattern, text, re.I):
            hits.append(label)
            score += points
    # Keep base signals while avoiding duplicate labels.
    signals = list(dict.fromkeys(list(base.get("signals", [])) + hits))
    score = min(score, 100)
    if score >= 70:
        label = "High warning level"
    elif score >= 35:
        label = "Caution advised"
    elif score > 0:
        label = "Some warning signals"
    else:
        label = "Few configured signals found"
    return {"score": score, "label": label, "signals": signals}

with st.sidebar:
    st.markdown("# 🛡️ HERShield AI")
    st.caption("YOUR SAFETY. YOUR CONTROL.")
    st.markdown('<span class="pill">REC HERS ’26 · PS2</span>', unsafe_allow_html=True)
    st.divider()
    selected = st.radio("YOUR WORKSPACE", PAGES, index=PAGES.index(st.session_state.page))
    st.session_state.page = selected
    st.divider()
    st.metric("Evidence notes", len(st.session_state.notes))
    st.metric("Messages scanned", len(st.session_state.history))
    st.caption("Prototype • Session-based data")
    st.warning("SOS is simulated. This app does not notify contacts or emergency services.")

page = st.session_state.page

# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">A SMARTER, CALMER SAFETY WORKSPACE</div>
      <h1>Your safety. Your control.<br>Your shield.</h1>
      <p>Journey check-ins, threat warnings, incident notes and digital-safety guidance
      brought together in one privacy-conscious prototype.</p>
      <span class="pill">PRIVACY-FIRST PROTOTYPE</span>
    </div>
    """, unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    a.metric("Safety modules", "06")
    b.metric("Evidence notes", len(st.session_state.notes), "Current session")
    c.metric("Threat scans", len(st.session_state.history), "Current session")
    d.metric("Trusted contacts", len(st.session_state.trusted_contacts))
    st.subheader("Your safety workspace")
    rows = [
        [("🚨","SOS Demo","Explore the emergency-style interface without sending a real alert.","DEMO"),
         ("🚶","Safe Walk","Set a journey countdown and check in when you arrive.","CHECK-IN"),
         ("📞","Fake Call","Simulate an incoming-call screen for a demo scenario.","SIMULATION")],
        [("🔎","Threat Scanner","Check English and Hinglish text for configured warning patterns.","ANALYSIS"),
         ("🗂️","Evidence Vault","Timestamp and export incident notes from this session.","SESSION NOTES"),
         ("🔐","Digital Safety","Review account, privacy and evidence checklist items.","CHECKLIST")],
        [("🧭","Safety Plan","Create a personal check-in message and backup plan.","PERSONAL PLAN"),
         ("👥","Trusted Circle","Keep trusted contact details handy and prepare a message.","CONTACTS"),
         ("🗝️","Codeword Signals","Create discreet pre-agreed phrases for check-ins.","QUICK SIGNAL")],
        [("📈","Incident Insights","Review logged incidents by category and priority.","PATTERN REVIEW"),
         ("📍","Nearby Help","Open maps for nearby police, hospitals and pharmacies.","MAP LINKS"),
         ("📄","Complaint Draft","Turn session notes into an editable incident report.","EXPORT")]
    ]
    for row in rows:
        cols = st.columns(3)
        for col, item in zip(cols, row):
            with col:
                card(*item)
                if st.button("Open " + item[1], key="open_"+item[1], use_container_width=True):
                    goto(item[1])
    st.info("If you are in immediate danger, contact local emergency services or a trusted person. Do not rely on this prototype as an emergency service.")

# ---------------- SOS DEMO ----------------
elif page == "SOS Demo":
    page_header("EMERGENCY UI · DEMONSTRATION", "🚨 SOS Demo", "A clear emergency-style screen for your hackathon presentation.")
    st.markdown('<div class="card"><div class="eyebrow">DEMO MODE</div><h2>Need help?</h2><p>This button only shows a local demonstration. It does not call anyone, share location, send SMS or notify emergency services.</p></div>', unsafe_allow_html=True)
    st.markdown("### Emergency actions (demo only)")
    if st.button("Activate SOS demonstration", type="primary", use_container_width=True):
        st.session_state.sos_demo_count += 1
        add_note("SOS demonstration activated (no alert was sent).", "SOS demo", "High")
        st.error("DEMO ONLY — no call, message, location or emergency alert has been sent.")
        st.write("For a real emergency, use your phone's emergency calling feature or contact local emergency services/trusted person.")
    st.metric("Demo activations this session", st.session_state.sos_demo_count)
    st.caption("No live location access or trusted-contact sharing is implemented.")

# ---------------- SAFE WALK ----------------
elif page == "Safe Walk":
    page_header("PLAN · CHECK IN · REVIEW", "🚶 Safe Walk", "Create a local countdown for a planned journey.")
    with st.form("walk_form"):
        destination = st.text_input("Destination label (optional)", placeholder="e.g. Hostel")
        minutes = st.number_input("Expected duration (minutes)", min_value=1, max_value=240, value=15, step=1)
        submitted = st.form_submit_button("Start Safe Walk", type="primary", use_container_width=True)
    if submitted:
        now = datetime.now()
        st.session_state.walk = {
            "destination": destination.strip(),
            "deadline": (now + timedelta(minutes=int(minutes))).isoformat(),
            "duration": int(minutes),
            "started": now.isoformat(timespec="seconds")
        }
        st.rerun()
    def render_active_walk():
        walk = st.session_state.walk
        if not walk:
            st.markdown(
                '<div class="card"><div class="emoji">🌙</div><h3>No active walk</h3>'
                '<p>Set an expected duration above to start a local check-in countdown.</p></div>',
                unsafe_allow_html=True,
            )
            return

        deadline = datetime.fromisoformat(walk["deadline"])
        remaining = max(0, int((deadline - datetime.now()).total_seconds()))
        st.markdown("### Current walk")
        a, b, c = st.columns(3)
        a.metric("Destination", walk["destination"] or "Not specified")
        b.metric("Check-in deadline", deadline.strftime("%I:%M %p"))
        c.metric("Time remaining", f"{remaining // 60:02d}:{remaining % 60:02d}")
        total_seconds = max(1, int(walk.get("duration", 15)) * 60)
        st.progress(min(1.0, max(0.0, remaining / total_seconds)))

        if remaining > 0:
            st.info(
                "Live countdown refreshes while this page is open. "
                "This prototype does not send background alerts or contact emergency services."
            )
        else:
            st.warning(
                "⏰ Check-in deadline passed. No alert has been sent. "
                "If you need help, contact your trusted person or local emergency services."
            )

        x, y = st.columns(2)
        with x:
            if st.button("✅ I'm safe — end walk", type="primary", use_container_width=True, key="walk_safe"):
                add_note(
                    "Safe Walk completed: " + (walk["destination"] or "destination not specified"),
                    "Safe Walk",
                    "Low",
                )
                st.session_state.walk = None
                st.success("Glad you're safe. Walk closed.")
                st.rerun()
        with y:
            if st.button("＋ Add 5 minutes", use_container_width=True, key="walk_extend"):
                current_deadline = datetime.fromisoformat(st.session_state.walk["deadline"])
                new_deadline = max(datetime.now(), current_deadline) + timedelta(minutes=5)
                st.session_state.walk["deadline"] = new_deadline.isoformat()
                st.session_state.walk["duration"] = max(
                    1, int((new_deadline - datetime.fromisoformat(st.session_state.walk["started"])).total_seconds() // 60)
                )
                st.rerun()

        if st.button("Cancel walk timer", key="walk_cancel"):
            st.session_state.walk = None
            st.rerun()

    # Streamlit fragments refresh this section every second on supported versions.
    if hasattr(st, "fragment"):
        render_active_walk = st.fragment(run_every="1s")(render_active_walk)
    else:
        st.caption("For a live countdown, update Streamlit to a version that supports fragments.")
    render_active_walk()

# ---------------- FAKE CALL ----------------
elif page == "Fake Call":
    page_header("PERSONAL SPACE · SIMULATION", "📞 Fake Call", "Simulate an incoming-call screen for a demo or role-play.")
    st.info("This is a visual simulation only. It does not place or receive a real phone call.")
    with st.form("fake_call_form"):
        caller = st.text_input("Caller display name", "Home")
        delay = st.selectbox("Simulated ring delay", ["Ring now", "After 10 seconds", "After 30 seconds"])
        run_call = st.form_submit_button("Prepare fake call", type="primary", use_container_width=True)
    if run_call:
        delay_seconds = {"Ring now": 0, "After 10 seconds": 10, "After 30 seconds": 30}[delay]
        st.session_state.fake_call = {
            "caller": caller.strip() or "Unknown caller",
            "delay": delay,
            "prepared_at": datetime.now().isoformat(timespec="seconds"),
            "ready_at": (datetime.now() + timedelta(seconds=delay_seconds)).isoformat()
        }
        st.rerun()
    call = st.session_state.fake_call
    if call:
        ready_at = datetime.fromisoformat(call["ready_at"])
        if datetime.now() >= ready_at:
            st.markdown(f"""
            <div style="background:linear-gradient(150deg,#171a28,#22233a);border:1px solid #47415f;border-radius:25px;padding:36px;text-align:center">
              <div style="width:88px;height:88px;border-radius:50%;background:#66518e;display:flex;align-items:center;justify-content:center;margin:auto;font-size:35px">☎</div>
              <h2 style="margin-top:20px">{call['caller']}</h2>
              <p class="muted">Incoming call · Simulation</p>
            </div>
            """, unsafe_allow_html=True)
            a, b = st.columns(2)
            with a:
                if st.button("🟢 Answer simulation", type="primary", use_container_width=True):
                    st.session_state.fake_call = None
                    st.success("Fake call answered in the demo.")
                    st.rerun()
            with b:
                if st.button("🔴 Decline", use_container_width=True):
                    st.session_state.fake_call = None
                    st.rerun()
        else:
            st.warning(f"Demo call prepared for {call['caller']}. It will be ready at {ready_at.strftime('%I:%M:%S %p')}.")
            st.caption("Streamlit does not guarantee a timed popup while idle. Click a page control or rerun after the selected delay.")
            if st.button("Show incoming call now"):
                st.session_state.fake_call["ready_at"] = datetime.now().isoformat()
                st.rerun()
            if st.button("Cancel fake call"):
                st.session_state.fake_call = None
                st.rerun()

# ---------------- THREAT SCANNER ----------------
elif page == "Threat Scanner":
    page_header("PAUSE · CHECK · DECIDE", "🔎 Threat Scanner", "Check for configured English and Hinglish warning patterns. Use fictional examples in demos.")
    with st.form("scanner_form"):
        message = st.text_area("Paste message text", height=170, placeholder="Example: OTP bhejo warna account block ho jayega...")
        scan = st.form_submit_button("Scan message", type="primary", use_container_width=True)
    if scan:
        if not message.strip():
            st.warning("Paste a message first.")
        else:
            result = analyze_local(message)
            record = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "time": datetime.now().isoformat(timespec="seconds"),
                "score": result["score"],
                "label": result["label"],
                "signals": result["signals"],
                "message": message[:500]
            }
            st.session_state.history.insert(0, record)
            st.session_state.last_scan = record
            st.rerun()
    result = st.session_state.last_scan
    if result:
        st.markdown("### Latest scan")
        a, b = st.columns([1, 2])
        a.metric("Warning score", f"{result['score']}/100")
        a.progress(result["score"] / 100)
        with b:
            st.subheader(result["label"])
            if result["score"] >= 70:
                st.error("High warning level — pause and verify independently.")
            elif result["score"] >= 35:
                st.warning("Caution advised — review carefully.")
            else:
                st.info("Few configured signals found. This does not prove safety.")
        if result["signals"]:
            st.markdown("**Signals detected**")
            for signal in result["signals"]:
                st.write("⚠️ " + signal)
        else:
            st.write("No configured warning patterns detected.")
        st.caption("This is heuristic pattern matching, not a trained AI model or calibrated probability.")
        x, y = st.columns(2)
        with x:
            if st.button("Save scan to Evidence Vault", use_container_width=True):
                add_note(f"Threat scan ({result['label']}, {result['score']}/100): {result['message']}", "Threat scan", "High" if result["score"] >= 70 else "Medium")
                st.success("Saved to the current session.")
        with y:
            if st.button("Clear latest result", use_container_width=True):
                st.session_state.last_scan = None
                st.rerun()
    with st.expander("Recent scans"):
        if not st.session_state.history:
            st.caption("No scans yet.")
        for item in st.session_state.history[:8]:
            st.write(f"**{item['time']}** · {item['label']} · {item['score']}/100")
            st.caption(item["message"][:160])
    st.info("Never share OTPs, passwords, PINs or banking credentials with an unverified sender.")

# ---------------- EVIDENCE VAULT ----------------
elif page == "Evidence Vault":
    page_header("DOCUMENT · EXPORT · DELETE", "🗂️ Evidence Vault", "Organize notes in the current session. Avoid entering sensitive personal details in a public demo.")
    with st.form("vault_form", clear_on_submit=True):
        category = st.selectbox("Entry type", ["Harassment", "Threatening message", "Suspicious contact", "Unsafe journey", "SOS demo", "Other"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        text = st.text_area("Incident notes", height=120, placeholder="What happened? Add only details you are comfortable storing in this demo.")
        save = st.form_submit_button("Save timestamped entry", type="primary", use_container_width=True)
    if save:
        if text.strip():
            add_note(text, category, priority)
            st.success("Entry saved in this session.")
            st.rerun()
        else:
            st.warning("Enter a note first.")
    st.metric("Saved entries", len(st.session_state.notes))
    if st.session_state.notes:
        st.download_button("⬇ Export vault as JSON", json.dumps(st.session_state.notes, indent=2, ensure_ascii=False), "hershield_evidence_vault.json", "application/json", use_container_width=True)
        for note in st.session_state.notes:
            with st.expander(f"{note['timestamp']} · {note['category']} · {note['priority']}"):
                st.write(note["text"])
                if st.button("Delete this entry", key="delete_"+note["id"]):
                    st.session_state.notes = [n for n in st.session_state.notes if n["id"] != note["id"]]
                    st.rerun()
        if st.button("Delete all vault entries"):
            st.session_state.notes = []
            st.rerun()
    else:
        st.info("No entries saved yet.")
    st.caption("Session storage is not encrypted long-term evidence storage. Exported JSON may contain sensitive text.")

# ---------------- DIGITAL SAFETY ----------------
elif page == "Digital Safety":
    page_header("CHECK · IMPROVE · REVIEW", "🔐 Digital Safety Check", "Review practical account and privacy habits. This checklist is guidance, not a security audit.")
    questions = [
        "Two-factor authentication is enabled on key accounts",
        "My social profiles are private or friends-only where appropriate",
        "I avoid sharing live location publicly",
        "I review photo location-tagging settings",
        "I use unique passwords for important accounts",
        "I know how to block and report abusive accounts",
        "I know how to preserve screenshots of threats",
    ]
    checked = st.session_state.digital_checks
    for i, question in enumerate(questions):
        checked[str(i)] = st.checkbox(question, value=checked.get(str(i), False), key=f"digital_{i}")
    count = sum(bool(checked.get(str(i), False)) for i in range(len(questions)))
    st.markdown("### Your privacy checklist")
    st.metric("Items reviewed", f"{count}/{len(questions)}")
    st.progress(count / len(questions))
    if count == len(questions):
        st.success("All checklist items marked. Consider reviewing them periodically.")
    else:
        next_item = next((q for i, q in enumerate(questions) if not checked.get(str(i), False)), None)
        st.info("Suggested next review: " + next_item)
    st.caption("Your selections stay in this app session; no account settings are changed automatically.")

# ---------------- PERSONAL SAFETY PLAN ----------------
elif page == "Safety Plan":
    page_header("PREPARE · CHECK IN · STAY CONNECTED", "🧭 Personal Safety Plan", "Create a small plan you can copy or share with a trusted person. Nothing is sent automatically.")
    st.markdown('<div class="card"><div class="eyebrow">YOUR PLAN, YOUR CHOICE</div><h3>Make the next step easier to remember</h3><p>Choose a trusted contact, set a check-in time, and agree on a code word or phrase with someone you trust. Avoid putting passwords, OTPs, or unnecessary private details here.</p></div>', unsafe_allow_html=True)
    with st.form("safety_plan_form"):
        contact = st.text_input("Trusted contact label", placeholder="e.g. Sister / close friend")
        destination = st.text_input("Destination or journey label", placeholder="e.g. Leaving campus for home")
        checkin = st.text_input("Expected check-in time", placeholder="e.g. 8:30 PM")
        codeword = st.text_input("Optional code word", placeholder="A phrase only you and your contact understand")
        backup = st.text_area("Backup steps", placeholder="e.g. If I miss check-in, try calling me; if still worried, follow the plan we agreed on.", height=90)
        plan_submit = st.form_submit_button("Create my safety card", type="primary", use_container_width=True)
    if plan_submit:
        safe_contact = contact.strip() or "[trusted contact]"
        safe_destination = destination.strip() or "[journey / destination]"
        safe_checkin = checkin.strip() or "[check-in time]"
        safe_codeword = codeword.strip() or "[not set]"
        safe_backup = backup.strip() or "Follow the backup steps agreed with my trusted contact."
        st.session_state.safety_plan = {
            "contact": safe_contact,
            "destination": safe_destination,
            "checkin": safe_checkin,
            "codeword": safe_codeword,
            "backup": safe_backup,
            "created": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        }
        st.rerun()
    plan = st.session_state.safety_plan
    if plan:
        card_text = ("HERShield AI — PERSONAL SAFETY CARD\n\n"
                     f"Trusted contact: {plan['contact']}\n"
                     f"Journey: {plan['destination']}\n"
                     f"Expected check-in: {plan['checkin']}\n"
                     f"Code word: {plan['codeword']}\n\n"
                     f"Backup steps: {plan['backup']}\n\n"
                     "Note: This card does not send alerts or share live location.")
        st.markdown("### Your safety card")
        st.code(card_text, language="text")
        st.download_button("⬇ Download safety card", card_text, "hershield_safety_card.txt", "text/plain", use_container_width=True)
        message_text = f"Hi {plan['contact']}, I'm planning: {plan['destination']}. Please expect my check-in by {plan['checkin']}. If you don't hear from me, follow the backup steps we've agreed on."
        st.markdown("### Check-in message")
        st.text_area("Copy this message to send yourself", value=message_text, height=100, key="safety_checkin_message")
        st.caption("The app does not send this message. Copy it into your preferred messaging app if you choose.")
        if st.button("Clear safety card"):
            st.session_state.safety_plan = None
            st.rerun()


# ---------------- TRUSTED CIRCLE ----------------
elif page == "Trusted Circle":
    page_header("PEOPLE YOU TRUST · READY-TO-COPY MESSAGES", "👥 Trusted Circle", "Keep a small list of people you trust and prepare a check-in message. This prototype never sends messages automatically.")
    st.info("Contact details are kept only in this Streamlit session. Avoid using a shared/public computer for real personal details.")
    with st.form("trusted_contact_form", clear_on_submit=True):
        cname = st.text_input("Contact name or label", placeholder="e.g. Sister / roommate")
        cphone = st.text_input("Phone number with country code", placeholder="e.g. 919876543210")
        csubmit = st.form_submit_button("Add trusted contact", type="primary", use_container_width=True)
    if csubmit:
        digits = re.sub(r"\D", "", cphone)
        if not cname.strip() or len(digits) < 8:
            st.error("Enter a contact label and a valid phone number including country code.")
        else:
            st.session_state.trusted_contacts.append({"id": datetime.now().strftime("%Y%m%d%H%M%S%f"), "name": cname.strip(), "phone": digits})
            st.success("Contact added to this session.")
            st.rerun()
    contacts = st.session_state.trusted_contacts
    if contacts:
        for contact in contacts:
            with st.container(border=True):
                left, right = st.columns([4, 1])
                with left:
                    st.markdown(f"**{contact['name']}**")
                    st.caption("+" + contact["phone"])
                with right:
                    if st.button("Remove", key="remove_contact_" + contact["id"]):
                        st.session_state.trusted_contacts = [c for c in contacts if c["id"] != contact["id"]]
                        st.rerun()
        st.subheader("Prepare a check-in message")
        contact_names = [c["name"] for c in contacts]
        chosen = st.selectbox("Choose recipient", contact_names)
        destination = st.text_input("Where are you going? (optional)", placeholder="e.g. Heading back to hostel")
        eta = st.text_input("Expected check-in time", placeholder="e.g. 8:30 PM")
        custom = st.text_area("Extra note (optional)", placeholder="e.g. I'll message you when I arrive.")
        chosen_contact = next(c for c in contacts if c["name"] == chosen)
        message = f"Hi {chosen_contact['name']}, I'm {destination.strip() or 'on my way'}. My expected check-in is {eta.strip() or 'not set'}. {custom.strip()} Please check in with me if you don't hear from me."
        st.text_area("Message preview", value=message, height=110, key="trusted_message_preview")
        st.link_button("Open WhatsApp with this message", "https://wa.me/" + chosen_contact["phone"] + "?text=" + quote(message), use_container_width=True)
        st.caption("This opens WhatsApp with a prefilled message. You must review and press Send yourself.")
    else:
        st.markdown('<div class="card"><div class="emoji">👥</div><h3>Your trusted circle starts here</h3><p>Add a person you trust, then prepare a check-in message before a journey.</p></div>', unsafe_allow_html=True)

# ---------------- CODEWORD SIGNALS ----------------
elif page == "Codeword Signals":
    page_header("PRE-AGREE · KEEP IT SIMPLE", "🗝️ Codeword Signals", "Agree on meanings with your trusted person beforehand. A phrase alone does not notify anyone.")
    st.warning("Use codewords only with people who already understand the plan. The app does not detect phrases in other apps or send alerts in the background.")
    defaults = {
        "Yellow": "Call me with an excuse to leave",
        "Orange": "Please come and pick me up",
        "Red": "I need help now — call me and follow our agreed plan",
    }
    for level, meaning in defaults.items():
        with st.container(border=True):
            st.markdown(f"### {level}")
            st.caption(meaning)
            value = st.text_input("Message phrase", value=st.session_state.codeword_messages.get(level, {
                "Yellow": "Can you call me in two minutes?",
                "Orange": "Did you remember the books? I'm ready to leave.",
                "Red": "Please call me now. It's urgent.",
            }[level]), key="codeword_" + level)
            st.session_state.codeword_messages[level] = value
            if st.session_state.trusted_contacts:
                target = st.selectbox("Trusted contact", [c["name"] for c in st.session_state.trusted_contacts], key="cw_target_" + level)
                person = next(c for c in st.session_state.trusted_contacts if c["name"] == target)
                st.link_button("Prepare WhatsApp message", "https://wa.me/" + person["phone"] + "?text=" + quote(value), key="cw_link_" + level, use_container_width=True)
            else:
                st.caption("Add a contact in Trusted Circle to prepare a message link.")

# ---------------- INCIDENT INSIGHTS ----------------
elif page == "Incident Insights":
    page_header("NOTICE PATTERNS · NOT PREDICTIONS", "📈 Incident Insights", "A simple summary of entries you chose to log. This is not a risk prediction or legal assessment.")
    notes = st.session_state.notes
    if not notes:
        st.info("No incident notes yet. Add a note in Evidence Vault to see a summary.")
    else:
        import pandas as pd
        df = pd.DataFrame(notes)
        a, b, c = st.columns(3)
        a.metric("Logged entries", len(notes))
        b.metric("High priority", sum(n.get("priority") == "High" for n in notes))
        c.metric("Categories", df["category"].nunique())
        st.subheader("Entries by category")
        st.bar_chart(df["category"].value_counts())
        st.subheader("Entries by priority")
        st.bar_chart(df["priority"].value_counts())
        dated = []
        for n in notes:
            try:
                dated.append(datetime.fromisoformat(n["timestamp"]).date().isoformat())
            except (ValueError, TypeError, KeyError):
                pass
        if dated:
            st.subheader("Logged entries over time")
            st.line_chart(pd.Series(dated).value_counts().sort_index())
        st.caption("Counts reflect only the notes in this session. A small sample can be misleading; use this view to organize records, not infer danger.")
        st.download_button("Download incident summary CSV", df.to_csv(index=False).encode("utf-8"), "hershield_incident_summary.csv", "text/csv", use_container_width=True)

# ---------------- NEARBY HELP ----------------
elif page == "Nearby Help":
    page_header("LOCAL OPTIONS · VERIFY BEFORE TRAVEL", "📍 Nearby Help", "Open map searches for nearby services. Check the result and current availability yourself.")
    st.markdown('<div class="card"><div class="emoji">🚨</div><h3>Immediate danger?</h3><p>Use your phone’s emergency calling feature or contact a trusted person. Do not rely on this prototype as an emergency service.</p></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.link_button("Police stations", "https://www.google.com/maps/search/police+station+near+me", use_container_width=True)
    with b:
        st.link_button("Hospitals", "https://www.google.com/maps/search/hospital+near+me", use_container_width=True)
    with c:
        st.link_button("Pharmacies", "https://www.google.com/maps/search/pharmacy+near+me", use_container_width=True)
    st.subheader("Useful India contacts")
    st.markdown("""
    - **112** — Emergency response number
    - **181** — Women Helpline (availability can vary by state)
    - **1930** — Cyber financial fraud helpline
    """)
    st.caption("Verify current helpline details through official government sources. The app does not place calls.")

# ---------------- COMPLAINT DRAFT ----------------
elif page == "Complaint Draft":
    page_header("ORGANIZE · REVIEW · EXPORT", "📄 Complaint Draft", "Generate an editable draft from notes saved in this session. Review carefully before using.")
    name = st.text_input("Your name (optional)", placeholder="Leave blank for a placeholder")
    authority = st.text_input("Address to (optional)", "The Officer-in-Charge / Cyber Crime Cell")
    if st.button("Generate draft", type="primary", use_container_width=True):
        who = name.strip() or "[Your name]"
        lines = [
            "To,",
            authority.strip() or "The appropriate authority",
            "",
            "Subject: Request to report harassment, threats, or suspicious activity",
            "",
            f"I, {who}, wish to report the following incident(s). The information below is a draft based on notes recorded in my HERShield AI session.",
            "",
        ]
        if st.session_state.notes:
            for i, note in enumerate(reversed(st.session_state.notes), start=1):
                lines.append(f"{i}. [{note['timestamp']}] [{note['category']}, priority: {note['priority']}] {note['text']}")
        else:
            lines.append("[Add the factual timeline and incident details here.]")
        scan = st.session_state.last_scan
        if scan:
            lines.extend(["", f"Recent message scan: {scan['label']} ({scan['score']}/100).", "Warning signals: " + (", ".join(scan["signals"]) if scan["signals"] else "No configured patterns detected.")])
            lines.append("Message excerpt: " + scan["message"][:300])
        lines.extend(["", "I request that this information be reviewed and that I be advised on appropriate next steps.", "", "Signature: " + who, "Date: " + datetime.now().strftime("%d %B %Y")])
        st.session_state.complaint_draft = "\n".join(lines)
    draft = st.session_state.get("complaint_draft", "")
    draft = st.text_area("Editable complaint draft", value=draft, height=350, key="complaint_editor")
    if draft.strip():
        st.download_button("Download draft as TXT", draft, "hershield_complaint_draft.txt", "text/plain", use_container_width=True)
    st.warning("This is not legal advice or an official complaint submission. Verify every detail, remove inaccuracies and use official channels to submit.")

# ---------------- PRIVACY & HELP ----------------
elif page == "Privacy & Help":
    page_header("TRANSPARENCY · LIMITATIONS · SUPPORT", "🛡️ Privacy & Help", "Know what the prototype does—and what it does not do.")
    a, b = st.columns(2)
    with a:
        card("🔒", "Session-based data", "Notes, scans and checklist choices live in Streamlit session state and may disappear when the session resets.", "PRIVACY")
        card("🧠", "Rule-based scanner", "Configured text patterns flag possible warning signals. This is not a trained AI model and may miss or misclassify messages.", "LIMITATION")
    with b:
        card("🚨", "SOS is simulated", "No call, SMS, live location or emergency alert is sent to anyone.", "DEMO ONLY")
        card("⏱️", "No background monitoring", "Countdowns and fake-call simulations do not guarantee alerts while the browser is idle or closed.", "LIMITATION")
    st.subheader("Emergency resources")
    st.write("For immediate danger, contact local emergency services or someone you trust. Confirm helpline numbers for your location through official sources.")
    if st.button("Run SOS simulation", type="primary", use_container_width=True):
        st.session_state.sos_demo_count += 1
        st.error("SIMULATION ONLY — no contact or emergency service has been notified.")
    st.caption(f"SOS demo activations in this session: {st.session_state.sos_demo_count}")

st.divider()
st.caption("HERShield AI · recHERs’26 · PS2 Women’s Safety · Prototype only; not an emergency service")
