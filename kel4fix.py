import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AquaChem IKA",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Root Variables */
:root {
    --teal:   #0EB8A4;
    --blue:   #1A6EFC;
    --indigo: #2D3A8C;
    --dark:   #0D1117;
    --card:   #161B25;
    --border: #242C3D;
    --text:   #E8EDF5;
    --muted:  #7A8BA6;
    --good:   #22C55E;
    --warn:   #F59E0B;
    --bad:    #EF4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

/* Hide default streamlit branding but keep sidebar toggle visible */
#MainMenu, footer {visibility: hidden;}

/* Sidebar Overrides */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #0D1117 0%, #0a2a40 50%, #0D1117 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(14,184,164,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -80px; left: 10%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(26,110,252,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #0EB8A4, #1A6EFC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(14,184,164,0.12);
    border: 1px solid rgba(14,184,164,0.4);
    color: var(--teal);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* Cards */
.param-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 22px;
    height: 100%;
    transition: border-color 0.2s;
}
.param-card:hover {
    border-color: var(--teal);
}
.param-title {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: var(--teal);
    margin-bottom: 6px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.param-fullname {
    color: var(--muted);
    font-size: 0.8rem;
    margin-bottom: 16px;
}
.param-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    margin-bottom: 4px;
}
.param-unit {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 14px;
}
.status-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.status-good   { background: rgba(34,197,94,0.15);  color: #22C55E; border: 1px solid rgba(34,197,94,0.35); }
.status-warn   { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.35); }
.status-bad    { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.35); }

/* Reference Table */
.ref-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}
.ref-table th {
    background: rgba(14,184,164,0.1);
    color: var(--teal);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}
.ref-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
.ref-table tr:last-child td { border-bottom: none; }
.ref-table tr:hover td { background: rgba(255,255,255,0.02); }

/* Section Header */
.sec-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: var(--teal);
    text-transform: uppercase;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-head::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* IKA Score Display */
.ika-ring {
    text-align: center;
    padding: 16px 0;
}
.ika-score {
    font-family: 'Space Mono', monospace;
    font-size: 3.8rem;
    font-weight: 700;
    line-height: 1;
}
.ika-label {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 6px;
}
.ika-cat {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 8px;
}

/* Info box classes */
.info-box {
    background: rgba(14,184,164,0.06);
    border: 1px solid rgba(14,184,164,0.25);
    border-left: 4px solid var(--teal);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
    margin: 10px 0;
    line-height: 1.6;
}
.warn-box {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.25);
    border-left: 4px solid #F59E0B;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
    margin: 10px 0;
    line-height: 1.6;
}
.bad-box {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.25);
    border-left: 4px solid #EF4444;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
    margin: 10px 0;
    line-height: 1.6;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 24px 0;
}

/* About Section Cards */
.about-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px 26px;
    margin-bottom: 18px;
}
.about-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: var(--teal);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.about-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 10px;
}
.about-body {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.7;
}

/* Metric Strip */
.metric-strip {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.metric-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 20px;
    flex: 1;
    min-width: 120px;
}
.metric-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--teal);
}
.metric-desc {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 2px;
}

/* Streamlit widget modifications */
.stSlider > label {
    color: var(--muted) !important;
    font-size: 0.85rem !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--blue));
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    padding: 10px 24px;
    transition: opacity 0.2s;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.85;
}
div[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
    color: var(--text) !important;
}

/* Tabs formatting */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(14,184,164,0.25), rgba(26,110,252,0.25)) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE FOR CUSTOMIZATION
# ─────────────────────────────────────────────
if "app_name" not in st.session_state:
    st.session_state.app_name = "AquaChem IKA"
if "group_name" not in st.session_state:
    st.session_state.group_name = "Anggota Kelompok 4"
if "group_desc" not in st.session_state:
    st.session_state.group_desc = (
        "Aqiila Rahmania Mumtaza (2560577)\n"
        "Gevan Eirano Yusuf (2560635)\n"
        "Magali Wahyudi (2560663)\n"
        "Naufa Afifah (2560715)\n"
        "Siti Halimah Tusysyadiyah Tsany (2560785)"
    )
if "web_desc" not in st.session_state:
    st.session_state.web_desc = (
        "Aplikasi ini dikembangkan untuk membantu analisis kualitas air "
        "berdasarkan parameter kimia utama yaitu pH, BOD, dan COD. "
        "Gunakan panel input di sebelah kiri untuk memasukkan nilai pengukuran lapangan."
    )

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.0", "Status": "💀 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan (Tercemar Sedang)", "Rentang": "5.0 – 6.0 atau 8.5 – 9.0", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Mendekati Normal", "Rentang": "6.0 – 6.5 atau 8.0 – 8.5", "Status": "🟡 Tercemar Ringan", "Kelas": "warn"},
    {"Kategori": "Normal / Baku Mutu", "Rentang": "6.5 – 8.0", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik (Air Bersih)", "Rentang": "< 2 mg/L", "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Air Bersih)", "Rentang": "2 – 3 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang", "Rentang": "3 – 6 mg/L", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "6 – 12 mg/L", "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 12 mg/L", "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik", "Rentang": "< 10 mg/L", "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Baku Mutu Kelas I/II)", "Rentang": "10 – 25 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan–Sedang", "Rentang": "25 – 50 mg/L", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "50 – 100 mg/L", "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 100 mg/L", "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]

# ─────────────────────────────────────────────
#  HELPER LOGIC FUNCTIONS
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.5 <= v <= 8.0: return "Memenuhi Baku Mutu", "good", 100
    elif (6.0 <= v < 6.5) or (8.0 < v <= 8.5): return "Tercemar Ringan", "warn", 60
    elif (5.0 <= v < 6.0) or (8.5 < v <= 9.0): return "Tercemar Sedang", "warn", 35
    else: return "Tercemar Berat", "bad", 10

def get_bod_status(v):
    if v < 2: return "Tidak Tercemar", "good", 100
    elif v <= 3: return "Memenuhi Baku Mutu", "good", 85
    elif v <= 6: return "Tercemar Sedang", "warn", 50
    elif v <= 12: return "Tercemar Berat", "bad", 25
    else: return "Sangat Tercemar Berat", "bad", 5

def get_cod_status(v):
    if v < 10: return "Tidak Tercemar", "good", 100
    elif v <= 25: return "Memenuhi Baku Mutu", "good", 80
    elif v <= 50: return "Tercemar Sedang", "warn", 45
    elif v <= 100: return "Tercemar Berat", "bad", 20
    else: return "Sangat Tercemar Berat", "bad", 5

def calc_ika(ph_val, bod_val, cod_val):
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80: return "Baik 🟢", "#22C55E"
    elif score >= 50: return "Tercemar Ringan–Sedang 🟡", "#F59E0B"
    elif score >= 25: return "Tercemar Berat 🔴", "#EF4444"
    else: return "Sangat Tercemar Berat ☠️", "#EF4444"

def status_chip(label, cls):
    return f'<span class="status-chip status-{cls}">{label}</span>'

def render_ref_table(data):
    rows = ""
    for r in data:
        cls  = r["Kelas"]
        chip = status_chip(r["Status"], cls)
        rows += f"<tr><td>{r['Kategori']}</td><td>{r['Rentang']}</td><td>{chip}</td></tr>"
    html = f"""
    <table class="ref-table">
      <thead><tr><th>Kategori</th><th>Rentang</th><th>Status</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""
    st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR INPUTS (FITUR SEPERTI PADA FOTO)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 8px 0;">
        <div style="font-family:'Space Mono',monospace; font-size:1.1rem; font-weight:700;
                    background:linear-gradient(90deg,#0EB8A4,#1A6EFC);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            💧 AquaChem IKA
        </div>
        <div style="color:#7A8BA6; font-size:0.78rem; margin-top:4px;">
            Sistem Informasi Kualitas Air
        </div>
    </div>
    <hr style="border:none; border-top:1px solid #242C3D; margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("**📥 Fitur Perhitungan & Parameter**")
    
    # Fitur Pemilihan Mode Persis seperti Foto / Kebutuhan Lab
    input_mode = st.radio("Mode Input Parameter:", ["📊 Langsung (Nilai)", "🧪 Dari Hasil Titrasi Lab"])
    
    st.markdown("---")
    
    # Input pH
    ph_val = st.slider("Nilai pH Air", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    
    # Inisialisasi default agar tidak eror
    bod_val = 0.0
    cod_val = 0.0
    
    if input_mode == "📊 Langsung (Nilai)":
        bod_val = st.slider("Nilai BOD (mg/L)", min_value=0.0, max_value=50.0, value=2.5, step=0.1)
        cod_val = st.slider("Nilai COD (mg/L)", min_value=0.0, max_value=150.0, value=18.0, step=0.1)
    
    else:
        # MODE TITRASI LAB (FITUR DI FOTO)
        st.markdown("<b style='color:#0EB8A4; font-size:0.85rem;'>🔬 Kalkulator Titrasi Winkler (BOD)</b>", unsafe_allow_html=True)
        bod_v_blanko = st.number_input("Vol. Titran Blanko (mL)", min_value=0.0, value=8.45, step=0.01, key="sb_vb")
        bod_v_sampel_t = st.number_input("Vol. Titran Sampel (mL)", min_value=0.0, value=5.20, step=0.01, key="sb_vst")
        bod_n = st.number_input("Normalitas Thiosulfat (N)", min_value=0.0000, value=0.0250, step=0.0001, format="%.4f", key="sb_n")
        bod_v_air = st.number_input("Volume Sampel Air (mL)", min_value=1.0, value=100.0, step=1.0, key="sb_va")
        
        # Rumus Hitung Otomatis BOD
        if bod_v_air > 0:
            bod_val = max(0.0, round(((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000) / bod_v_air, 2))
        
        st.markdown(f"**BOD Terhitung:** `{bod_val} mg/L`")
        st.markdown("---")
        
        st.markdown("<b style='color:#1A6EFC; font-size:0.85rem;'>🔬 Kalkulator Titrasi Refluks (COD)</b>", unsafe_allow_html=True)
        cod_v_blanko = st.number_input("Vol. Titran Blanko COD (mL)", min_value=0.0, value=15.10, step=0.01, key="sc_vb")
        cod_v_sampel_t = st.number_input("Vol. Titran Sampel COD (mL)", min_value=0.0, value=12.40, step=0.01, key="sc_vst")
        cod_n = st.number_input("Normalitas FAS (N)", min_value=0.0000, value=0.1000, step=0.0001, format="%.4f", key="sc_n")
        cod_v_air = st.number_input("Volume Sampel Air COD (mL)", min_value=1.0, value=20.0, step=1.0, key="sc_va")
        
        # Rumus Hitung Otomatis COD
        if cod_v_air > 0:
            cod_val = max(0.0, round(((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000) / cod_v_air, 2))
            
        st.markdown(f"**COD Terhitung:** `{cod_val} mg/L`")

    st.markdown("---")
    
    with st.expander("⚙️ Kustomisasi Aplikasi"):
        st.session_state.app_name = st.text_input("Nama Aplikasi", st.session_state.app_name)
        st.session_state.group_name = st.text_input("Nama Kelompok", st.session_state.group_name)
        st.session_state.group_desc = st.text_area("Daftar Anggota", st.session_state.group_desc, height=120)
        st.session_state.web_desc = st.text_area("Deskripsi", st.session_state.web_desc, height=80)

# ─────────────────────────────────────────────
#  CORE CALCULATIONS
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)

ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  MAIN DASHBOARD PAGE WIRE UP
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">DATA MONITORING REAL-TIME</div>
  <h1 class="hero-title">{st.session_state.app_name}</h1>
  <p class="hero-sub">{st.session_state.web_desc}</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analisis Kualitas Air",
    "📖 Standar Baku Mutu",
    "📈 Grafik & Visualisasi",
    "ℹ️ Profil Pengembang"
])

# ══════════════════════════════════════════════
#  TAB 1: DASHBOARD UTAMA
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">Indeks Kualitas Air (IKA)</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown(f"""
        <div class="param-card" style="border-color: {ika_color}60;">
          <div class="ika-ring">
            <div class="ika-score" style="color: {ika_color};">{ika_score}</div>
            <div class="ika-label">Skor Akhir Berbobot</div>
            <div class="ika-cat" style="color: {ika_color};">{ika_cat}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">pH</div>
          <div class="param-fullname">Derajat Keasaman</div>
          <div class="param-value">{ph_val}</div>
          <div class="param-unit">skala log</div>
          {status_chip(ph_label, ph_cls)}
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">BOD</div>
          <div class="param-fullname">Biochemical Oxygen Demand</div>
          <div class="param-value">{bod_val}</div>
          <div class="param-unit">mg/L O₂</div>
          {status_chip(bod_label, bod_cls)}
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">COD</div>
          <div class="param-fullname">Chemical Oxygen Demand</div>
          <div class="param-value">{cod_val}</div>
          <div class="param-unit">mg/L O₂</div>
          {status_chip(cod_label, cod_cls)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Tinjauan Detail Parameter Kerja</div>', unsafe_allow_html=True)
    
    with st.expander("🔵 Analisis Tingkat Keasaman (pH)", expanded=True):
        if ph_cls == "good":
            st.markdown(f'<div class="info-box">✅ Air berada pada kisaran pH ideal ({ph_val}). Kondisi ekosistem perairan stabil dan tidak korosif.</div>', unsafe_allow_html=True)
        elif ph_cls == "warn":
            st.markdown(f'<div class="warn-box">⚠️ pH air menunjukkan sedikit anomali ({ph_val}). Dapat memicu stress ringan pada biota air sensitif jika dibiarkan.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bad-box">🚨 Kritis! pH bernilai {ph_val}. Indikasi kuat adanya kontaminasi asam kuat atau senyawa alkalin tinggi berbahaya.</div>', unsafe_allow_html=True)

    with st.expander("🟢 Kebutuhan Oksigen Biologis (BOD)", expanded=True):
        if bod_cls == "good":
            st.markdown(f'<div class="info-box">✅ Kepadatan bahan organik rendah ({bod_val} mg/L). Oksigen terlarut melimpah dan aman bagi mikroorganisme air.</div>', unsafe_allow_html=True)
        elif bod_cls == "warn":
            st.markdown(f'<div class="warn-box">⚠️ Akumulasi limbah organik terdeteksi ({bod_val} mg/L). Mikroba mengonsumsi oksigen lebih cepat dari biasanya.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bad-box">🚨 Bahaya Pencemaran Organik ({bod_val} mg/L). Berisiko menciptakan kondisi anoksik (kehabisan oksigen) di badan air.</div>', unsafe_allow_html=True)

    with st.expander("🔴 Kebutuhan Oksigen Kimiawi (COD)", expanded=True):
        if cod_cls == "good":
            st.markdown(f'<div class="info-box">✅ Kadar oksidasi kimiawi aman ({cod_val} mg/L). Tidak ada indikasi polusi polutan kimia non-biodegradable yang berarti.</div>', unsafe_allow_html=True)
        elif cod_cls == "warn":
            st.markdown(f'<div class="warn-box">⚠️ Nilai COD meningkat ({cod_val} mg/L). Sinyal awal masuknya polutan industri atau limpahan air permukaan tercemar.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bad-box">🚨 Kontaminasi Bahan Kimia Akut ({cod_val} mg/L). Air tercemar berat oleh zat anorganik/organik kompleks yang sulit didegradasi alami.</div>', unsafe_allow_html=True)

    if cod_val > 0:
        b_c_ratio = round(bod_val / cod_val, 2)
        st.markdown('<div class="sec-head">Rasio Biodegradabilitas</div>', unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Rasio BOD / COD</div>
              <div class="param-value">{b_c_ratio}</div>
              <div class="param-fullname" style="margin-top:8px;">
                { '🟢 Nilai Rasio Tinggi (≥ 0.5): Limbah didominasi zat organik alami, mudah diolah secara biologis.' if b_c_ratio >= 0.5 else '🟡 Nilai Rasio Sedang (0.3 - 0.49): Sebagian limbah sulit terurai biologis.' if b_c_ratio >= 0.3 else '🔴 Nilai Rasio Rendah (< 0.3): Didominasi polutan toksik/kimia, membutuhkan pengolahan khusus.' }
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col_right:
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Kontribusi Sub-Indeks Bobot</div>
              <div style="margin-top:12px;">
                <div style="font-size:0.8rem; display:flex; justify-content:space-between;"><span>Sub-pH (30%)</span><span>{ph_si}/100</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px; margin-bottom:8px;"><div style="background:#0EB8A4; width:{ph_si}%; height:100%; border-radius:4px;"></div></div>
                <div style="font-size:0.8rem; display:flex; justify-content:space-between;"><span>Sub-BOD (35%)</span><span>{bod_si}/100</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px; margin-bottom:8px;"><div style="background:#1A6EFC; width:{bod_si}%; height:100%; border-radius:4px;"></div></div>
                <div style="font-size:0.8rem; display:flex; justify-content:space-between;"><span>Sub-COD (35%)</span><span>{cod_si}/100</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px;"><div style="background:#2D3A8C; width:{cod_si}%; height:100%; border-radius:4px;"></div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2: BAKU MUTU STANDARD
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">Standar Lampiran VI PP No. 22 Tahun 2021</div>', unsafe_allow_html=True)
    st.markdown("#### 🔵 Parameter Derajat Keasaman (pH)")
    render_ref_table(PH_REF)
    st.markdown("<br><h4>🟢 Parameter Biochemical Oxygen Demand (BOD)</h4>", unsafe_allow_html=True)
    render_ref_table(BOD_REF)
    st.markdown("<br><h4>🔴 Parameter Chemical Oxygen Demand (COD)</h4>", unsafe_allow_html=True)
    render_ref_table(COD_REF)

# ══════════════════════════════════════════════
#  TAB 3: VISUALISASI GRAFIK
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">Visualisasi Posisi Data Parameter</div>', unsafe_allow_html=True)
    cg1, cg2 = st.columns(2)
    with cg1:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number", value=ika_score,
            title={"text": "Indeks IKA", "font": {"color": "#E8EDF5", "size": 14}},
            number={"font": {"color": ika_color, "size": 42}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#7A8BA6"},
                "bar": {"color": ika_color, "thickness": 0.2},
                "bgcolor": "#161B25", "borderwidth": 0,
                "steps": [
                    {"range": [0, 25], "color": "rgba(239,68,68,0.12)"},
                    {"range": [25, 50], "color": "rgba(239,68,68,0.05)"},
                    {"range": [50, 80], "color": "rgba(245,158,11,0.08)"},
                    {"range": [80, 100], "color": "rgba(34,197,94,0.1)"}
                ]
            }
        ))
        fig_g.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117", height=240, margin=dict(l=20,r=20,t=40,b=10))
        st.plotly_chart(fig_g, use_container_width=True)
    with cg2:
        radar_cats = ["pH (Sub)", "BOD (Sub)", "COD (Sub)"]
        radar_vals = [ph_si, bod_si, cod_si]
        fig_r = go.Figure(go.Scatterpolar(r=radar_vals + [radar_vals[0]], theta=radar_cats + [radar_cats[0]], fill="toself", fillcolor="rgba(14,184,164,0.15)", line=dict(color="#0EB8A4", width=2)))
        fig_r.update_layout(polar=dict(bgcolor="#161B25", radialaxis=dict(visible=True, range=[0, 100], gridcolor="#242C3D")), paper_bgcolor="#0D1117", height=240, margin=dict(l=30,r=30,t=40,b=10))
        st.plotly_chart(fig_r, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4: TENTANG PENGEMBANG
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">Informasi Kelompok & Project</div>', unsafe_allow_html=True)
    cx1, cx2 = st.columns(2)
    with cx1:
        st.markdown(f"""
        <div class="about-card" style="border-color:rgba(14,184,164,0.3);">
          <div class="about-label">Modul Sistem</div>
          <div class="about-title">💧 {st.session_state.app_name}</div>
          <div class="about-body">{st.session_state.web_desc}</div>
        </div>
        """, unsafe_allow_html=True)
    with cx2:
        g_html = st.session_state.group_desc.replace("\n", "<br>")
        st.markdown(f"""
        <div class="about-card" style="border-color:rgba(26,110,252,0.3);">
          <div class="about-label">Tim Teknis</div>
          <div class="about-title">👥 {st.session_state.group_name}</div>
          <div class="about-body">{g_html}</div>
        </div>
        """, unsafe_allow_html=True)
