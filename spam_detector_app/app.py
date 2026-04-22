import streamlit as st
import joblib
import numpy as np
import time
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpamShield – AI Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0b0e1a;
    --surface:   #131728;
    --card:      #1a1f36;
    --border:    #252c48;
    --accent1:   #6c63ff;
    --accent2:   #ff4d6d;
    --accent3:   #00d4b4;
    --text:      #e8eaf6;
    --muted:     #7b82a8;
    --safe:      #00d4b4;
    --danger:    #ff4d6d;
    --radius:    16px;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding: 2rem 1.5rem 4rem;
    max-width: 780px;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(108,99,255,.2), rgba(0,212,180,.2));
    border: 1px solid rgba(108,99,255,.4);
    color: var(--accent3);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    padding: .35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 .5rem;
    background: linear-gradient(135deg, #fff 30%, var(--accent1) 70%, var(--accent3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Info Cards ── */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .9rem;
    margin: 1.8rem 0 2.2rem;
}
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1rem;
    text-align: center;
    transition: border-color .25s;
}
.info-card:hover { border-color: var(--accent1); }
.info-card .ic-icon { font-size: 1.6rem; margin-bottom: .4rem; }
.info-card .ic-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent1);
}
.info-card .ic-label {
    font-size: .75rem;
    color: var(--muted);
    margin-top: .15rem;
    text-transform: uppercase;
    letter-spacing: .08em;
}

/* ── Section Label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .6rem;
}

/* ── Textarea Override ── */
textarea {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .97rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color .25s !important;
    resize: vertical !important;
}
textarea:focus {
    border-color: var(--accent1) !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,.18) !important;
    outline: none !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent1), #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: .04em !important;
    padding: .85rem 2rem !important;
    cursor: pointer !important;
    transition: all .25s !important;
    margin-top: .5rem !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(108,99,255,.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Result Card ── */
.result-safe {
    background: linear-gradient(135deg, rgba(0,212,180,.08), rgba(0,212,180,.03));
    border: 1.5px solid rgba(0,212,180,.4);
    border-radius: var(--radius);
    padding: 1.8rem 1.6rem;
    text-align: center;
    animation: fadeUp .45s ease;
}
.result-danger {
    background: linear-gradient(135deg, rgba(255,77,109,.1), rgba(255,77,109,.03));
    border: 1.5px solid rgba(255,77,109,.45);
    border-radius: var(--radius);
    padding: 1.8rem 1.6rem;
    text-align: center;
    animation: fadeUp .45s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-icon { font-size: 3rem; margin-bottom: .6rem; }
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    margin: 0 0 .3rem;
}
.result-safe   .result-title { color: var(--safe); }
.result-danger .result-title { color: var(--danger); }
.result-desc { color: var(--muted); font-size: .92rem; line-height: 1.55; }

/* ── Confidence Bar ── */
.conf-wrap { margin-top: 1.1rem; }
.conf-label {
    display: flex;
    justify-content: space-between;
    font-size: .78rem;
    color: var(--muted);
    margin-bottom: .35rem;
}
.conf-bar-bg {
    background: var(--border);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.conf-bar-fill-safe {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--safe), #00f5d4);
    transition: width 1s cubic-bezier(.4,0,.2,1);
}
.conf-bar-fill-danger {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--danger), #ff8fa3);
    transition: width 1s cubic-bezier(.4,0,.2,1);
}

/* ── Sample Chips ── */
.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    margin: .4rem 0 1rem;
}
.chip {
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: .78rem;
    padding: .3rem .75rem;
    border-radius: 999px;
    cursor: pointer;
    transition: all .2s;
    white-space: nowrap;
}
.chip:hover {
    border-color: var(--accent1);
    color: var(--accent1);
    background: rgba(108,99,255,.08);
}

/* ── History Table ── */
.hist-row {
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: .7rem .9rem;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--border);
    margin-bottom: .5rem;
    font-size: .87rem;
}
.hist-badge-safe   { background: rgba(0,212,180,.15);  color: var(--safe);   padding: .2rem .55rem; border-radius: 999px; font-size: .72rem; font-weight: 600; white-space: nowrap; }
.hist-badge-danger { background: rgba(255,77,109,.15); color: var(--danger); padding: .2rem .55rem; border-radius: 999px; font-size: .72rem; font-weight: 600; white-space: nowrap; }
.hist-text { flex: 1; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Spinner tweak ── */
.stSpinner > div { border-top-color: var(--accent1) !important; }

/* ── Selectbox + misc ── */
.stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Load Model & Vectorizer ───────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model_path = "spam_classifier_model.joblib"
    vec_path   = "tfidf_vectorizer.joblib"
    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        return None, None
    return joblib.load(model_path), joblib.load(vec_path)

model, vectorizer = load_artifacts()


# ── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🛡️ AI-Powered Detection</div>
  <h1 class="hero-title">SpamShield</h1>
  <p class="hero-sub">Instantly detect spam messages using a Naïve Bayes classifier trained on real-world SMS data.</p>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="ic-icon">🎯</div>
    <div class="ic-val">98.2%</div>
    <div class="ic-label">Accuracy</div>
  </div>
  <div class="info-card">
    <div class="ic-icon">📊</div>
    <div class="ic-val">TF-IDF</div>
    <div class="ic-label">Vectorizer</div>
  </div>
  <div class="info-card">
    <div class="ic-icon">⚡</div>
    <div class="ic-val">&lt;50ms</div>
    <div class="ic-label">Inference</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Model-not-found warning ───────────────────────────────────────────────────
if model is None or vectorizer is None:
    st.warning(
        "⚠️  **Model files not found.**  "
        "Please place `spam_classifier_model.joblib` and `tfidf_vectorizer.joblib` "
        "in the same folder as `app.py` and restart the app."
    )
    st.stop()

# ── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sample Messages ───────────────────────────────────────────────────────────
SAMPLES = {
    "🎁 Free prize": "Congratulations! You've won a FREE iPhone. Click now to claim your prize!",
    "💰 Loan offer":  "Get instant loan approval up to ₹50,000. No documents needed. Apply today!",
    "📅 Meeting":     "Hey, are you coming to the meeting tomorrow at 10 AM?",
    "📚 Study":       "Can you send me the notes from today's lecture?",
    "🏆 Casino":      "WINNER!! As a valued customer you have been selected to receive a £900 prize reward!",
    "☕ Casual":       "I'll grab coffee on the way, want anything?",
}

st.markdown('<div class="section-label">Try a sample message</div>', unsafe_allow_html=True)

col_chips = st.columns(len(SAMPLES))
chosen_sample = None
for i, (label, msg) in enumerate(SAMPLES.items()):
    if col_chips[i].button(label, key=f"chip_{i}"):
        chosen_sample = msg

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Text Input ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Enter your message</div>', unsafe_allow_html=True)

default_text = chosen_sample if chosen_sample else st.session_state.get("last_input", "")
user_input = st.text_area(
    label="",
    value=default_text,
    placeholder="Type or paste a message here…",
    height=130,
    key="msg_input",
    label_visibility="collapsed",
)
st.session_state["last_input"] = user_input

analyze_btn = st.button("🔍  Analyze Message", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────────────────
if analyze_btn:
    if not user_input.strip():
        st.warning("Please enter a message before analyzing.")
    else:
        with st.spinner("Analyzing…"):
            time.sleep(0.4)
            vec   = vectorizer.transform([user_input])
            pred  = model.predict(vec)[0]
            proba = model.predict_proba(vec)[0]

        is_spam   = pred == 1
        confidence = float(proba[1] if is_spam else proba[0]) * 100
        bar_class  = "conf-bar-fill-danger" if is_spam else "conf-bar-fill-safe"

        if is_spam:
            st.markdown(f"""
            <div class="result-danger">
              <div class="result-icon">🚨</div>
              <div class="result-title">SPAM Detected</div>
              <div class="result-desc">This message shows strong indicators of spam — unsolicited promotions, phishing attempts, or scam content.</div>
              <div class="conf-wrap">
                <div class="conf-label"><span>Spam confidence</span><span>{confidence:.1f}%</span></div>
                <div class="conf-bar-bg">
                  <div class="{bar_class}" style="width:{confidence}%"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
              <div class="result-icon">✅</div>
              <div class="result-title">Safe Message</div>
              <div class="result-desc">This message appears to be legitimate. No spam signals were detected by the classifier.</div>
              <div class="conf-wrap">
                <div class="conf-label"><span>Safe confidence</span><span>{confidence:.1f}%</span></div>
                <div class="conf-bar-bg">
                  <div class="{bar_class}" style="width:{confidence}%"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Save to history
        st.session_state.history.insert(0, {
            "text":   user_input[:80] + ("…" if len(user_input) > 80 else ""),
            "result": "SPAM" if is_spam else "Safe",
            "conf":   f"{confidence:.0f}%",
        })
        st.session_state.history = st.session_state.history[:6]

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Recent checks</div>', unsafe_allow_html=True)
    for item in st.session_state.history:
        badge_cls = "hist-badge-danger" if item["result"] == "SPAM" else "hist-badge-safe"
        st.markdown(f"""
        <div class="hist-row">
          <span class="{badge_cls}">{item['result']}</span>
          <span class="hist-text">{item['text']}</span>
          <span style="color:var(--muted);font-size:.78rem;white-space:nowrap">{item['conf']}</span>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;color:var(--muted);font-size:.78rem;">
  Built with Streamlit · Naïve Bayes + TF-IDF · SMS Spam Collection Dataset
</div>
""", unsafe_allow_html=True)
