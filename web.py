import os
import streamlit as st

st.title("📚 Info Kelas & Jadwal Pelajaran")

# --- DAFTAR NAMA YANG DIBLOKIR TOTAL DARI WEB ---
# Tulis nama panggilan mereka dengan huruf kecil semua di sini
daftar_blokir = ["p", "", ""]

# --- GERBANG UTAMA (MINTA NAMA SEBELUM BUKA WEB) ---
st.subheader("🔒 Verifikasi Pengunjung")
nama_pengunjung = st.text_input(
    "Masukkan nama lengkap atau panggilanmu untuk masuk:"
)

# Jika belum isi nama, web ditahan (tidak menampilkan jadwal & PR)
if not nama_pengunjung:
  st.warning("⚠️ Silakan ketik namamu terlebih dahulu untuk membuka website.")
  st.stop()  # Menghentikan kode agar tidak lanjut ke bawah

# Cek apakah nama pengunjung ada di daftar blokir
kena_blokir = any(b in nama_pengunjung.lower() for b in daftar_blokir)

if kena_blokir:
  st.error(
      f"❌ Maaf {nama_pengunjung}, kamu sedang dalam masa hukuman dan **tidak"
      " diizinkan** mengakses website ini!"
  )
  st.stop()  # Menghentikan web total (mereka tidak bisa lihat apa-apa lagi)

# Jika lolos blokir, web akan terbuka normal di bawah ini:
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

# --- FORM TAMBAH PR DENGAN PASSWORD PIKET ---
st.subheader(f"Tambah PR untuk Hari {hari} (Khusus Petugas Piket)")


def get_password(hari):
  passwords = {
      "Senin": "senin",
      "Selasa": "selasa",
      "Rabu": "rabu",
      "Kamis": "kamis",
      "Jum'at": "jumat",
  }
  return passwords.get(hari)


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
