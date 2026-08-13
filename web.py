import os
import streamlit as st

st.title("📚 Info Kelas & Jadwal Pelajaran")

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

# --- FORM TAMBAH PR DENGAN KEAMANAN PASSWORD ---
st.subheader(f"Tambah PR untuk Hari {hari} (Khusus Petugas Piket)")

# Daftar nama anak yang diblokir (kalau ada yang nakal, masukkan namanya di sini)
daftar_blokir = ["Rabu"]


# PASSWORD KUAT DARI MASING-MASING PIKET
# (Ganti teks di dalam tanda kutip dengan password yang diberikan oleh anak piket hari itu)
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
  nama_piket = st.text_input("Nama Petugas Piket:")
  password_piket = st.text_input(
      "Password Khusus Hari Ini:", type="password"
  )
  pr_baru = st.text_area(f"Ketik tugas baru untuk {hari}:")

  submit_button = st.form_submit_button(label="Simpan PR")

  if submit_button:
    # 1. Cek apakah nama anak tersebut sedang dihukum
    if nama_piket.lower() in daftar_blokir:
      st.error(
          f"❌ Maaf {nama_piket}, kamu sedang dalam masa hukuman dan tidak"
          " boleh mengisi PR!"
      )
    # 2. Cek password sesuai yang diberikan kelompok piket hari itu
    elif password_piket != get_password(hari):
      st.error(
          f"❌ Password salah! Minta password yang benar ke petugas piket hari"
          f" {hari}."
      )
    elif not nama_piket or not pr_baru:
      st.warning("Nama dan tugas wajib diisi!")
    else:
      with open(file_pr, "a") as f:
        f.write(f"- {pr_baru} (Piket: {nama_piket})\n")
      st.success(
          f"✅ PR untuk hari {hari} berhasil ditambahkan oleh {nama_piket}!"
      )

# Tombol hapus PR khusus darurat (kalau ada salah ketik)
if st.button(f"Hapus Semua PR Hari {hari}"):
  if os.path.exists(file_pr):
    os.remove(file_pr)
    st.success(f"Semua PR hari {hari} sudah dibersihkan!")
