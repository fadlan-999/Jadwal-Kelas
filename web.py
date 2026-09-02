import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ====================== CONFIG ======================
st.set_page_config(page_title="Kelas 4EU", layout="wide")
st.title("📚 Kelas 4EU - Info Jadwal & PR")

# CSS untuk menyembunyikan menu Streamlit
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

# ====================== DAFTAR SISWA ======================
daftar_siswa = [
    "Pilih Nama Kamu...", "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", 
    "ANISA", "AZZAM", "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", 
    "FADLAN", "FAIZ", "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", 
    "JIBRIL", "KEANDRA", "KEJORA", "KEYLA", "MASUD", "NABILA", 
    "NADHIF MUZAKI", "NADHIF RAZA", "NINDITA", "NINDYA", "RAFA BB", 
    "RAIS", "RAKA", "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"
]

daftar_blokir = []  # Tambahkan nama yang di blokir di sini

# ====================== DATABASE ======================
DB_FILE = "kelas4eu.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS jadwal (
            id INTEGER PRIMARY KEY,
            hari TEXT,
            jam TEXT,
            mata_pelajaran TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pr (
            id INTEGER PRIMARY KEY,
            tanggal_input TEXT,
            mata_pelajaran TEXT,
            judul_pr TEXT,
            deadline TEXT,
            catatan TEXT,
            input_oleh TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_jadwal():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM jadwal", conn)
    conn.close()
    return df

def load_pr():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM pr", conn)
    conn.close()
    return df

def save_pr(new_pr):
    conn = sqlite3.connect(DB_FILE)
    new_pr.to_sql('pr', conn, if_exists='append', index=False)
    conn.close()

def delete_pr(pr_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM pr WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()

init_db()

# ====================== ADMIN PASSWORD ======================
ADMIN_PASSWORD = "12345"   # GANTI INI SESUKA KAMU!

# ====================== LOGIN SYSTEM ======================
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""

st.subheader("🔒 Verifikasi Siswa")
nama_pilihan = st.selectbox("Pilih Namamu:", daftar_siswa)

if st.button("Masuk", type="primary"):
    if nama_pilihan == "Pilih Nama Kamu...":
        st.warning("⚠️ Silakan pilih namamu terlebih dahulu!")
    elif nama_pilihan in daftar_blokir:
        st.error(f"❌ Maaf {nama_pilihan}, akunmu sedang diblokir!")
    else:
        st.session_state.sudah_login = True
        st.session_state.user_aktif = nama_pilihan
        st.success(f"✅ Selamat datang, {nama_pilihan}!")
        st.rerun()

if not st.session_state.sudah_login:
    st.stop()

# ====================== HALAMAN UTAMA ======================
st.success(f"Halo, **{st.session_state.user_aktif}** 👋")
if st.button("Keluar / Ganti Nama"):
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""
    st.rerun()

st.divider()

menu = st.sidebar.selectbox("Menu", ["📅 Jadwal Pelajaran", "📝 PR & Tugas"])

# ====================== JADWAL PELAJARAN ======================
if menu == "📅 Jadwal Pelajaran":
    st.header("📅 Jadwal Pelajaran")
    
    password = st.text_input("Password Admin (untuk mengedit)", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("Mode Admin Aktif")
        with st.form("tambah_jadwal"):
            col1, col2 = st.columns(2)
            with col1:
                hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
                jam = st.text_input("Jam Pelajaran")
            with col2:
                mapel = st.text_input("Mata Pelajaran")
            if st.form_submit_button("Tambahkan Jadwal"):
                if jam and mapel:
                    conn = sqlite3.connect(DB_FILE)
                    conn.execute("INSERT INTO jadwal (hari, jam, mata_pelajaran) VALUES (?, ?, ?)",
                               (hari, jam, mapel))
                    conn.commit()
                    conn.close()
                    st.success("Jadwal berhasil ditambahkan!")
                    st.rerun()

    df_jadwal = load_jadwal()
    if not df_jadwal.empty:
        for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
            jadwal_hari = df_jadwal[df_jadwal['hari'] == hari]
            if not jadwal_hari.empty:
                st.subheader(hari)
                st.dataframe(jadwal_hari[['jam', 'mata_pelajaran']], 
                           use_container_width=True, hide_index=True)
    else:
        st.info("Jadwal belum ada. Masuk mode admin untuk menambahkan.")

# ====================== PR & TUGAS ======================
elif menu == "📝 PR & Tugas":
    st.header("📝 Catatan PR & Tugas")

    with st.form("input_pr"):
        col1, col2 = st.columns(2)
        with col1:
            mapel = st.text_input("Mata Pelajaran *")
            deadline = st.date_input("Deadline", min_value=datetime.today().date())
        with col2:
            judul = st.text_input("Judul PR / Tugas *")
        
        catatan = st.text_area("Catatan Tambahan")
        submitted = st.form_submit_button("Simpan PR")

        if submitted:
            if mapel and judul:
                new_pr = pd.DataFrame([{
                    "tanggal_input": datetime.now().strftime("%Y-%m-%d"),
                    "mata_pelajaran": mapel,
                    "judul_pr": judul,
                    "deadline": str(deadline),
                    "catatan": catatan,
                    "input_oleh": st.session_state.user_aktif
                }])
                save_pr(new_pr)
                st.success("✅ PR berhasil disimpan!")
                st.rerun()
            else:
                st.error("Mata Pelajaran dan Judul PR wajib diisi.")

    # Tampilkan PR
    df_pr = load_pr()
    if not df_pr.empty:
        df_pr = df_pr.sort_values(by="deadline")
        st.subheader("Daftar PR yang Aktif")
        for _, row in df_pr.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.write(f"**{row['mata_pelajaran']}** — {row['judul_pr']}")
                    st.caption(f"Deadline: **{row['deadline']}** | Oleh: {row['input_oleh']}")
                    if row['catatan']:
                        st.write(row['catatan'])
                with col2:
                    if row['input_oleh'] == st.session_state.user_aktif:
                        if st.button("🗑 Hapus", key=f"hapus_{row['id']}"):
                            delete_pr(row['id'])
                            st.success("PR dihapus")
                            st.rerun()
    else:
        st.info("Belum ada PR yang dimasukkan.")

st.sidebar.caption("---\nKelas 4EU")
