import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# ====================== CONFIG ======================
st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

# ====================== DARK ELEGANT CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600&display=swap');
    
    .main {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    #MainMenu, header, footer {visibility: hidden;}
    
    h1 {
        font-family: 'Poppins', sans-serif;
        color: #67e8f9;
        font-weight: 600;
        letter-spacing: -1px;
        margin-bottom: 0;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2937;
        padding: 12px;
        border-radius: 16px;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1;
        border-radius: 12px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #14b8a6 !important;
        color: white !important;
    }
    
    .card {
        background-color: #1e2937;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
    }
    
    .teal-accent {
        color: #67e8f9;
        font-weight: 600;
    }
    
    .btn-teal {
        background-color: #14b8a6;
        color: white;
        border-radius: 12px;
    }
    
    .expander-header {
        background-color: #1e2937;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>✦ Kelas 9D</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Modern Classroom Management • Tahun Pelajaran 2025/2026</p>", unsafe_allow_html=True)

# ====================== DATA SISWA ======================
daftar_siswa = ["Pilih Nama Kamu...", "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", 
                "AZZAM", "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
                "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", "KEJORA", 
                "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", "NADHIF RAZA", "NINDITA", 
                "NINDYA", "RAFA BB", "RAIS", "RAKA", "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"]

DB_FILE = "kelas9d.db"

# ====================== DATABASE ======================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DROP TABLE IF EXISTS jadwal")
    conn.execute("DROP TABLE IF EXISTS pr")
    conn.execute('''CREATE TABLE jadwal 
                    (id INTEGER PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT, guru TEXT)''')
    conn.execute('''CREATE TABLE pr 
                    (id INTEGER PRIMARY KEY, hari TEXT, tanggal_input TEXT, mata_pelajaran TEXT, 
                     judul_pr TEXT, tanggal_pengumpulan TEXT, catatan TEXT, input_oleh TEXT)''')
    conn.commit()
    conn.close()

def seed_jadwal():
    conn = sqlite3.connect(DB_FILE)
    data = [ ... ]  # (sama seperti kode sebelumnya - saya singkat agar tidak terlalu panjang)
    # Isi data jadwal tetap sama seperti kode sebelumnya
    conn.executemany("INSERT INTO jadwal (hari, jam, mata_pelajaran, guru) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

# (Load, Save, Update, Delete functions tetap sama seperti kode sebelumnya)

# ====================== LOGIN ======================
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""
    st.session_state.edit_pr_id = None

if not st.session_state.sudah_login:
    st.markdown("### Silakan verifikasi identitasmu")
    nama = st.selectbox("", daftar_siswa, label_visibility="collapsed")
    if st.button("Masuk ke Kelas 9D", type="primary", use_container_width=True):
        if nama != "Pilih Nama Kamu...":
            st.session_state.sudah_login = True
            st.session_state.user_aktif = nama
            st.rerun()
    st.stop()

# ====================== HEADER ======================
st.success(f"Selamat datang kembali, **{st.session_state.user_aktif}**")
if st.button("Ganti Akun", use_container_width=False):
    st.session_state.sudah_login = False
    st.rerun()

st.divider()

tab1, tab2, tab3 = st.tabs(["📅 Jadwal Pelajaran", "📝 Input PR", "📜 Riwayat PR"])

# Tab contents akan saya lengkapi di balasan berikutnya karena terlalu panjang.
