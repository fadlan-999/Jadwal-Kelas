import streamlit as st
import pandas as pd
from datetime import datetime, date
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Kelas 9D", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
    --h: 222;
    --c-950: hsl(var(--h), 48%, 5%);
    --c-900: hsl(var(--h), 42%, 8%);
    --c-850: hsl(var(--h), 38%, 11%);
    --c-800: hsl(var(--h), 34%, 14%);
    --c-700: hsl(var(--h), 28%, 20%);
    --c-500: hsl(var(--h), 22%, 42%);
    --c-400: hsl(var(--h), 24%, 58%);
    --c-300: hsl(var(--h), 32%, 72%);
    --c-100: hsl(var(--h), 50%, 93%);
    --accent: hsl(var(--h), 78%, 70%);
    --line: hsla(var(--h), 40%, 80%, .12);
    --line-strong: hsla(var(--h), 40%, 80%, .22);
    --glass: hsla(var(--h), 40%, 12%, .55);
}

.stApp {
    background:
      radial-gradient(ellipse 70% 55% at 15% 10%, hsla(var(--h), 70%, 45%, .22), transparent 65%),
      radial-gradient(ellipse 60% 50% at 85% 85%, hsla(var(--h), 60%, 40%, .18), transparent 65%),
      linear-gradient(160deg, var(--c-900) 0%, var(--c-950) 60%, hsl(var(--h),45%,4%) 100%);
    color: var(--c-100);
    font-family: 'Manrope', system-ui, sans-serif;
}
.stApp::before{
    content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
    background-image:
      linear-gradient(var(--line) 1px, transparent 1px),
      linear-gradient(90deg, var(--line) 1px, transparent 1px);
    background-size: 72px 72px;
    mask-image: radial-gradient(ellipse 80% 70% at 50% 30%, #000 30%, transparent 100%);
    -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 30%, #000 30%, transparent 100%);
}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

h1 {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    letter-spacing: -.02em;
    background: linear-gradient(135deg, var(--c-100), var(--accent));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.subtitle {color: var(--c-400); font-size: 1.02rem; font-family: 'JetBrains Mono', monospace;}

[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {
    background: linear-gradient(180deg, hsla(var(--h),40%,16%,.55), hsla(var(--h),42%,9%,.65));
    border: 1px solid var(--line-strong) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px);
}

[data-testid="stMetric"] {
    background: linear-gradient(180deg, hsla(var(--h),40%,16%,.55), hsla(var(--h),42%,9%,.65));
    border: 1px solid var(--line-strong);
    border-radius: 16px;
    padding: 16px 18px;
    backdrop-filter: blur(16px);
}
[data-testid="stMetricValue"] { color: var(--c-100); font-family: 'JetBrains Mono', monospace; }

.stTabs [data-baseweb="tab-list"] {
    background: hsla(var(--h),45%,5%,.55);
    border: 1px solid var(--line);
    padding: 5px;
    border-radius: 14px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: var(--c-400);
    font-weight: 600;
    border-radius: 10px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--c-700), var(--c-800)) !important;
    color: var(--c-100) !important;
    border: 1px solid var(--line-strong) !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-border"] {
    background-color: transparent !important;
}

.stButton button, .stFormSubmitButton button {
    background: linear-gradient(135deg, var(--c-300), var(--accent)) !important;
    color: var(--c-950) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] {
    background: hsla(var(--h),40%,12%,.4);
    border: 1px solid var(--line-strong);
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>✦ Kelas 9D</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Modern Classroom Management • Tahun Pelajaran 2026/2027</p>", unsafe_allow_html=True)

# ====================== KONSTANTA ======================
ADMIN_ACCOUNTS = ["FADLAN"]

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

# ====================== DATABASE ======================
@st.cache_resource
def get_engine():
    db_url = st.secrets["SUPABASE_DB_URL"]
    return create_engine(db_url, pool_pre_ping=True)

engine = get_engine()

def init_db():
    with engine.begin() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS jadwal
                        (id SERIAL PRIMARY KEY, hari TEXT, jam TEXT, mata_pelajaran TEXT, guru TEXT)'''))
        conn.execute(text('''CREATE TABLE IF NOT EXISTS pr
                        (id SERIAL PRIMARY KEY, hari TEXT, tanggal_input TEXT, mata_pelajaran TEXT,
                         judul_pr TEXT, tanggal_pengumpulan TEXT, catatan TEXT, input_oleh TEXT,
                         status TEXT DEFAULT 'aktif')'''))
        columns = [row[0] for row in conn.execute(text(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'pr'"
        )).fetchall()]
        if 'status' not in columns:
            conn.execute(text("ALTER TABLE pr ADD COLUMN status TEXT DEFAULT 'aktif'"))

def seed_jadwal():
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM jadwal")).scalar()
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
            rows = [{"hari": h, "jam": j, "mapel": m, "guru": g} for h, j, m, g in data]
            conn.execute(
                text("INSERT INTO jadwal (hari, jam, mata_pelajaran, guru) VALUES (:hari, :jam, :mapel, :guru)"),
                rows
            )

def load_jadwal():
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT * FROM jadwal"), conn)

def load_pr_aktif():
    with engine.connect() as conn:
        return pd.read_sql(text("""
            SELECT * FROM pr
            WHERE status = 'aktif'
            ORDER BY tanggal_pengumpulan ASC
        """), conn)

def load_semua_pr():
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT * FROM pr ORDER BY tanggal_input DESC"), conn)

def pr_sudah_ada(mapel, judul, tanggal_pengumpulan):
    with engine.connect() as conn:
        hasil = conn.execute(text("""
            SELECT COUNT(*) FROM pr
            WHERE mata_pelajaran = :mapel AND judul_pr = :judul AND tanggal_pengumpulan = :tgl
            AND status = 'aktif'
        """), {"mapel": mapel, "judul": judul, "tgl": str(tanggal_pengumpulan)}).scalar()
        return hasil > 0

def save_pr(new_pr):
    with engine.begin() as conn:
        new_pr.to_sql('pr', conn, if_exists='append', index=False)

def arsipkan_pr(pr_id):
    with engine.begin() as conn:
        conn.execute(text("UPDATE pr SET status = 'selesai' WHERE id = :id"), {"id": pr_id})

def hapus_permanen(pr_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM pr WHERE id = :id"), {"id": pr_id})

def batalkan_selesai(pr_id):
    with engine.begin() as conn:
        conn.execute(text("UPDATE pr SET status = 'aktif' WHERE id = :id"), {"id": pr_id})

@st.cache_resource
def setup_database():
    init_db()
    seed_jadwal()
    return True

setup_database()

# ====================== LOGIN ======================

# Pastikan setiap session_state selalu tersedia
if "sudah_login" not in st.session_state:
    st.session_state.sudah_login = False

if "user_aktif" not in st.session_state:
    st.session_state.user_aktif = ""

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# ====================== HALAMAN LOGIN ======================
if not st.session_state.sudah_login:

    st.markdown("### Silakan verifikasi identitasmu")

    nama = st.selectbox(
        "Pilih nama kamu",
        daftar_siswa,
        label_visibility="collapsed"
    )

    # ==================================================
    # FADLAN = ADMIN → WAJIB PASSWORD
    # ==================================================
    if nama == "FADLAN":

        password = st.text_input(
            "🔐 Password Admin",
            type="password",
            placeholder="Masukkan password admin"
        )

        if st.button(
            "👑 Masuk sebagai Admin",
            type="primary",
            use_container_width=True
        ):

            admin_password = st.secrets.get(
                "ADMIN_PASSWORD",
                ""
            )

            if not admin_password:
                st.error(
                    "⚠️ Password admin belum diatur di Streamlit Secrets."
                )

            elif password == admin_password:

                st.session_state.sudah_login = True
                st.session_state.user_aktif = "FADLAN"
                st.session_state.is_admin = True

                st.rerun()

            else:
                st.error("❌ Password admin salah!")


    # ==================================================
    # SISWA BIASA → TANPA PASSWORD
    # ==================================================
    elif nama != "Pilih Nama Kamu...":

        if st.button(
            "Masuk ke Kelas 9D",
            type="primary",
            use_container_width=True
        ):

            st.session_state.sudah_login = True
            st.session_state.user_aktif = nama
            st.session_state.is_admin = False

            st.rerun()

    else:
        st.info("Silakan pilih nama terlebih dahulu.")

    st.stop()


# ====================== DATA LOGIN ======================

user_aktif = st.session_state.user_aktif
is_admin = st.session_state.is_admin

# ====================== DASHBOARD ======================
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

# ====================== TAB 1: JADWAL ======================
with tab1:
    st.markdown("### 📅 Jadwal Pelajaran Kelas 9D")
    st.info("**Jam Sekolah**\nSenin–Rabu: 06.40–15.10 | Kamis: 06.40–14.30 | Jumat: 06.40–11.20")
    df_jadwal = load_jadwal()
    for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
        jadwal_hari = df_jadwal[df_jadwal['hari'] == hari]
        if not jadwal_hari.empty:
            st.markdown(f"**🗓 {hari}**")
            st.dataframe(jadwal_hari[['jam', 'mata_pelajaran', 'guru']], use_container_width=True, hide_index=True)

# ====================== TAB 2: INPUT PR ======================
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
                    st.error("❌ PR ini sudah pernah dimasukkan! Tidak disimpan lagi.")
                else:
                    data = {
                        "hari": hari, "mata_pelajaran": mapel, "judul_pr": judul,
                        "tanggal_pengumpulan": str(tanggal_pengumpulan), "catatan": catatan,
                        "tanggal_input": datetime.now().strftime("%Y-%m-%d"),
                        "input_oleh": user_aktif,
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
        for idx, (_, row) in enumerate(df_pr.iterrows()):
            status = status_deadline(row['tanggal_pengumpulan'])
            # Admin atau pemilik PR bisa selesaikan
            boleh_selesaikan = (row['input_oleh'] == user_aktif) or is_admin
            with st.container(border=True):
                col1, col2 = st.columns([6, 2])
                with col1:
                    st.write(f"**{row['hari']} • {row['mata_pelajaran']}** — {row['judul_pr']}")
                    st.caption(f"Pengumpulan: **{row['tanggal_pengumpulan']}** | {status} | Oleh: {row['input_oleh']}")
                    if row['catatan']:
                        st.write(row['catatan'])
                with col2:
                    if boleh_selesaikan:
                        if st.button("✅ Selesaikan", key=f"selesai_tab2_{row['id']}_{idx}"):
                            arsipkan_pr(row['id'])
                            st.success("PR ditandai selesai!")
                            st.rerun()
    else:
        st.info("Tidak ada PR aktif saat ini.")

# ====================== TAB 3: RIWAYAT ======================
with tab3:
    st.markdown("### 📜 Riwayat PR")
    st.caption("Menampilkan SEMUA PR yang pernah dimasukkan, termasuk yang sudah selesai")

    if is_admin:
        st.info("👑 Kamu login sebagai **Admin** — bisa kelola semua PR.")

    df_riwayat = load_semua_pr()

    if df_riwayat.empty:
        st.info("Belum ada data riwayat PR.")

    else:
        # Ubah tanggal input menjadi datetime
        df_riwayat['tanggal_input_dt'] = pd.to_datetime(
            df_riwayat['tanggal_input']
        )

        # Tambahkan nama bulan Indonesia
        df_riwayat['bulan'] = df_riwayat[
            'tanggal_input_dt'
        ].apply(format_bulan_indo)

        # Urutkan berdasarkan tanggal terbaru
        df_riwayat = df_riwayat.sort_values(
            by='tanggal_input_dt',
            ascending=False
        )

        # Ambil setiap bulan HANYA SATU KALI
        bulan_unik = (
            df_riwayat
            .drop_duplicates(subset=['bulan'])
            ['bulan']
            .tolist()
        )

        # ================= TAMPILKAN PER BULAN =================
        for bulan_idx, bulan in enumerate(bulan_unik):

            # Ambil semua PR pada bulan tersebut
            df_bulan = df_riwayat[
                df_riwayat['bulan'] == bulan
            ]

            with st.expander(
                f"📅 {bulan} ({len(df_bulan)} PR)",
                expanded=True
            ):

                # Kelompokkan berdasarkan mata pelajaran
                daftar_mapel_bulan = sorted(
                    df_bulan['mata_pelajaran'].unique()
                )

                for mapel_idx, mapel_name in enumerate(
                    daftar_mapel_bulan
                ):

                    df_mapel = df_bulan[
                        df_bulan['mata_pelajaran'] == mapel_name
                    ]

                    st.markdown(
                        f"**{mapel_name}** ({len(df_mapel)} tugas)"
                    )

                    # ================= TAMPILKAN PR =================
                    for row_idx, (_, row) in enumerate(
                        df_mapel.iterrows()
                    ):

                        # Status PR
                        status_badge = (
                            "✅ Selesai"
                            if row['status'] == 'selesai'
                            else "🟢 Aktif"
                        )

                        # Key unik untuk tombol Streamlit
                        unique_suffix = (
                            f"{bulan_idx}_"
                            f"{mapel_idx}_"
                            f"{row_idx}_"
                            f"{row['id']}"
                        )

                        # Admin bisa semua PR
                        # Siswa hanya bisa PR miliknya
                        boleh_aksi = (
                            row['input_oleh'] == user_aktif
                            or is_admin
                        )

                        with st.container(border=True):

                            col1, col2, col3 = st.columns(
                                [5, 1.5, 1.5]
                            )

                            # ================= INFO PR =================
                            with col1:

                                st.write(
                                    f"**{row['hari']}** — "
                                    f"{row['judul_pr']}"
                                )

                                st.caption(
                                    f"Pengumpulan: "
                                    f"**{row['tanggal_pengumpulan']}** "
                                    f"| Oleh: "
                                    f"**{row['input_oleh']}**"
                                )

                                if row['catatan']:
                                    st.write(row['catatan'])

                            # ================= STATUS =================
                            with col2:

                                st.caption(status_badge)

                                if (
                                    row['status'] == 'selesai'
                                    and boleh_aksi
                                ):

                                    if st.button(
                                        "↩️ Batalkan",
                                        key=f"batal_{unique_suffix}"
                                    ):

                                        batalkan_selesai(
                                            row['id']
                                        )

                                        st.success(
                                            "Dikembalikan ke PR Aktif!"
                                        )

                                        st.rerun()

                            # ================= HAPUS =================
                            with col3:

                                if boleh_aksi:

                                    if st.button(
                                        "🗑️ Hapus",
                                        key=f"hapus_{unique_suffix}"
                                    ):

                                        hapus_permanen(
                                            row['id']
                                        )

                                        st.success(
                                            "PR dihapus permanen!"
                                        )

                                        st.rerun()

                    st.markdown("---")
