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

/* Memperbaiki warna teks kolom input angka agar terbaca jelas & kontras di HP */
div[data-testid="stNumberInput"] input {
    color: #0D1117 !important;
    background-color: #FFFFFF !important;
    font-weight: bold;
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

/* Info box & Notice styling */
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

/* Design tombol hitung */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--blue));
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 12px 24px;
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
#  SESSION STATE — Menyimpan hasil hitung rumus
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
        "berdasarkan parameter kimia utama yaitu pH, BOD, dan COD."
    )

if "ph_direct_value" not in st.session_state:
    st.session_state.ph_direct_value = 7.0
if "bod_calc_result" not in st.session_state:
    st.session_state.bod_calc_result = 2.0
if "cod_calc_result" not in st.session_state:
    st.session_state.cod_calc_result = 15.0

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
#  HELPER FUNCTIONS
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
#  SIDEBAR (INPUT DETEKSI DATA JADI)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 8px 0;">
        <div style="font-family:'Space Mono',monospace; font-size:1.1rem; font-weight:700;
                    background:linear-gradient(90deg,#0EB8A4,#1A6EFC);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            💧 AquaChem IKA
        </div>
    </div>
    <hr style="border:none; border-top:1px solid #242C3D; margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**📥 Masukkan Nilai Akhir Parameter**")
    st.info("Ketik langsung data pH, BOD, dan COD yang sudah Anda miliki di sini. Aplikasi akan langsung mendeteksi kualitas air secara otomatis.")

    # Input angka utama di sidebar samping
    ph_val  = st.number_input("Nilai pH Air (In-Situ)", min_value=0.0, max_value=14.0, value=st.session_state.ph_direct_value, step=0.1, key="main_ph_input")
    bod_val = st.number_input("Nilai BOD (mg/L)", min_value=0.0, max_value=200.0, value=st.session_state.bod_calc_result, step=0.1, key="main_bod_input")
    cod_val = st.number_input("Nilai COD (mg/L)", min_value=0.0, max_value=500.0, value=st.session_state.cod_calc_result, step=0.1, key="main_cod_input")

    st.markdown("<hr style='border:none;border-top:1px solid #242C3D;margin:20px 0;'>", unsafe_allow_html=True)

    with st.expander("⚙️ Pengaturan Aplikasi"):
        new_app = st.text_input("Nama Aplikasi", value=st.session_state.app_name)
        new_grp = st.text_input("Nama Kelompok", value=st.session_state.group_name)
        new_gdesc = st.text_area("Deskripsi Kelompok", value=st.session_state.group_desc, height=80)
        new_wdesc = st.text_area("Deskripsi Website", value=st.session_state.web_desc, height=100)
        if st.button("💾 SIMPAN PENGATURAN"):
            st.session_state.app_name  = new_app
            st.session_state.group_name  = new_grp
            st.session_state.group_desc  = new_gdesc
            st.session_state.web_desc    = new_wdesc
            st.success("Pengaturan tersimpan!")

# Hitung Skor Kualitas Air IKA
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)

ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  MAIN — HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">INDEKS KUALITAS AIR</div>
  <h1 class="hero-title">{st.session_state.app_name}</h1>
  <p class="hero-sub">{st.session_state.web_desc}</p>
</div>
""", unsafe_allow_html=True)

# Tabs menu utama
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Analisis Parameter",
    "📖  Referensi Standar",
    "📈  Visualisasi",
    "ℹ️  Tentang",
])

# ══════════════════════════════════════════════
#  TAB 1 — ANALISIS PARAMETER & KALKULATOR UTAMA
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">Indeks Kualitas Air (IKA) & Status Real-time</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])

    with c1:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color}40;">
          <div class="ika-ring">
            <div class="ika-score" style="color:{ika_color};">{ika_score}</div>
            <div class="ika-label">Skor IKA (0–100)</div>
            <div class="ika-cat" style="color:{ika_color};">{ika_cat}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">pH</div>
          <div class="param-fullname">Derajat Keasaman (In-Situ)</div>
          <div class="param-value">{ph_val}</div>
          <div class="param-unit">skala</div>
          {status_chip(ph_label, ph_cls)}
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">BOD</div>
          <div class="param-fullname">Biochemical Oxygen Demand</div>
          <div class="param-value">{bod_val}</div>
          <div class="param-unit">mg/L</div>
          {status_chip(bod_label, bod_cls)}
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">COD</div>
          <div class="param-fullname">Chemical Oxygen Demand</div>
          <div class="param-value">{cod_val}</div>
          <div class="param-unit">mg/L</div>
          {status_chip(cod_label, cod_cls)}
        </div>""", unsafe_allow_html=True)

    # 🚀 KALKULATOR KHUSUS UNTUK DATA TITRASI LAB (BOD & COD)
    st.markdown('<div class="sec-head">🧪 Kalkulator Rumus Lab (Titrasi Kimia)</div>', unsafe_allow_html=True)
    
    with st.expander("👉 JIKA BELUM ADA DATA JADI BOD/COD, KLIK DISINI UNTUK MENGHITUNG DARI HASIL TITRASI LAB", expanded=False):
        st.markdown("<p style='color: #7A8BA6; font-size: 0.88rem;'>Gunakan panel di bawah ini untuk mengonversi volume miliLiter titrasi hasil praktikum laboratorium menjadi kadar mg/L jadi.</p>", unsafe_allow_html=True)
        
        calc_col1, calc_col2 = st.columns(2)
        
        # 🧪 1. Kalkulator Rumus BOD (Titrasi Winkler)
        with calc_col1:
            st.markdown("""<div style="font-weight: bold; color: #1A6EFC; font-family: 'Space Mono', monospace; margin-bottom: 8px;">🔬 Perhitungan BOD (Winkler)</div>""", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.75rem; color:#7A8BA6;'>Rumus: ((Vb - Vs) x N x 8000) / V_sampel</p>", unsafe_allow_html=True)
            bod_v_blanko   = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=10.0, step=0.01, key="main_bod_vb")
            bod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=8.5,  step=0.01, key="main_bod_vs")
            bod_n          = st.number_input("Normalitas Na₂S₂O₃ (N)", min_value=0.0, value=0.025, step=0.001, format="%.4f", key="main_bod_n")
            bod_v_sampel   = st.number_input("Volume Sampel Air (mL)", min_value=0.1, value=100.0, step=1.0, key="main_bod_ml")
            
            if st.button("🔢 HITUNG NILAI BOD"):
                if bod_v_sampel > 0:
                    hasil_bod = round((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000 / bod_v_sampel, 2)
                    st.session_state.bod_calc_result = hasil_bod
                    st.success(f"Dihitung: BOD = {hasil_bod} mg/L")
                    st.rerun()

        # 🧪 2. Kalkulator Rumus COD (Titrasi Dikromat)
        with calc_col2:
            st.markdown("""<div style="font-weight: bold; color: #8B5CF6; font-family: 'Space Mono', monospace; margin-bottom: 8px;">🔬 Perhitungan COD (Dikromat)</div>""", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.75rem; color:#7A8BA6;'>Rumus: ((Vb - Vs) x N x 8000) / V_sampel</p>", unsafe_allow_html=True)
            cod_v_blanko   = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=15.0, step=0.01, key="main_cod_vb")
            cod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=12.0, step=0.01, key="main_cod_vs")
            cod_n          = st.number_input("Normalitas FAS (N)", min_value=0.0, value=0.1,  step=0.001, format="%.4f", key="main_cod_n")
            cod_v_sampel   = st.number_input("Volume Sampel Air (mL)", min_value=0.1, value=20.0, step=1.0, key="main_cod_ml")
            
            if st.button("🔢 HITUNG NILAI COD"):
                if cod_v_sampel > 0:
                    hasil_cod = round((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000 / cod_v_sampel, 2)
                    st.session_state.cod_calc_result = hasil_cod
                    st.success(f"Dihitung: COD = {hasil_cod} mg/L")
                    st.rerun()

    # Detail Analisis Parameter Deskriptif
    st.markdown('<div class="sec-head">Detail Analisis Parameter</div>', unsafe_allow_html=True)
    with st.expander("🔵 pH — Derajat Keasaman Air", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a: st.markdown("**Apa itu pH?**\npH mengukur tingkat keasaman cairan secara langsung di lapangan (*in-situ*). Rentang optimal baku mutu PP 22/2021 adalah 6.5–8.0.")
        with col_b:
            if ph_cls == "good": st.markdown(f'<div class="info-box">✅ <strong>pH {ph_val}</strong> — Memenuhi standar baku mutu air permukaan kelas II.</div>', unsafe_allow_html=True)
            elif ph_cls == "warn": st.markdown(f'<div class="warn-box">⚠️ <strong>pH {ph_val}</strong> — Indikasi asam/basa ringan, memerlukan pantauan berkala.</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div class="bad-box">🚨 <strong>pH {ph_val}</strong> — Kondisi kritis/ekstrem! Air sangat tercemar.</div>', unsafe_allow_html=True)

    with st.expander("🟢 BOD — Biochemical Oxygen Demand", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a: st.markdown("**Apa itu BOD?**\nBOD mengukur oksigen untuk penguraian biologis bakteri. Standar baku mutu nasional Kelas II adalah ≤ 3 mg/L.")
        with col_b:
            if bod_cls == "good": st.markdown(f'<div class="info-box">✅ <strong>BOD {bod_val} mg/L</strong> — Aman, kandungan limbah organik rendah.</div>', unsafe_allow_html=True)
            elif bod_cls == "warn": st.markdown(f'<div class="warn-box">⚠️ <strong>BOD {bod_val} mg/L</strong> — Melewati batas baku mutu! Tercemar ringan-sedang.</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div class="bad-box">🚨 <strong>BOD {bod_val} mg/L</strong> — Pencemaran organik berat yang membahayakan biota akuatik.</div>', unsafe_allow_html=True)

    with st.expander("🔴 COD — Chemical Oxygen Demand", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a: st.markdown("**Apa itu COD?**\nCOD adalah kebutuhan oksigen penguraian senyawa kimia organik menggunakan oksidator. Standar baku mutu nasional Kelas II adalah ≤ 25 mg/L.")
        with col_b:
            if cod_cls == "good": st.markdown(f'<div class="info-box">✅ <strong>COD {cod_val} mg/L</strong> — Sesuai ambang batas aman baku mutu kimiawi.</div>', unsafe_allow_html=True)
            elif cod_cls == "warn": st.markdown(f'<div class="warn-box">⚠️ <strong>COD {cod_val} mg/L</strong> — Melewati batas aman! Terindikasi ada pencemaran zat kimia.</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div class="bad-box">🚨 <strong>COD {cod_val} mg/L</strong> — Konsentrasi senyawa kimia sangat tinggi dan berbahaya.</div>', unsafe_allow_html=True)

    # Analisis Rasio Lanjutan
    st.markdown('<div class="sec-head">Analisis Rasio Lanjutan</div>', unsafe_allow_html=True)
    if cod_val > 0:
        ratio = round(bod_val / cod_val, 3)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Rasio BOD/COD</div>
              <div class="param-fullname">Tingkat Biodegradabilitas</div>
              <div class="param-value">{ratio}</div>
              <div style="margin-top:10px; font-size:0.83rem; color:#7A8BA6; line-height:1.6;">
                {'✅ <b style="color:#22C55E">Mudah Terurai</b> — Limbah organik dapat dibersihkan secara alami menggunakan mikroba.' if ratio >= 0.5 else ('⚠️ <b style="color:#F59E0B">Cukup Terurai</b> — Perlu kombinasi sistem biologis-kimia.' if ratio >= 0.3 else '🔴 <b style="color:#EF4444">Sulit Terurai</b> — Didominasi bahan kimia rekalcitran / anorganik keras.')}
              </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Distribusi Bobot Sub-Indeks</div>
              <div class="param-fullname">Persentase Pengaruh Skor IKA</div>
              <div style="margin-top:14px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:#7A8BA6; font-size:0.83rem;">pH (Bobot 30%)</span><span style="font-family:'Space Mono',monospace; color:#0EB8A4;">{ph_si}</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px; margin-bottom:12px;"><div style="background:#0EB8A4; width:{ph_si}%; height:100%; border-radius:4px;"></div></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:#7A8BA6; font-size:0.83rem;">BOD (Bobot 35%)</span><span style="font-family:'Space Mono',monospace; color:#1A6EFC;">{bod_si}</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px; margin-bottom:12px;"><div style="background:#1A6EFC; width:{bod_si}%; height:100%; border-radius:4px;"></div></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:#7A8BA6; font-size:0.83rem;">COD (Bobot 35%)</span><span style="font-family:'Space Mono',monospace; color:#8B5CF6;">{cod_si}</span></div>
                <div style="background:#242C3D; border-radius:4px; height:6px;"><div style="background:#8B5CF6; width:{cod_si}%; height:100%; border-radius:4px;"></div></div>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — REFERENSI STANDAR
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">Baku Mutu Air Nasional (PP No. 22 Tahun 2021)</div>', unsafe_allow_html=True)
    st.markdown("#### 🔵 pH — Rentang Derajat Keasaman")
    render_ref_table(PH_REF)
    st.markdown("<br>#### 🟢 BOD — Biochemical Oxygen Demand (Baku Mutu Kelas II ≤ 3 mg/L)", unsafe_allow_html=True)
    render_ref_table(BOD_REF)
    st.markdown("<br>#### 🔴 COD — Chemical Oxygen Demand (Baku Mutu Kelas II ≤ 25 mg/L)", unsafe_allow_html=True)
    render_ref_table(COD_REF)

# ══════════════════════════════════════════════
#  TAB 3 — VISUALISASI GRAFIK PLOTLY
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">Visualisasi Grafik Distribusi</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=ika_score,
            title={"text": "Indeks Kualitas Air (IKA)", "font": {"color": "#E8EDF5", "size": 14}},
            number={"font": {"color": ika_color, "size": 48}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": ika_color, "thickness": 0.25}, "bgcolor": "#161B25"}
        ))
        fig_gauge.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117", height=300, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col2:
        fig_radar = go.Figure(go.Scatterpolar(r=[ph_si, bod_si, cod_si, ph_si], theta=["pH","BOD","COD","pH"], fill="toself", fillcolor="rgba(14,184,164,0.15)", line=dict(color="#0EB8A4", width=2)))
        fig_radar.update_layout(polar=dict(bgcolor="#161B25", radialaxis=dict(visible=True, range=[0, 100])), paper_bgcolor="#0D1117", plot_bgcolor="#0D1117", height=300, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_radar, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — TENTANG KELOMPOK
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">Detail Pembuat Aplikasi</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<div class="param-card"><div class="param-title">💧 {st.session_state.app_name}</div><div style="color:var(--muted); font-size:0.9rem; margin-top:10px;">{st.session_state.web_desc}</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="param-card"><div class="param-title">👥 {st.session_state.group_name}</div><div style="color:var(--muted); font-size:0.9rem; margin-top:10px; line-height:1.6;">{st.session_state.group_desc.replace("\n", "<br>")}</div></div>', unsafe_allow_html=True)
