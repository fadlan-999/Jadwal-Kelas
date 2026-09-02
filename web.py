import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# ====================== CONFIG ======================
st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main {background-color: #f8f9fa;}
    .stContainer {border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
    h1 {color: #1a237e;}
    .deadline-today {background-color: #ffebee; border-left: 5px solid #f44336;}
    .deadline-soon {background-color: #fff3e0; border-left: 5px solid #ff9800;}
</style>
""", unsafe_allow_html=True)

st.title("📚 Kelas 9D")
st.caption("Jadwal Pelajaran & Catatan PR/Tugas Tahun Pelajaran 2025/2026")

# ====================== DATA SISWA ======================
daftar_siswa = ["Pilih Nama Kamu...", "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", 
                "AZZAM", "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
                "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", "KEJORA", 
                "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", "NADHIF RAZA", "NINDITA", 
                "NINDYA", "RAFA BB", "RAIS", "RAKA", "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"]

DB_FILE = "kelas9d.db"

# ====================== DATABASE SETUP ======================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DROP TABLE IF EXISTS jadwal")
    conn.execute("DROP TABLE IF EXISTS pr")
    conn.execute('''CREATE TABLE jadwal 
                    (id INTEGER PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT, guru TEXT)''')
    conn.execute('''CREATE TABLE pr 
                    (id INTEGER PRIMARY KEY, hari TEXT, tanggal_input TEXT, mata_pelajaran TEXT, 
                     judul_pr TEXT, deadline TEXT, catatan TEXT, input_oleh TEXT)''')
    conn.commit()
    conn.close()

def seed_jadwal():
    conn = sqlite3.connect(DB_FILE)
    data = [
        ("Senin", "07.40-09.00", "MULOK", "Bu Asnani & Umi Megawati"),
        ("Senin", "09.00-10.40", "FIQIH", "Bu Ondiana"),
        ("Senin", "10.40-12.00", "SKI", "Bu Ida"),
        ("Senin", "12.30-13.50", "ALQURAN HADIST", "Pak Iswadi"),
        ("Senin", "13.50-15.10", "BAHASA INDONESIA", "Bu Irzawati"),
        ("Selasa", "07.00-08.20", "IPA", "Bu Susi"),
        ("Selasa", "08.20-09.40", "SBK", "Bu Ermawati"),
        ("Selasa", "10.00-11.20", "MATEMATIKA", "Bu Asnani"),
        ("Selasa", "11.20-13.50", "BAHASA INDONESIA", "Bu Irzawati"),
        ("Selasa", "13.50-15.10", "IPS", "Bu Lia Lisa"),
        ("Rabu", "07.00-08.20", "MATEMATIKA", "Bu Asnani"),
        ("Rabu", "08.20-09.40", "PJOK", "Bu Maya"),
        ("Rabu", "10.00-12.00", "TIK", "Bu Amilatun Khasanah"),
        ("Rabu", "12.30-13.50", "Coding", "Bu Nona"),
        ("Rabu", "13.50-15.10", "BAHASA INGGRIS", "Ma'am Nur"),
        ("Kamis", "07.00-09.00", "BAHASA ARAB", "Buyah Fauzan"),
        ("Kamis", "09.00-10.40", "BAHASA INGGRIS", "Ma'am Nur"),
        ("Kamis", "10.40-13.10", "AQIDAH AKHLAK", "Umi Elsa"),
        ("Kamis", "13.10-14.30", "IPS", "Bu Lia Lisa"),
        ("Jumat", "07.40-09.00", "IPA", "Bu Susi"),
        ("Jumat", "09.00-10.40", "PPKN", "Umi Kariana"),
        ("Jumat", "10.40-11.20", "BAHASA DAERAH", "Bu Relly Susanti"),
    ]
    conn.executemany("INSERT INTO jadwal (hari, jam, mata_pelajaran, guru) VALUES (?, ?, ?, ?)", data)
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

def update_pr(pr_id, data):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""UPDATE pr SET hari=?, mata_pelajaran=?, judul_pr=?, deadline=?, catatan=? 
                    WHERE id=?""", 
                 (data['hari'], data['mata_pelajaran'], data['judul_pr'], 
                  data['deadline'], data['catatan'], pr_id))
    conn.commit()
    conn.close()

def delete_pr(pr_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM pr WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()

# Inisialisasi
init_db()
seed_jadwal()

# ====================== SESSION STATE ======================
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""
    st.session_state.edit_pr_id = None

# ====================== LOGIN ======================
if not st.session_state.sudah_login:
    st.subheader("🔐 Verifikasi Siswa Kelas 9D")
    nama = st.selectbox("Pilih Namamu:", daftar_siswa)
    if st.button("Masuk", type="primary", use_container_width=True):
        if nama != "Pilih Nama Kamu...":
            st.session_state.sudah_login = True
            st.session_state.user_aktif = nama
            st.rerun()
    st.stop()

# ====================== MAIN APP ======================
st.success(f"👋 Halo, **{st.session_state.user_aktif}**!")
if st.button("Keluar / Ganti Nama"):
    st.session_state.sudah_login = False
    st.session_state.edit_pr_id = None
    st.rerun()

st.divider()

tab1, tab2 = st.tabs(["📅 Jadwal Pelajaran", "📝 PR & Tugas"])

# ====================== TAB 1: JADWAL ======================
with tab1:
    st.header("📅 Jadwal Pelajaran Kelas 9D")
    st.info("**Jam Sekolah**\nSenin–Rabu: 06.40–15.10 | Kamis: 06.40–14.30 | Jumat: 06.40–11.20")
    
    df_jadwal = load_jadwal()
    for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
        jadwal_hari = df_jadwal[df_jadwal['hari'] == hari]
        if not jadwal_hari.empty:
            st.subheader(f"🗓 {hari}")
            st.dataframe(jadwal_hari[['jam', 'mata_pelajaran', 'guru']], 
                        use_container_width=True, hide_index=True)

# ====================== TAB 2: PR & TUGAS ======================
with tab2:
    st.header("📝 PR & Tugas")

    # --- FORM ---
    edit_mode = st.session_state.edit_pr_id is not None
    with st.form("pr_form"):
        st.subheader("Edit PR" if edit_mode else "Tambah PR Baru")
        
        hari = st.selectbox("Hari *", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
        col1, col2 = st.columns(2)
        with col1:
            mapel = st.text_input("Mata Pelajaran *")
        with col2:
            judul = st.text_input("Judul PR / Tugas *")
        
        deadline = st.date_input("Deadline", value=date.today(), min_value=date.today())
        catatan = st.text_area("Catatan (opsional)")
        
        submitted = st.form_submit_button("💾 Simpan Perubahan" if edit_mode else "💾 Simpan PR", 
                                        use_container_width=True)
        
        if submitted:
            if not mapel or not judul:
                st.error("Mata Pelajaran dan Judul PR wajib diisi!")
            else:
                data = {
                    "hari": hari,
                    "mata_pelajaran": mapel,
                    "judul_pr": judul,
                    "deadline": str(deadline),
                    "catatan": catatan
                }
                if edit_mode:
                    update_pr(st.session_state.edit_pr_id, data)
                    st.success("✅ PR berhasil diupdate!")
                    st.session_state.edit_pr_id = None
                else:
                    new_data = pd.DataFrame([{
                        **data,
                        "tanggal_input": datetime.now().strftime("%Y-%m-%d"),
                        "input_oleh": st.session_state.user_aktif
                    }])
                    save_pr(new_data)
                    st.success("✅ PR berhasil disimpan!")
                st.rerun()

    # --- DAFTAR PR ---
    df_pr = load_pr()
    if not df_pr.empty:
        df_pr = df_pr.sort_values(by=["hari", "deadline"])
        st.subheader("Daftar PR")
        
        for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
            pr_hari = df_pr[df_pr['hari'] == hari]
            if not pr_hari.empty:
                st.markdown(f"### 🗓 {hari}")
                for _, row in pr_hari.iterrows():
                    deadline_date = datetime.strptime(row['deadline'], "%Y-%m-%d").date()
                    days_left = (deadline_date - date.today()).days
                    
                    if days_left < 0:
                        css_class = "deadline-today"
                        status = "⛔ Lewat Deadline"
                    elif days_left == 0:
                        css_class = "deadline-today"
                        status = "🔴 Hari Ini"
                    elif days_left <= 3:
                        css_class = "deadline-soon"
                        status = f"⚠️ {days_left} hari lagi"
                    else:
                        css_class = ""
                        status = f"🟢 {days_left} hari lagi"
                    
                    with st.container(border=True):
                        st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([6, 2, 2])
                        with col1:
                            st.write(f"**{row['mata_pelajaran']}** — {row['judul_pr']}")
                            st.caption(f"Deadline: **{row['deadline']}** | Oleh: {row['input_oleh']}")
                            if row['catatan']:
                                st.write(row['catatan'])
                        with col2:
                            st.caption(status)
                        with col3:
                            if row['input_oleh'] == st.session_state.user_aktif:
                                if st.button("✏️ Edit", key=f"edit_{row['id']}"):
                                    st.session_state.edit_pr_id = row['id']
                                    st.rerun()
                                if st.button("🗑 Hapus", key=f"del_{row['id']}"):
                                    delete_pr(row['id'])
                                    st.success("PR dihapus")
                                    st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada PR yang dimasukkan. Tambahkan PR di atas.")

st.caption("--- Kelas 9D | Dibuat untuk memudahkan belajar")
