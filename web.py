import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

# ====================== DESAIN ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600&display=swap');
    .main {background-color: #0f172a; color: #e2e8f0;}
    #MainMenu, header, footer {visibility: hidden;}
    h1 {font-family: 'Poppins', sans-serif; color: #67e8f9; font-weight: 600;}
    .subtitle {color: #94a3b8; font-size: 1.05rem;}
    .card {background-color: #1e2937; padding: 18px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>✦ Kelas 9D</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Modern Classroom Management • Tahun Pelajaran 2026/2027</p>", unsafe_allow_html=True)

# ====================== DATA ======================
daftar_siswa = ["Pilih Nama Kamu...", "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", 
                "AZZAM", "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
                "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", "KEJORA", 
                "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", "NADHIF RAZA", "NINDITA", 
                "NINDYA", "RAFA BB", "RAIS", "RAKA", "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"]

daftar_mapel = [
    "MULOK", "FIQIH", "SKI", "ALQURAN HADIST", "BAHASA INDONESIA",
    "IPA", "MATEMATIKA", "IPS", "PPKN", "PJOK", "SBK", "TIK", "Coding",
    "BAHASA INGGRIS", "BAHASA ARAB", "AQIDAH AKHLAK", "BAHASA DAERAH", "Lainnya"
]

DB_FILE = "kelas9d.db"

# ====================== DATABASE ======================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DROP TABLE IF EXISTS jadwal")
    conn.execute("DROP TABLE IF EXISTS pr")
    conn.execute('''CREATE TABLE jadwal (id INTEGER PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT, guru TEXT)''')
    conn.execute('''CREATE TABLE pr 
                    (id INTEGER PRIMARY KEY, hari TEXT, tanggal_input TEXT, mata_pelajaran TEXT, 
                     judul_pr TEXT, tanggal_pengumpulan TEXT, catatan TEXT, input_oleh TEXT)''')
    conn.commit()
    conn.close()

def seed_jadwal():
    conn = sqlite3.connect(DB_FILE)
    data = [ ... ]  # (sama seperti sebelumnya, saya singkat)
    # Isi data jadwal kamu tetap sama
    conn.executemany("INSERT INTO jadwal (hari, jam, mata_pelajaran, guru) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def load_pr():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM pr ORDER BY tanggal_input DESC", conn)
    conn.close()
    return df

def save_pr(new_pr):
    conn = sqlite3.connect(DB_FILE)
    new_pr.to_sql('pr', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

def delete_pr(pr_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM pr WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()

init_db()
seed_jadwal()

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

st.success(f"Selamat datang kembali, **{st.session_state.user_aktif}** 👋")
if st.button("Ganti Akun"):
    st.session_state.sudah_login = False
    st.session_state.edit_pr_id = None
    st.rerun()

st.divider()

tab1, tab2, tab3 = st.tabs(["📅 Jadwal Pelajaran", "📝 Input PR", "📜 Riwayat PR"])

with tab1:
    st.markdown("### 📅 Jadwal Pelajaran Kelas 9D")
    st.info("**Jam Sekolah**\nSenin–Rabu: 06.40–15.10 | Kamis: 06.40–14.30 | Jumat: 06.40–11.20")
    df_jadwal = pd.read_sql("SELECT * FROM jadwal", sqlite3.connect(DB_FILE))
    for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
        jadwal_hari = df_jadwal[df_jadwal['hari'] == hari]
        if not jadwal_hari.empty:
            st.markdown(f"**🗓 {hari}**")
            st.dataframe(jadwal_hari[['jam', 'mata_pelajaran', 'guru']], use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### 📝 Input PR & Tugas")
    
    with st.form("pr_form"):
        st.subheader("Tambah PR Baru")
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
        mapel = st.selectbox("Mata Pelajaran *", daftar_mapel)
        if mapel == "Lainnya":
            mapel = st.text_input("Masukkan Mata Pelajaran")

        judul = st.text_input("Judul PR / Tugas *")
        tanggal_pengumpulan = st.date_input("Tanggal Pengumpulan", value=date.today())
        catatan = st.text_area("Catatan (opsional)")
        
        if st.form_submit_button("Simpan PR", use_container_width=True):
            if mapel and judul and mapel.strip() != "":
                data = {
                    "hari": hari,
                    "mata_pelajaran": mapel,
                    "judul_pr": judul,
                    "tanggal_pengumpulan": str(tanggal_pengumpulan),
                    "catatan": catatan,
                    "tanggal_input": datetime.now().strftime("%Y-%m-%d"),
                    "input_oleh": st.session_state.user_aktif
                }
                save_pr(pd.DataFrame([data]))
                st.success("✅ PR berhasil disimpan!")
                st.rerun()        # ← Ini yang paling penting
            else:
                st.error("Mata Pelajaran dan Judul PR wajib diisi!")

with tab3:
    st.markdown("### 📜 Riwayat PR")
    df_riwayat = load_pr()
    
    if df_riwayat.empty:
        st.info("Belum ada data riwayat PR.")
    else:
        df_riwayat['tanggal_input'] = pd.to_datetime(df_riwayat['tanggal_input'])
        df_riwayat['bulan'] = df_riwayat['tanggal_input'].dt.strftime('%B %Y')
        df_riwayat = df_riwayat.sort_values(by='tanggal_input', ascending=False)
        
        for bulan in df_riwayat['bulan'].unique():
            df_bulan = df_riwayat[df_riwayat['bulan'] == bulan]
            with st.expander(f"📅 {bulan} ({len(df_bulan)} PR)", expanded=True):
                for mapel in sorted(df_bulan['mata_pelajaran'].unique()):
                    df_mapel = df_bulan[df_bulan['mata_pelajaran'] == mapel]
                    st.markdown(f"**{mapel}** ({len(df_mapel)} tugas)")
                    for _, row in df_mapel.iterrows():
                        with st.container(border=True):
                            st.write(f"**{row['hari']}** — {row['judul_pr']}")
                            st.caption(f"Pengumpulan: **{row['tanggal_pengumpulan']}** | Oleh: {row['input_oleh']}")
                            if row['catatan']:
                                st.write(row['catatan'])
                    st.markdown("---")

st.caption("--- Kelas 9D")
