import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ====================== CONFIG ======================
st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

st.title("📚 Kelas 9D")
st.caption("Jadwal Pelajaran & Catatan PR/Tugas")

# CSS Hide Streamlit Menu
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== DAFTAR SISWA KELAS 9D ======================
daftar_siswa = ["Pilih Nama Kamu...", "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", 
                "AZZAM", "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
                "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", "KEJORA", 
                "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", "NADHIF RAZA", "NINDITA", 
                "NINDYA", "RAFA BB", "RAIS", "RAKA", "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"]

# ====================== DATABASE ======================
DB_FILE = "kelas9d.db"   # Database baru untuk kelas 9D

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS jadwal 
                    (id INTEGER PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS pr 
                    (id INTEGER PRIMARY KEY, tanggal_input TEXT, mata_pelajaran TEXT, 
                     judul_pr TEXT, deadline TEXT, catatan TEXT, input_oleh TEXT)''')
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

def update_pr(pr_id, updated_data):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""UPDATE pr SET mata_pelajaran=?, judul_pr=?, deadline=?, catatan=? 
                    WHERE id=?""", 
                 (updated_data['mata_pelajaran'], updated_data['judul_pr'], 
                  updated_data['deadline'], updated_data['catatan'], pr_id))
    conn.commit()
    conn.close()

def delete_pr(pr_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM pr WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()

init_db()

# ====================== LOGIN ======================
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""
    st.session_state.edit_pr_id = None

if not st.session_state.sudah_login:
    st.subheader("🔒 Verifikasi Siswa Kelas 9D")
    nama_pilihan = st.selectbox("Pilih Namamu:", daftar_siswa)
    if st.button("Masuk", type="primary"):
        if nama_pilihan != "Pilih Nama Kamu...":
            st.session_state.sudah_login = True
            st.session_state.user_aktif = nama_pilihan
            st.rerun()
    st.stop()

# ====================== HALAMAN UTAMA ======================
st.success(f"Halo, **{st.session_state.user_aktif}** 👋 Selamat datang di Kelas 9D")
if st.button("Keluar / Ganti Nama"):
    st.session_state.sudah_login = False
    st.session_state.edit_pr_id = None
    st.rerun()

st.divider()

tab1, tab2 = st.tabs(["📅 Jadwal Pelajaran", "📝 PR & Tugas"])

# ====================== TAB JADWAL ======================
with tab1:
    st.header("📅 Jadwal Pelajaran")
    st.info("Semua siswa kelas 9D dapat menambahkan jadwal.")

    with st.form("tambah_jadwal"):
        col1, col2 = st.columns(2)
        with col1:
            hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
            jam = st.text_input("Jam Pelajaran (contoh: 07.00 - 08.00)")
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
        st.info("Belum ada jadwal pelajaran.")

# ====================== TAB PR ======================
with tab2:
    st.header("📝 PR & Tugas")

    edit_mode = st.session_state.edit_pr_id is not None
    st.subheader("Edit PR" if edit_mode else "Tambah PR Baru")

    with st.form("form_pr"):
        col1, col2 = st.columns(2)
        with col1:
            mapel = st.text_input("Mata Pelajaran *")
            deadline = st.date_input("Deadline", min_value=datetime.today().date())
        with col2:
            judul = st.text_input("Judul PR / Tugas *")
        
        catatan = st.text_area("Catatan (opsional)")
        
        submit_label = "Simpan Perubahan" if edit_mode else "Simpan PR"
        submitted = st.form_submit_button(submit_label)

        if submitted:
            if mapel and judul:
                data = {
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
            else:
                st.error("Mata Pelajaran dan Judul PR wajib diisi.")

    # Tampilkan Daftar PR
    df_pr = load_pr()
    if not df_pr.empty:
        df_pr = df_pr.sort_values(by="deadline")
        st.subheader("Daftar PR")
        for _, row in df_pr.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([5, 1, 1])
                with col1:
                    st.write(f"**{row['mata_pelajaran']}** — {row['judul_pr']}")
                    st.caption(f"Deadline: **{row['deadline']}** | Oleh: {row['input_oleh']}")
                    if row['catatan']:
                        st.write(row['catatan'])
                with col2:
                    if row['input_oleh'] == st.session_state.user_aktif:
                        if st.button("✏️ Edit", key=f"edit_{row['id']}"):
                            st.session_state.edit_pr_id = row['id']
                            st.rerun()
                with col3:
                    if row['input_oleh'] == st.session_state.user_aktif:
                        if st.button("🗑 Hapus", key=f"del_{row['id']}"):
                            delete_pr(row['id'])
                            st.success("PR dihapus")
                            st.rerun()
    else:
        st.info("Belum ada PR yang dimasukkan.")

st.caption("--- Kelas 9D")
