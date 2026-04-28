# streamlit_app.py — Polished AI Problem Decomposer + Self-Improving Agent

import time
import json
import streamlit as st
from dotenv import load_dotenv
from agent import ProblemDecomposerAgent

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Problem Decomposer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root{
    --bg1:#05060c;
    --bg2:#0f1020;
    --card:rgba(255,255,255,0.045);
    --card2:rgba(255,255,255,0.065);
    --border:rgba(255,255,255,0.09);
    --text:#f8fafc;
    --muted:#94a3b8;
    --primary:#8b5cf6;
    --secondary:#6366f1;
    --blue:#60a5fa;
    --green:#34d399;
    --amber:#fbbf24;
    --danger:#fb7185;
}

/* Main App */
.stApp{
    font-family:'Inter',sans-serif;
    color:var(--text);
    background:
    radial-gradient(circle at top left,#1f1147 0%,transparent 35%),
    radial-gradient(circle at bottom right,#0d3b66 0%,transparent 30%),
    linear-gradient(135deg,#04050a,#090a15,#05060c);
    background-attachment:fixed;
}

/* Floating particles effect */
.stApp:before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
    radial-gradient(rgba(255,255,255,.06) 1px, transparent 1px);
    background-size:32px 32px;
    opacity:.18;
    pointer-events:none;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:rgba(7,8,18,.82)!important;
    backdrop-filter:blur(18px);
    border-right:1px solid var(--border)!important;
}

[data-testid="stSidebar"] *{
    color:var(--text)!important;
}

/* Hide streamlit */
#MainMenu, footer, header{
    visibility:hidden;
}

/* Hero */
.hero{
    text-align:center;
    padding:3.5rem 1rem 1.5rem;
    animation:fadeUp .7s ease;
}

.hero-badge{
    display:inline-block;
    padding:8px 16px;
    border-radius:999px;
    font-size:11px;
    letter-spacing:.16em;
    font-family:'JetBrains Mono';
    color:#ddd6fe;
    border:1px solid rgba(139,92,246,.35);
    background:rgba(139,92,246,.12);
    box-shadow:0 0 20px rgba(139,92,246,.18);
    margin-bottom:1rem;
}

.hero-title{
    font-size:clamp(2.3rem,5vw,4rem);
    font-weight:800;
    line-height:1.05;
    background:linear-gradient(135deg,#ffffff,#c4b5fd,#60a5fa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:.7rem;
}

.hero-sub{
    color:var(--muted);
    font-size:1rem;
    letter-spacing:.03em;
}

/* Pipeline */
.pipeline{
    display:flex;
    justify-content:center;
    flex-wrap:wrap;
    gap:12px;
    margin:2rem 0;
}

.pipe-step{
    padding:10px 18px;
    border-radius:14px;
    font-size:12px;
    font-family:'JetBrains Mono';
    background:var(--card);
    border:1px solid var(--border);
    color:var(--muted);
    transition:.25s ease;
}

.pipe-step:hover{
    transform:translateY(-2px);
}

.pipe-step.active{
    color:#fff;
    border-color:rgba(139,92,246,.5);
    background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(99,102,241,.14));
    box-shadow:0 0 20px rgba(139,92,246,.25);
}

.pipe-step.done{
    color:#86efac;
    border-color:rgba(52,211,153,.35);
}

.pipe-arrow{
    color:#334155;
    font-size:20px;
    padding-top:4px;
}

/* Cards */
.stage-card,
.stat-chip,
.mem-bar{
    background:var(--card);
    border:1px solid var(--border);
    backdrop-filter:blur(16px);
    border-radius:22px;
    box-shadow:
    0 10px 30px rgba(0,0,0,.35),
    inset 0 1px 0 rgba(255,255,255,.03);
}

.stage-card{
    margin-bottom:1.2rem;
    overflow:hidden;
    animation:fadeUp .5s ease;
}

.stage-card:hover{
    transform:translateY(-2px);
    transition:.25s ease;
    border-color:rgba(255,255,255,.13);
}

/* Card Header */
.card-header{
    display:flex;
    align-items:center;
    gap:14px;
    padding:1rem 1.2rem;
    border-bottom:1px solid rgba(255,255,255,.05);
}

.card-icon{
    width:44px;
    height:44px;
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
}

.icon-blue{background:rgba(96,165,250,.15);}
.icon-amber{background:rgba(251,191,36,.15);}
.icon-green{background:rgba(52,211,153,.15);}

.card-title{
    font-size:1rem;
    font-weight:700;
}

.card-sub{
    font-size:11px;
    color:var(--muted);
    font-family:'JetBrains Mono';
}

/* Rows */
.step-row,.crit-row,.impr-row{
    margin:10px 12px;
    padding:14px 16px;
    border-radius:16px;
    background:rgba(255,255,255,.03);
    transition:.22s ease;
}

.step-row:hover,.crit-row:hover,.impr-row:hover{
    background:rgba(255,255,255,.06);
    transform:translateX(4px);
}

.step-row{border-left:3px solid var(--blue);}
.crit-row{border-left:3px solid var(--amber);}
.impr-row{border-left:3px solid var(--green);}

.step-text,.crit-text,.impr-text{
    color:#e2e8f0;
    font-size:13px;
    line-height:1.6;
}

/* Stats */
.stats-row{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:14px;
    margin-bottom:1.4rem;
}

.stat-chip{
    text-align:center;
    padding:20px;
}

.stat-chip:hover{
    transform:translateY(-3px);
    transition:.25s ease;
}

.stat-num{
    font-size:1.9rem;
    font-weight:800;
    background:linear-gradient(135deg,#fff,#c4b5fd);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.stat-lbl{
    font-size:10px;
    color:var(--muted);
    letter-spacing:.14em;
    text-transform:uppercase;
}

/* Text Area */
.stTextArea textarea{
    background:rgba(255,255,255,.04)!important;
    border:1px solid var(--border)!important;
    border-radius:18px!important;
    color:#fff!important;
    padding:16px!important;
    font-size:.95rem!important;
}

.stTextArea textarea:focus{
    border-color:var(--primary)!important;
    box-shadow:0 0 0 3px rgba(139,92,246,.15)!important;
}

/* Buttons */
div.stButton > button{
    border:none!important;
    border-radius:14px!important;
    color:white!important;
    font-weight:700!important;
    padding:.7rem 1rem!important;
    background:linear-gradient(135deg,#8b5cf6,#6366f1)!important;
    box-shadow:0 12px 24px rgba(99,102,241,.28)!important;
    transition:.22s ease!important;
}

div.stButton > button:hover{
    transform:translateY(-2px)!important;
    box-shadow:0 18px 30px rgba(99,102,241,.35)!important;
}

/* Download buttons */
div.stDownloadButton > button{
    border:none!important;
    border-radius:14px!important;
    font-weight:700!important;
    background:linear-gradient(135deg,#0ea5e9,#6366f1)!important;
    color:white!important;
}

/* Memory */
.mem-bar{
    padding:1rem 1.2rem;
    margin-top:1rem;
}

.mem-chip{
    display:inline-block;
    margin:5px;
    padding:6px 12px;
    border-radius:999px;
    font-size:11px;
    color:#67e8f9;
    border:1px solid rgba(103,232,249,.25);
    background:rgba(103,232,249,.08);
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}
::-webkit-scrollbar-thumb{
    background:#312e81;
    border-radius:10px;
}

/* Animation */
@keyframes fadeUp{
    from{
        opacity:0;
        transform:translateY(18px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

/* Mobile */
@media(max-width:900px){
    .stats-row{
        grid-template-columns:repeat(2,1fr);
    }
}

@media(max-width:640px){
    .stats-row{
        grid-template-columns:1fr;
    }

    .hero-title{
        font-size:2rem;
    }

    .pipeline{
        gap:8px;
    }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────
for k, v in {
    "result": None, "running": False, "phase": "idle",
    "error": None, "_steps": [], "_critiques": [],
    "history": [], "run_count": 0, "selected_problem": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 Agent Control")
    st.markdown("---")

    st.markdown("**Model**")
    model_choice = st.selectbox(
        "model",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"],
        label_visibility="collapsed",
    )

    st.markdown("**Creativity**")
    temperature = st.slider("temp", 0.0, 1.0, 0.7, 0.05, label_visibility="collapsed",
                            help="Higher = more creative; lower = more precise")

    st.markdown("---")
    st.markdown("**Session Stats**")
    ca, cb = st.columns(2)
    ca.metric("Runs", st.session_state.run_count)
    cb.metric("Saved", len(st.session_state.history))

    st.markdown("---")
    st.markdown("**📜 History**")
    if not st.session_state.history:
        st.markdown('<span style="color:#44445a;font-size:12px;font-family:monospace;">no runs yet.</span>',
                    unsafe_allow_html=True)
    else:
        for i, h in enumerate(reversed(st.session_state.history[-8:])):
            short = h["problem"][:36] + ("…" if len(h["problem"]) > 36 else "")
            if st.button(f"📄 {short}", key=f"hist_{i}", use_container_width=True):
                st.session_state.result = h
                st.session_state.phase = "done"
                st.rerun()
        st.markdown("")
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<span style="color:#44445a;font-size:11px;font-family:monospace;">'
        'distinction-level ai agent<br>powered by groq llm api</span>',
        unsafe_allow_html=True,
    )

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ Distinction-Level AI Agent</div>
  <div class="hero-title">AI Problem Decomposer<br>+ Self-Improving Agent</div>
  <div class="hero-sub">Reasoning &nbsp;·&nbsp; Planning &nbsp;·&nbsp; Reflection &nbsp;·&nbsp; Improvement</div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline bar ───────────────────────────────────────────────────────────
phase = st.session_state.phase
ORDER = ["decomposing", "critiquing", "improving", "done"]

def pipe_cls(key):
    if phase == key: return "pipe-step active"
    if phase in ORDER and key in ORDER and ORDER.index(key) < ORDER.index(phase): return "pipe-step done"
    if phase == "done" and key in ORDER: return "pipe-step done"
    return "pipe-step"

st.markdown(f"""
<div class="pipeline">
  <span class="pipe-step {'done' if phase != 'idle' else ''}">💬 Input</span>
  <span class="pipe-arrow">›</span>
  <span class="{pipe_cls('decomposing')}">🧩 Decompose</span>
  <span class="pipe-arrow">›</span>
  <span class="{pipe_cls('critiquing')}">🔍 Critique</span>
  <span class="pipe-arrow">›</span>
  <span class="{pipe_cls('improving')}">✨ Improve</span>
</div>
""", unsafe_allow_html=True)

# ── Quick prompts ──────────────────────────────────────────────────────────
QUICK = [
    "🌐 Build a website from scratch",
    "📱 Launch a mobile app in 60 days",
    "🚀 Start a startup in 90 days",
    "🛒 Create an e-commerce store",
    "🤖 Build an AI chatbot",
    "📊 Create a data dashboard",
]
st.markdown('<p style="font-size:11px;color:#44445a;font-family:\'JetBrains Mono\',monospace;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">// quick prompts</p>', unsafe_allow_html=True)
qcols = st.columns(3)
for idx, q in enumerate(QUICK):
    label = q.split(" ", 1)[1]
    if qcols[idx % 3].button(q, key=f"q{idx}", use_container_width=True):
        st.session_state.selected_problem = label
        st.rerun()

st.markdown("---")

# ── Problem input ──────────────────────────────────────────────────────────
problem = st.text_area(
    "Problem",
    value=st.session_state.selected_problem,
    placeholder='Describe any problem or goal — e.g. "Build a mobile app for food delivery"',
    height=110,
    label_visibility="collapsed",
)

col_run, col_reset = st.columns([5, 1])
with col_run:
    run_label = "⏳  Running..." if st.session_state.running else "▶  Run Agent"
    run_clicked = st.button(run_label, disabled=st.session_state.running or not problem.strip(),
                            use_container_width=True)
with col_reset:
    if st.button("↺", use_container_width=True, help="Reset everything"):
        for k in ("result", "error", "selected_problem"):
            st.session_state[k] = None if k != "selected_problem" else ""
        st.session_state.phase = "idle"
        st.session_state.running = False
        st.rerun()

# ── Trigger ────────────────────────────────────────────────────────────────
if run_clicked and problem.strip():
    st.session_state.update({"running": True, "result": None, "error": None,
                              "_steps": [], "_critiques": [], "phase": "decomposing"})
    st.rerun()

# ── Pipeline execution ─────────────────────────────────────────────────────
if st.session_state.running and phase not in ("idle", "done", "error"):
    try:
        agent = ProblemDecomposerAgent()

        if phase == "decomposing":
            with st.spinner("🧩 Stage 1 — Decomposing the problem into steps..."):
                steps = agent.decompose(problem)
            st.session_state._steps = steps
            st.session_state.phase = "critiquing"
            st.rerun()

        elif phase == "critiquing":
            with st.spinner("🔍 Stage 2 — Agent critiquing its own plan..."):
                agent.memory.set_problem(problem)
                agent.memory.set_steps(st.session_state._steps)
                critiques = agent.critique()
            st.session_state._critiques = critiques
            st.session_state.phase = "improving"
            st.rerun()

        elif phase == "improving":
            with st.spinner("✨ Stage 3 — Generating improved plan..."):
                agent.memory.set_problem(problem)
                agent.memory.set_steps(st.session_state._steps)
                agent.memory.set_critiques(st.session_state._critiques)
                improved = agent.improve()

            result = {
                "problem":   problem,
                "steps":     st.session_state._steps,
                "critiques": st.session_state._critiques,
                "improved":  improved,
                "model":     model_choice,
            }
            st.session_state.result = result
            st.session_state.history.append(result)
            st.session_state.run_count += 1
            st.session_state.phase = "done"
            st.session_state.running = False
            st.rerun()

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.running = False
        st.session_state.phase = "error"
        st.rerun()

# ── Error ──────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"**Agent Error:** {st.session_state.error}")
    if "GROQ_API_KEY" in (st.session_state.error or ""):
        st.info("💡 Add `GROQ_API_KEY=your_key_here` to your `.env` file and restart.")

# ── Results ────────────────────────────────────────────────────────────────
if st.session_state.result and st.session_state.phase == "done":
    r = st.session_state.result
    st.markdown("---")

    growth = round((len(r['improved']) - len(r['steps'])) / max(len(r['steps']), 1) * 100)
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-chip">
        <div class="stat-num">{len(r['steps'])}</div>
        <div class="stat-lbl">Initial Steps</div>
      </div>
      <div class="stat-chip">
        <div class="stat-num">{len(r['critiques'])}</div>
        <div class="stat-lbl">Critiques Found</div>
      </div>
      <div class="stat-chip">
        <div class="stat-num">{len(r['improved'])}</div>
        <div class="stat-lbl">Improved Steps</div>
      </div>
      <div class="stat-chip">
        <div class="stat-num">{growth:+d}%</div>
        <div class="stat-lbl">Plan Growth</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stage 1 + 2
    c1, c2 = st.columns(2)
    with c1:
        rows = "".join(
            f'<div class="step-row"><span class="step-num">{str(i+1).zfill(2)}</span><span class="step-text">{s}</span></div>'
            for i, s in enumerate(r["steps"])
        )
        st.markdown(f"""
        <div class="stage-card blue-card">
          <div class="card-header">
            <div class="card-icon icon-blue">🧩</div>
            <div class="card-meta">
              <div class="card-title">Step Decomposition</div>
              <div class="card-sub">agent.plan() → initial breakdown</div>
            </div>
            <span class="status-pill pill-done">✓ done</span>
          </div>
          <div class="card-body">{rows}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        rows = "".join(
            f'<div class="crit-row"><span class="crit-icon">⚠</span><span class="crit-text">{c}</span></div>'
            for c in r["critiques"]
        )
        st.markdown(f"""
        <div class="stage-card amber-card">
          <div class="card-header">
            <div class="card-icon icon-amber">🔍</div>
            <div class="card-meta">
              <div class="card-title">Self-Critique</div>
              <div class="card-sub">agent.reflect() → gaps &amp; weaknesses</div>
            </div>
            <span class="status-pill pill-done">✓ done</span>
          </div>
          <div class="card-body">{rows}</div>
        </div>""", unsafe_allow_html=True)

    # Stage 3
    rows = "".join(
        f'<div class="impr-row"><span class="impr-num">{str(i+1).zfill(2)}</span><span class="impr-text">{s}</span></div>'
        for i, s in enumerate(r["improved"])
    )
    st.markdown(f"""
    <div class="stage-card green-card">
      <div class="card-header">
        <div class="card-icon icon-green">✨</div>
        <div class="card-meta">
          <div class="card-title">Improved Plan</div>
          <div class="card-sub">agent.improve() → goal-based refined output addressing all critiques</div>
        </div>
        <span class="status-pill pill-done">✓ done</span>
      </div>
      <div class="card-body">{rows}</div>
    </div>""", unsafe_allow_html=True)

    # Memory bar
    mem_items = [
        ("problem", r["problem"][:28] + ("…" if len(r["problem"]) > 28 else "")),
        ("steps_count", len(r["steps"])),
        ("critiques_count", len(r["critiques"])),
        ("improved_count", len(r["improved"])),
        ("model", r.get("model", "llama-3.3-70b")),
        ("phase", "complete ✓"),
    ]
    mem_html = "".join(
        f'<span class="mem-chip"><span class="mem-key">{k}:</span>{v}</span>'
        for k, v in mem_items
    )
    st.markdown(f"""
    <div class="mem-bar">
      <div class="mem-label">🧠 agent.memory — session state</div>
      <div class="mem-grid">{mem_html}</div>
    </div>""", unsafe_allow_html=True)

    # Download + actions
    st.markdown("<br>", unsafe_allow_html=True)
    txt = (
        f"AI AGENT REPORT\n{'='*40}\n"
        f"Problem : {r['problem']}\nModel   : {r.get('model','N/A')}\n\n"
        f"STAGE 1 — DECOMPOSITION ({len(r['steps'])} steps)\n"
        + "\n".join(f"{i+1:02d}. {s}" for i,s in enumerate(r['steps']))
        + f"\n\nSTAGE 2 — SELF-CRITIQUE ({len(r['critiques'])} issues)\n"
        + "\n".join(f"  - {c}" for c in r['critiques'])
        + f"\n\nSTAGE 3 — IMPROVED PLAN ({len(r['improved'])} steps)\n"
        + "\n".join(f"{i+1:02d}. {s}" for i,s in enumerate(r['improved']))
    )

    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.download_button("⬇ Download .txt",  data=txt,
                           file_name="agent_report.txt",  mime="text/plain",  use_container_width=True)
    with dc2:
        st.download_button("⬇ Download .json", data=json.dumps(r, indent=2),
                           file_name="agent_report.json", mime="application/json", use_container_width=True)
    with dc3:
        if st.button("▶ Run Again", use_container_width=True):
            st.session_state.result = None
            st.session_state.phase = "idle"
            st.rerun()

    with st.expander("🔬 Raw agent output (JSON)"):
        st.json(r)

elif phase == "idle" and not st.session_state.result:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#22223a;">
      <div style="font-size:3rem;margin-bottom:1rem;">🤖</div>
      <div style="font-size:0.85rem;font-family:'JetBrains Mono',monospace;">
        pick a quick prompt or enter your problem above<br>
        then click <span style="color:#7c6fcd;">Run Agent</span>
      </div>
    </div>""", unsafe_allow_html=True)