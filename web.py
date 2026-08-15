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

# --- DAFTAR NAMA SISWA SEKELAS ---
daftar_siswa = [
    "Pilih Nama Kamu...",
    "AFIQAH", "AISYAH", "ALIF", "ALIFAH", "ALYA", "ANISA", "AZZAM", 
    "AZZIZAH", "CAHAYA", "DYAH", "DZAKKI", "EIJI", "FADLAN", "FAIZ", 
    "FAKHRI", "FARAND", "FATIH", "HABIB", "HAIKAL", "JIBRIL", "KEANDRA", 
    "KEJORA", "KEYLA", "MASUD", "NABILA", "NADHIF MUZAKI", 
    "NADHIF RAZA", "NINDITA", "NINDYA", "RAFA BB", "RAIS", "RAKA", 
    "RIFQA", "SHAQUILLA", "SHOFI", "ZILAN"
]

daftar_blokir = []

# --- SISTEM LOGIN SISWA ---
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

if st.button(f"Hapus Semua PR Hari {hari}"):
  if os.path.exists(file_pr):
    os.remove(file_pr)
    st.success(f"Semua PR hari {hari} sudah dibersihkan!")


# ==========================================
# --- FITUR BARU: ASISTEN AI KELAS (GROQ) ---
# ==========================================
st.divider()
st.title("⚡ Asisten AI Kelas (Llama 3)")
st.write("Bot ini anti-lag dan sudah membaca seluruh catatan PR kelas kita. Tanya apa saja!")

try:
    from groq import Groq
    
    # 1. Menghubungkan Kunci API Groq
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # 2. Mengumpulkan Data PR secara diam-diam
    ingatan_kelas = "Kamu adalah asisten AI ramah khusus untuk kelasku. Gunakan bahasa Indonesia yang santai tapi sopan. Berikut adalah data PR kelas saat ini yang harus kamu jadikan acuan menjawab:\n"
    for hari_cek in ["senin", "selasa", "rabu", "kamis", "jum'at"]:
        file_cek = f"pr_{hari_cek}.txt"
        if os.path.exists(file_cek):
            with open(file_cek, "r") as f:
                ingatan_kelas += f"- Hari {hari_cek.capitalize()}: {f.read()}\n"
        else:
            ingatan_kelas += f"- Hari {hari_cek.capitalize()}: Tidak ada PR.\n"

    # 3. Menyiapkan memori obrolan Groq
    if "groq_chat" not in st.session_state:
        # Pesan tipe "system" adalah instruksi rahasia yang tidak muncul di layar
        st.session_state.groq_chat = [
            {"role": "system", "content": ingatan_kelas}
        ]

    # 4. Menampilkan riwayat chat di layar (kecuali pesan sistem)
    for message in st.session_state.groq_chat:
        if message["role"] != "system":
            # Groq memakai role "assistant", bukan "model" seperti Gemini
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 5. Kolom input user
    pertanyaan_user = st.chat_input("Tanya soal PR atau materi sekolah di sini...")

    if pertanyaan_user:
        # Tampilkan chat user
        with st.chat_message("user"):
            st.markdown(pertanyaan_user)
        
        # Simpan ke memori sementara
        st.session_state.groq_chat.append({"role": "user", "content": pertanyaan_user})
        
       # Panggil mesin Llama 3 dari Groq
with st.chat_message("assistant"):
    respon = client.chat.completions.create(
        model="llama-3.1-8b-instant", # Mesin generasi terbaru
        messages=st.session_state.groq_chat,
        temperature=0.7
    )
            jawaban_ai = respon.choices[0].message.content
            st.markdown(jawaban_ai)
            
        # Simpan balasan AI ke memori
        st.session_state.groq_chat.append({"role": "assistant", "content": jawaban_ai})

except KeyError:
    st.error("⚠️ Ups! API Key Groq belum dipasang di 'Secrets' Streamlit.")
except ImportError:
    st.error("⚠️ Sistem sedang mengunduh mesin Groq. Tunggu sebentar sampai Streamlit selesai me-refresh aplikasi (pastikan file requirements.txt sudah di-update).")
except Exception as e:
    st.error(f"❌ Terjadi kesalahan pada AI: {e}")
