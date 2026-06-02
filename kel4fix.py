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

/* Hide default streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

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
.param-card:hover { border-color: var(--teal); }
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

/* IKA Score */
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

/* Info box */
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
.divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

/* About section */
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

/* Metric strip */
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

/* Streamlit overrides */
.stSlider > label { color: var(--muted) !important; font-size: 0.85rem !important; }
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
.stButton > button:hover { opacity: 0.85; }
div[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary { color: var(--text) !important; }

/* Tabs */
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
#  SESSION STATE — default settings
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
        "Gunakan slider di panel kiri untuk memasukkan nilai pengukuran lapangan."
    )

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.0",
     "Status": "💀 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan (Tercemar Sedang)", "Rentang": "5.0 – 6.0 atau 8.5 – 9.0",
     "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Mendekati Normal", "Rentang": "6.0 – 6.5 atau 8.0 – 8.5",
     "Status": "🟡 Tercemar Ringan", "Kelas": "warn"},
    {"Kategori": "Normal / Baku Mutu", "Rentang": "6.5 – 8.0",
     "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik (Air Bersih)", "Rentang": "< 2 mg/L",
     "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Air Bersih)", "Rentang": "2 – 3 mg/L",
     "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang", "Rentang": "3 – 6 mg/L",
     "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "6 – 12 mg/L",
     "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 12 mg/L",
     "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik", "Rentang": "< 10 mg/L",
     "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Baku Mutu Kelas I/II)", "Rentang": "10 – 25 mg/L",
     "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan–Sedang", "Rentang": "25 – 50 mg/L",
     "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "50 – 100 mg/L",
     "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 100 mg/L",
     "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.5 <= v <= 8.0:
        return "Memenuhi Baku Mutu", "good", 100
    elif (6.0 <= v < 6.5) or (8.0 < v <= 8.5):
        return "Tercemar Ringan", "warn", 60
    elif (5.0 <= v < 6.0) or (8.5 < v <= 9.0):
        return "Tercemar Sedang", "warn", 35
    else:
        return "Tercemar Berat", "bad", 10

def get_bod_status(v):
    if v < 2:
        return "Tidak Tercemar", "good", 100
    elif v <= 3:
        return "Memenuhi Baku Mutu", "good", 85
    elif v <= 6:
        return "Tercemar Sedang", "warn", 50
    elif v <= 12:
        return "Tercemar Berat", "bad", 25
    else:
        return "Sangat Tercemar Berat", "bad", 5

def get_cod_status(v):
    if v < 10:
        return "Tidak Tercemar", "good", 100
    elif v <= 25:
        return "Memenuhi Baku Mutu", "good", 80
    elif v <= 50:
        return "Tercemar Sedang", "warn", 45
    elif v <= 100:
        return "Tercemar Berat", "bad", 20
    else:
        return "Sangat Tercemar Berat", "bad", 5

def calc_ika(ph_val, bod_val, cod_val):
    """
    Indeks Kualitas Air sederhana berdasarkan sub-indeks tiap parameter.
    Bobot: pH=30%, BOD=35%, COD=35%
    """
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80:
        return "Baik 🟢", "#22C55E"
    elif score >= 50:
        return "Tercemar Ringan–Sedang 🟡", "#F59E0B"
    elif score >= 25:
        return "Tercemar Berat 🔴", "#EF4444"
    else:
        return "Sangat Tercemar Berat ☠️", "#EF4444"

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
#  SIDEBAR
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
            Indeks Kualitas Air — Parameter Kimia
        </div>
    </div>
    <hr style="border:none; border-top:1px solid #242C3D; margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**📥 Masukkan Nilai Parameter**")

    input_mode = st.radio("Mode Input", ["📊 Langsung (Nilai)", "🧪 Dari Titrasi"], horizontal=True)

    # ── pH (always direct input) ──
    ph_val = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                             help="Skala 0–14. Baku mutu: 6.5–8.0")

    if input_mode == "📊 Langsung (Nilai)":
        bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1,
                                  help="Biochemical Oxygen Demand. Baku mutu: < 3 mg/L")
        cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1,
                                  help="Chemical Oxygen Demand. Baku mutu: < 25 mg/L")
    else:
        # ── BOD dari Titrasi Winkler ──
        st.markdown("""<div style="font-size:0.8rem; color:#0EB8A4; font-family:'Space Mono',monospace;
                       margin:10px 0 6px 0;">🔬 BOD — Titrasi Winkler</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:#7A8BA6; margin-bottom:8px;">
            Rumus: BOD = (V_titran_blanko − V_titran_sampel) × N_Na₂S₂O₃ × 8000 / V_sampel
            </div>""", unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bod_v_blanko   = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=10.0, step=0.01, key="bod_vb")
            bod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=8.5,  step=0.01, key="bod_vs")
        with col_b2:
            bod_n          = st.number_input("N Na₂S₂O₃", min_value=0.0, value=0.025, step=0.001, format="%.4f", key="bod_n")
            bod_v_sampel   = st.number_input("V Sampel (mL)",         min_value=0.1,  value=100.0, step=1.0,  key="bod_ml")

        if bod_v_sampel > 0:
            bod_val = round((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000 / bod_v_sampel, 3)
        else:
            bod_val = 0.0
        st.markdown(f"""<div style="background:rgba(14,184,164,0.08); border:1px solid rgba(14,184,164,0.3);
                        border-radius:8px; padding:8px 14px; font-size:0.83rem; margin:6px 0 14px 0;">
                        BOD terhitung: <b style="color:#0EB8A4; font-family:'Space Mono',monospace;">
                        {bod_val} mg/L</b></div>""", unsafe_allow_html=True)

        # ── COD dari Titrasi Permanganometri / Dikromat ──
        st.markdown("""<div style="font-size:0.8rem; color:#8B5CF6; font-family:'Space Mono',monospace;
                       margin:6px 0 6px 0;">🔬 COD — Titrasi Dikromat / Permanganometri</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:#7A8BA6; margin-bottom:8px;">
            Rumus: COD = (V_blanko − V_sampel) × N_titran × 8000 / V_sampel
            </div>""", unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cod_v_blanko   = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=15.0, step=0.01, key="cod_vb")
            cod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=12.0, step=0.01, key="cod_vs")
        with col_c2:
            cod_n          = st.number_input("N Titran (FAS/KMnO₄)", min_value=0.0, value=0.1,  step=0.001, format="%.4f", key="cod_n")
            cod_v_sampel   = st.number_input("V Sampel (mL)",          min_value=0.1, value=20.0, step=1.0,  key="cod_ml")

        if cod_v_sampel > 0:
            cod_val = round((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000 / cod_v_sampel, 3)
        else:
            cod_val = 0.0
        st.markdown(f"""<div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.3);
                        border-radius:8px; padding:8px 14px; font-size:0.83rem; margin:6px 0 4px 0;">
                        COD terhitung: <b style="color:#8B5CF6; font-family:'Space Mono',monospace;">
                        {cod_val} mg/L</b></div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #242C3D;margin:20px 0;'>",
                unsafe_allow_html=True)

    with st.expander("⚙️  Pengaturan Aplikasi"):
        new_app = st.text_input("Nama Aplikasi", value=st.session_state.app_name)
        new_grp = st.text_input("Nama Kelompok", value=st.session_state.group_name)
        new_gdesc = st.text_area("Deskripsi Kelompok", value=st.session_state.group_desc, height=80)
        new_wdesc = st.text_area("Deskripsi Website", value=st.session_state.web_desc, height=100)
        if st.button("💾  SIMPAN PENGATURAN"):
            st.session_state.app_name  = new_app
            st.session_state.group_name  = new_grp
            st.session_state.group_desc  = new_gdesc
            st.session_state.web_desc    = new_wdesc
            st.success("Pengaturan tersimpan!")

    st.markdown("""
    <div style="margin-top:24px; padding:12px; background:#0D1117;
                border-radius:8px; border:1px solid #242C3D; font-size:0.75rem; color:#7A8BA6;">
        📋 Referensi: PP No. 22/2021 & PermenLHK<br>
        Baku mutu air kelas II
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CALCULATE
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)

ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ =
