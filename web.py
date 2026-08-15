import os
import streamlit as st

# --- SUNTIKAN CSS UNTUK MENYEMBUNYIKAN LOGO GITHUB & MENU ---
sembunyikan_menu = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(sembunyikan_menu, unsafe_allow_html=True)

st.title("📚 Info Kelas & Jadwal Pelajaran")

# --- DAFTAR NAMA SISWA SEKELAS (TANPA PASSWORD) ---
daftar_siswa = [
    "Pilih Nama Kamu...",
    "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", "AZZAM", 
    "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
    "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", 
    "KEJORA", "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", 
    "NADHIF RAZA", "NINDITA", "NINDYA", "RAFA BB", "RAIS", "RAKA", 
    "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"
]

# --- DAFTAR NAMA YANG DI-BLOKIR (Huruf kecil) ---
daftar_blokir = [""]

# --- SISTEM LOGIN SISWA (HANYA PILIH NAMA) ---
st.subheader("🔒 Verifikasi Siswa")
nama_pilihan = st.selectbox("Pilih Namamu:", daftar_siswa)
masuk_btn = st.button("Masuk")

if "sudah_login" not in st.session_state:
  st.session_state.sudah_login = False
  st.session_state.user_aktif = ""

if masuk_btn:
  if nama_pilihan == "Pilih Nama Kamu...":
    st.warning("⚠️ Silakan pilih namamu terlebih dahulu!")
  elif any(b.lower() in nama_pilihan.lower() for b in daftar_blokir):
    st.error(f"❌ Maaf {nama_pilihan}, akunmu sedang dalam masa hukuman!")
  else:
    st.session_state.sudah_login = True
    st.session_state.user_aktif = nama_pilihan
    st.success(f"Berhasil masuk sebagai {nama_pilihan}!")
    st.rerun()

# Jika belum login, tahan halaman di sini
if not st.session_state.sudah_login:
  st.stop()

# --- HALAMAN UTAMA SETELAH LOGIN ---
st.success(f"Halo, {st.session_state.user_aktif}! Selamat datang di info kelas.")
if st.button("Keluar / Ganti Nama"):
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

# --- FORM TAMBAH PR ---
st.subheader(f"Tambah PR untuk Hari {hari}")

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
          f"✅ PR berhasil ditambahkan oleh {st.session_state.user_aktif}!"
      )

# Tombol hapus PR khusus darurat
if st.button(f"Hapus Semua PR Hari {hari}"):
  if os.path.exists(file_pr):
    os.remove(file_pr)
    st.success(f"Semua PR hari {hari} sudah dibersihkan!")


# ==========================================
# --- FITUR BARU: ASISTEN AI CHATBOT ---
# ==========================================
st.divider()
st.title("🤖 Asisten AI Kelas")
st.write("Silakan tanya apa saja ke bot ini!")

# 1. Menyiapkan memori untuk menyimpan riwayat obrolan
if "riwayat_chat" not in st.session_state:
    st.session_state.riwayat_chat = []

# 2. Menampilkan obrolan yang sudah ada di memori
for chat in st.session_state.riwayat_chat:
    with st.chat_message(chat["peran"]):
        st.markdown(chat["pesan"])

# 3. Kolom untuk mengetik pesan di bagian bawah layar
pertanyaan_user = st.chat_input("Ketik pertanyaanmu di sini...")

if pertanyaan_user:
    # Tampilkan chat dari user di layar
    with st.chat_message("user"):
        st.markdown(pertanyaan_user)
    # Simpan ke memori
    st.session_state.riwayat_chat.append({"peran": "user", "pesan": pertanyaan_user})

    # --- Di sinilah nanti kita akan memanggil "Otak AI" sungguhan ---
    # Untuk sementara, bot hanya akan membeo
    jawaban_ai = f"Halo! Aku asisten AI kelas. Kamu tadi bilang: '{pertanyaan_user}'. Saat ini otak AI-ku sedang dirakit!"
    # -----------------------------------------------------------------

    # Tampilkan balasan AI di layar
    with st.chat_message("assistant"):
        st.markdown(jawaban_ai)
    # Simpan ke memori
    st.session_state.riwayat_chat.append({"peran": "assistant", "pesan": jawaban_ai})
      
