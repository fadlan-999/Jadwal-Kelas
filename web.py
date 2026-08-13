import os
import streamlit as st

st.title("📚 Info Kelas & Jadwal Pelajaran")

# --- DATABASE PASSWORD 36 SISWA (SESUAI ABJAD) ---
password_siswa = {
    "AFIQAH": "afiqah1",
    "AISYAH": "aisy2",
    "ALIF": "alif3",
    "ALIFAH": "alifah4",
    "ALYA": "alya5",
    "ANISA": "anisa6",
    "AZZAM": "azzam7",
    "AZZIZAH": "azzizah8",
    "CAHAYA": "cahaya9",
    "DYAH": "dyah10",
    "DZAKKI": "dzakki11",
    "EIJI": "eiji12",
    "FADLAN": "fadlan13",
    "FAIZ": "faiz14",
    "FAKHRI": "fakhri15",
    "FARAND": "farand16",
    "FATIH": "fatih17",
    "HABIB": "habib18",
    "HAIKAL": "haikal19",
    "JIBRIL": "jibril20",
    "KEANDRA": "keandra21",
    "KEJORA": "kejora22",
    "KEYLA": "keyla23",
    "MASUD": "masud24",
    "NABILA": "nabila25",
    "NADHIF MUZAKI": "nadhifm26",
    "NADHIF RAZA": "nadhifr27",
    "NINDITA": "nindita28",
    "NINDYA": "nindya29",
    "RAFA BB": "rafabb30",
    "RAIS": "rais31",
    "RAKA": "raka32",
    "RIFQA": "rifqa33",
    "SHAQUILLA": "shaquilla34",
    "SHOFI": "shofi35",
    "ZILAN": "zilan36",
}

# --- DAFTAR NAMA YANG DI-BLOKIR (Huruf kecil) ---
daftar_blokir = []

# --- SISTEM LOGIN SISWA ---
st.subheader("🔒 Login Siswa")
nama_pilihan = st.selectbox(
    "Pilih Namamu:", ["Pilih Nama Kamu..."] + list(password_siswa.keys())
)
pw_input = st.text_input("Masukkan Password Pribadimu:", type="password")
masuk_btn = st.button("Masuk")

if "sudah_login" not in st.session_state:
  st.session_state.sudah_login = False
  st.session_state.user_aktif = ""

if masuk_btn:
  if nama_pilihan == "Pilih Nama Kamu...":
    st.warning("⚠️ Silakan pilih namamu terlebih dahulu!")
  elif any(b.lower() in nama_pilihan.lower() for b in daftar_blokir):
    st.error(f"❌ Maaf {nama_pilihan}, akunmu sedang dalam masa hukuman!")
  elif password_siswa.get(nama_pilihan) == pw_input:
    st.session_state.sudah_login = True
    st.session_state.user_aktif = nama_pilihan
    st.success(f"Berhasil masuk sebagai {nama_pilihan}!")
    st.rerun()
  else:
    st.error("❌ Password salah!")

if not st.session_state.sudah_login:
  st.stop()

# --- HALAMAN UTAMA SETELAH LOGIN ---
st.success(f"Halo, {st.session_state.user_aktif}! Selamat datang di info kelas.")
if st.button("Keluar / Logout"):
  st.session_state.sudah_login = False
  st.session_state.user_aktif = ""
  st.rerun()

st.divider()

# --- JADWAL PELAJARAN ---
st.header("📅 Jadwal Pelajaran")
hari = st.selectbox(
    "Pilih Hari:", ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at"]
)

if hari == "Senin":
  st.write("1. Mulok\n2. Fiqih\n3. SKI\n4. Alquran Hadist\n5. Bahasa Indonesia")
elif hari == "Selasa":
  st.write("1. IPA\n2. SBK\n3. Matematika\n4. Bahasa Indonesia\n5. IPS")
elif hari == "Rabu":
  st.write("1. Matematika\n2. PJOK\n3. TIK\n4. Coding\n5. Bahasa Inggris")
elif hari == "Kamis":
  st.write("1. Bahasa Arab\n2. Bahasa Inggris\n3. Aqidah Akhlak\n4. IPS")
elif hari == "Jum'at":
  st.write("1. IPA\n2. PPKN\n3. Bahasa Daerah")

st.divider()

# --- CATATAN PR ---
st.header(f"📝 Catatan PR Hari {hari}")
file_pr = f"pr_{hari.lower()}.txt"

if os.path.exists(file_pr):
  with open(file_pr, "r") as f:
    isi_pr = f.read()
else:
  isi_pr = f"Belum ada PR untuk hari {hari}. Santai dulu!"

st.info(isi_pr)


# --- PASSWORD PIKET HARIAN ---
def get_password_piket(hari):
  passwords = {
      "Senin": "1",
      "Selasa": "2",
      "Rabu": "3",
      "Kamis": "4",
      "Jum'at": "5",
  }
  return passwords.get(hari)


# --- INISIALISASI STATUS BUKA AKSES PIKET PER HARI ---
kunci_piket = f"piket_terbuka_{hari}"
if kunci_piket not in st.session_state:
   st.session_state[kunci_piket] = False

# --- FORM TAMBAH PR (TANPA ULANG PASSWORD TERUS-MENERUS) ---
st.subheader(f"Tambah PR untuk Hari {hari} (Khusus Petugas Piket)")

if not st.session_state[kunci_piket]:
  # Jika belum buka akses, minta password sekali saja
  pw_piket_input = st.text_input(
      f"Masukkan Password Piket Hari {hari} (Sekali Saja):", type="password"
  )
  if st.button("Buka Akses Tambah PR"):
    if pw_piket_input == get_password_piket(hari):
      st.session_state[kunci_piket] = True
      st.success("Akses terbuka! Silakan tambah PR sepuasnya.")
      st.rerun()
    else:
      st.error("❌ Password piket salah!")
else:
  # Jika akses sudah terbuka, tidak perlu masukkan password lagi!
  st.success(
      f"🔓 Akses Input PR Hari {hari} Aktif (Piket: {st.session_state.user_aktif})"
  )

  with st.form(key=f"form_pr_{hari}"):
    pr_baru = st.text_area(f"Ketik tugas baru untuk {hari}:")
    submit_button = st.form_submit_button(label="Simpan PR")

    if submit_button:
      if not pr_baru:
        st.warning("Tugas wajib diisi!")
      else:
        with open(file_pr, "a") as f:
          f.write(
              f"- {pr_baru} (Diposting oleh: {st.session_state.user_aktif})\n"
          )
        st.success(
            f"✅ PR berhasil ditambahkan! Kamu bisa langsung mengetik tugas"
            " berikutnya."
        )

  # Tombol untuk mengunci kembali akses jika sudah selesai
  if st.button("Kunci Kembali Akses Piket"):
    st.session_state[kunci_piket] = False
    st.rerun()

# Tombol hapus PR khusus darurat
if st.button(f"Hapus Semua PR Hari {hari}"):
  if os.path.exists(file_pr):
    os.remove(file_pr)
    st.success(f"Semua PR hari {hari} sudah dibersihkan!")
