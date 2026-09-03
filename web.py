import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

# ====================== CSS DIPERBAIKI (Saran #8) ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #172554);
    color: #e2e8f0;
}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

h1 {
    font-family: 'Poppins', sans-serif;
    color: #67e8f9;
    font-weight: 600;
}
.subtitle {color: #94a3b8; font-size: 1.05rem;}
.card {background-color: #1e2937; padding: 18px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 12px;}

.stTabs [data-baseweb="tab-list"] {
    background-color: #1e2937;
    padding: 10px;
    border-radius: 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #14b8a6 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>✦ Kelas 9D</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Modern Classroom Management • Tahun Pelajaran 2026/2027</p>", unsafe_allow_html=True)

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

BULAN_INDO = {
    "January": "Januari", "February": "Februari", "March": "Maret",
    "April": "April", "May": "Mei", "June": "Juni",
    "July": "Juli", "August": "Agustus", "September": "September",
    "October": "Oktober", "November": "November", "December": "Desember"
}

def format_bulan_indo(tanggal_dt):
    bulan_en = tanggal_dt.strftime('%B')
    tahun = tanggal_dt.strftime('%Y')
    return f"{BULAN_INDO.get(bulan_en, bulan_en)} {tahun}"

def status_deadline(tanggal_pengumpulan):
    """Saran #5: Status deadline dengan warna"""
    deadline = pd.to_datetime(tanggal_pengumpulan).date()
    hari_ini = date.today()
    selisih = (deadline - hari_ini).days
    
    if selisih < 0:
        return "🔴 Terlambat"
    elif selisih == 0:
        return "🟠 Dikumpulkan hari ini"
    elif selisih == 1:
        return "🟡 Dikumpulkan besok"
    else:
        return f"🟢 {selisih} hari lagi"

DB_FILE = "kelas9d.db"

# ====================== DATABASE ======================
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS jadwal 
                        (id INTEGER PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT, guru TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS pr 
                        (id INTEGER PRIMARY KEY, hari TEXT, tanggal_input TEXT, mata_pelajaran TEXT, 
                         judul_pr TEXT, tanggal_pengumpulan TEXT, catatan TEXT, input_oleh TEXT,
                         status TEXT DEFAULT 'aktif')''')
        cursor = conn.execute("PRAGMA table_info(pr)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'status' not in columns:
            conn.execute("ALTER TABLE pr ADD COLUMN status TEXT DEFAULT 'aktif'")

def seed_jadwal():
    with sqlite3.connect(DB_FILE) as conn:
        count = conn.execute("SELECT COUNT(*) FROM jadwal").fetchone()[0]
        if count == 0:
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

def load_jadwal():
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql("SELECT * FROM jadwal", conn)

def load_pr_aktif():
    """Saran #6: Diurutkan berdasarkan tanggal_pengumpulan (deadline terdekat di atas)"""
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql("""
            SELECT * FROM pr 
            WHERE status = 'aktif' 
            ORDER BY tanggal_pengumpulan ASC
        """, conn)

def load_semua_pr():
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql("SELECT * FROM pr ORDER BY tanggal_input DESC", conn)

def pr_sudah_ada(mapel, judul, tanggal_pengumpulan):
    """Saran #7: Cek duplikasi PR"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT COUNT(*) FROM pr
            WHERE mata_pelajaran = ? AND judul_pr = ? AND tanggal_pengumpulan = ?
            AND status = 'aktif'
        """, (mapel, judul, str(tanggal_pengumpulan)))
        return cursor.fetchone()[0] > 0

def save_pr(new_pr):
    with sqlite3.connect(DB_FILE) as conn:
        new_pr.to_sql('pr', conn, if_exists='append', index=False)


def arsipkan_pr(pr_id):
    """Ubah status PR menjadi selesai"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "UPDATE pr SET status = 'selesai' WHERE id = ?",
            (pr_id,)
        )


def hapus_permanen(pr_id):
    """Hapus PR selamanya dari database"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM pr WHERE id = ?",
            (pr_id,)
        )


def batalkan_selesai(pr_id):
    """Kembalikan status dari 'selesai' menjadi 'aktif' lagi"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "UPDATE pr SET status = 'aktif' WHERE id = ?",
            (pr_id,)
        )
init_db()
seed_jadwal()

# ====================== LOGIN ======================
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False
    st.session_state.user_aktif = ""

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
    st.session_state.user_aktif = ""
    st.rerun()

st.divider()

# ====================== DASHBOARD (Saran #9) ======================
df_semua = load_semua_pr()
df_aktif_count = load_pr_aktif()

total_pr = len(df_semua)
pr_aktif_jumlah = len(df_aktif_count)
pr_selesai = len(df_semua[df_semua['status'] == 'selesai']) if not df_semua.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📋 Total PR", total_pr)
with col2:
    st.metric("🟢 PR Aktif", pr_aktif_jumlah)
with col3:
    st.metric("✅ Selesai", pr_selesai)

st.divider()

tab1, tab2, tab3 = st.tabs(["📅 Jadwal Pelajaran", "📝 Input PR", "📜 Riwayat PR"])

with tab1:
    st.markdown("### 📅 Jadwal Pelajaran Kelas 9D")
    st.info("**Jam Sekolah**\nSenin–Rabu: 06.40–15.10 | Kamis: 06.40–14.30 | Jumat: 06.40–11.20")
    df_jadwal = load_jadwal()
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
            if mapel and judul and str(mapel).strip() != "":
                if pr_sudah_ada(mapel, judul, tanggal_pengumpulan):
                    st.error("❌ PR ini sudah pernah dimasukkan! (Mata Pelajaran, Judul, dan Tanggal Pengumpulan sama). Tidak disimpan lagi.")
                else:
                    data = {
                        "hari": hari, "mata_pelajaran": mapel, "judul_pr": judul,
                        "tanggal_pengumpulan": str(tanggal_pengumpulan), "catatan": catatan,
                        "tanggal_input": datetime.now().strftime("%Y-%m-%d"),
                        "input_oleh": st.session_state.user_aktif,
                        "status": "aktif"
                    }
                    save_pr(pd.DataFrame([data]))
                    st.success("✅ PR berhasil disimpan!")
                    st.rerun()
            else:
                st.error("Mata Pelajaran dan Judul PR wajib diisi!")

    df_pr = load_pr_aktif()
    if not df_pr.empty:
        st.markdown("### PR Aktif")
        st.caption("Diurutkan berdasarkan tanggal pengumpulan terdekat")
        for _, row in df_pr.iterrows():
            status = status_deadline(row['tanggal_pengumpulan'])
            with st.container(border=True):
                col1, col2 = st.columns([6, 2])
                with col1:
                    st.write(f"**{row['hari']} • {row['mata_pelajaran']}** — {row['judul_pr']}")
                    st.caption(f"Pengumpulan: **{row['tanggal_pengumpulan']}** | {status} | Oleh: {row['input_oleh']}")
                    if row['catatan']:
                        st.write(row['catatan'])
                with col2:
                    if row['input_oleh'] == st.session_state.user_aktif:
                        if st.button("✅ Selesaikan", key=f"selesai_{row['id']}"):
                            arsipkan_pr(row['id'])
                            st.success("PR ditandai selesai!")
                            st.rerun()
    else:
        st.info("Tidak ada PR aktif saat ini.")

with tab3:
    st.markdown("### 📜 Riwayat PR")
    st.caption("Menampilkan SEMUA PR yang pernah dimasukkan, termasuk yang sudah selesai")
    
    df_riwayat = load_semua_pr()
    if df_riwayat.empty:
        st.info("Belum ada data riwayat PR.")
    else:
        df_riwayat['tanggal_input_dt'] = pd.to_datetime(df_riwayat['tanggal_input'])
        df_riwayat['bulan'] = df_riwayat['tanggal_input_dt'].apply(format_bulan_indo)
        df_riwayat = df_riwayat.sort_values(by='tanggal_input_dt', ascending=False)
        
        bulan_unik = df_riwayat[['bulan', 'tanggal_input_dt']].drop_duplicates().sort_values('tanggal_input_dt', ascending=False)['bulan'].tolist()
        
        for bulan in bulan_unik:
            df_bulan = df_riwayat[df_riwayat['bulan'] == bulan]
            with st.expander(f"📅 {bulan} ({len(df_bulan)} PR)", expanded=True):
                for mapel_name in sorted(df_bulan['mata_pelajaran'].unique()):
                    df_mapel = df_bulan[df_bulan['mata_pelajaran'] == mapel_name]
                    st.markdown(f"**{mapel_name}** ({len(df_mapel)} tugas)")
                    for _, row in df_mapel.iterrows():
                        status_badge = "✅ Selesai" if row['status'] == 'selesai' else "🟢 Aktif"
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([5, 1.5, 1.5])
                            with col1:
                                st.write(f"**{row['hari']}** — {row['judul_pr']}")
                                st.caption(f"Pengumpulan: **{row['tanggal_pengumpulan']}** | Oleh: {row['input_oleh']}")
                                if row['catatan']:
                                    st.write(row['catatan'])
                            with col2:
                                st.caption(status_badge)
                                # Tombol batalkan hanya muncul kalau status = selesai dan milik user tsb
                                if row['status'] == 'selesai' and row['input_oleh'] == st.session_state.user_aktif:
                                    if st.button("↩️ Batalkan", key=f"batal_{row['id']}"):
                                        batalkan_selesai(row['id'])
                                        st.success("Dikembalikan ke PR Aktif!")
                                        st.rerun()
                            with col3:
                                # Tombol hapus permanen, hanya untuk yang punya PR itu
                                if row['input_oleh'] == st.session_state.user_aktif:
                                    if st.button("🗑️ Hapus", key=f"hapus_{row['id']}"):
                                        hapus_permanen(row['id'])
                                        st.success("PR dihapus permanen!")
                                        st.rerun()
                    st.markdown("---")

st.caption("--- Kelas 9D")
