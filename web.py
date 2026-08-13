import os
import streamlit as st

st.title("📚 Info Kelas & Jadwal Pelajaran")

# --- DAFTAR NAMA SISWA SEKELAS (HURUF BESAR SESUAI ABJAD) ---
daftar_siswa = [
    "Pilih Nama Kamu...",
    "AFIQAH",
    "AISYAH",
    "ALIF",
    "ALIFAH",
    "ALYA",
    "ANISA",
    "AZZAM",
    "AZZIZAH",
    "CAHAYA",
    "DYAH",
    "DZAKKI",
    "EIJI",
    "FADLAN",
    "FAIZ",
    "FAKHRI",
    "FARAND",
    "FATIH",
    "HABIB",
    "HAIKAL",
    "JIBRIL",
    "KEANDRA",
    "KEJORA",
    "KEYLA ELVINA QUEENZA",
    "MASUD",
    "NABILA",
    "NADHIF MUZAKI",
    "NADHIF RAZA",
    "NINDITA",
    "NINDYA",
    "RAFA BB",
    "RAIS",
    "RAKA",
    "RIFQA",
    "SHAQUILLA",
    "SHOFI",
    "ZILAN",
]

# --- DAFTAR NAMA YANG DI-BLOKIR (Gunakan huruf kecil semua) ---
# Contoh: ["budi", "joko"]
daftar_blokir = ["FADLAN"] 

# --- GERBANG UTAMA (MENU PILIH NAMA / DROPDOWN) ---
st.subheader("🔒 Verifikasi Pengunjung")
nama_pengunjung = st.selectbox("Pilih Namamu dari Daftar:", daftar_siswa)

# Jika belum memilih nama
if nama_pengunjung == "Pilih Nama Kamu...":
  st.warning("⚠️ Silakan pilih namamu terlebih dahulu untuk membuka website.")
  st.stop() 

# Cek apakah nama yang dipilih masuk daftar blokir
kena_blokir = any(b.lower() in nama_pengunjung.lower() for b in daftar_blokir)

if kena_blokir:
  st.error(
      f"❌ Maaf {nama_pengunjung}, kamu sedang dalam masa hukuman dan **tidak"
      " diizinkan** mengakses website ini!"
  )
  st.stop() 

# Jika lolos verifikasi, web terbuka normal:
st.success(f"Halo, {nama_pengunjung}! Selamat datang di info kelas.")
st.divider()

# --- BAGIAN JADWAL & PILIH HARI ---
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

# --- BAGIAN PR BERDASARKAN HARI ---
st.header(f"📝 Catatan PR Hari {hari}")
file_pr = f"pr_{hari.lower()}.txt"

if os.path.exists(file_pr):
  with open(file_pr, "r") as f:
    isi_pr = f.read()
else:
  isi_pr = f"Belum ada PR untuk hari {hari}. Santai dulu!"

st.info(isi_pr)

# --- PASSWORD PIKET BERDASARKAN HARI ---
def get_password(hari):
  passwords = {
      "Senin": "1",
      "Selasa": "2",
      "Rabu": "3",
      "Kamis": "4",
      "Jum'at": "5",
  }
  return passwords.get(hari)

# --- FORM TAMBAH PR DENGAN PASSWORD PIKET ---
st.subheader(f"Tambah PR untuk Hari {hari} (Khusus Petugas Piket)")

with st.form(key=f"form_pr_{hari}"):
  password_piket = st.text_input(
      "Password Khusus Hari Ini:", type="password"
  )
  pr_baru = st.text_area(f"Ketik tugas baru untuk {hari}:")
  submit_button = st.form_submit_button(label="Simpan PR")

  if submit_button:
    if password_piket != get_password(hari):
      st.error(
          f"❌ Password salah! Minta password yang benar ke petugas piket hari"
          f" {hari}."
      )
    elif not pr_baru:
      st.warning("Tugas wajib diisi!")
    else:
      with open(file_pr, "a") as f:
        f.write(f"- {pr_baru} (Piket: {nama_pengunjung})\n")
      st.success(
          f"✅ PR untuk hari {hari} berhasil ditambahkan oleh {nama_pengunjung}!"
      )

# Tombol hapus PR khusus darurat
if st.button(f"Hapus Semua PR Hari {hari}"):
  if os.path.exists(file_pr):
    os.remove(file_pr)
    st.success(f"Semua PR hari {hari} sudah dibersihkan!")
