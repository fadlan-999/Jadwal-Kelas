import streamlit as st
import os

st.title("📚 Info Kelas & Jadwal Pelajaran")

# --- BAGIAN JADWAL ---
st.header("📅 Jadwal Pelajaran")
hari = st.selectbox("Pilih Hari:", ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at"])

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

# --- BAGIAN PR ---
st.header("📝 Catatan PR Kelas")

# Membaca isi file PR
if os.path.exists("pr_kelas.txt"):
    with open("pr_kelas.txt", "r") as f:
        isi_pr = f.read()
else:
    isi_pr = "Belum ada PR nih. Santai dulu!"

# Menampilkan PR dalam kotak biru
st.info(isi_pr)

# Form untuk menambah PR
st.subheader("Tambah PR Baru")
pr_baru = st.text_input("Ketik tugas baru di sini:")
if st.button("Simpan PR"):
    if pr_baru:
        with open("pr_kelas.txt", "a") as f:
            f.write("- " + pr_baru + "\n")
        st.success("PR berhasil ditambahkan! Silakan refresh (muat ulang) halaman ini.")

# Tombol untuk menghapus PR
if st.button("Hapus Semua PR"):
    if os.path.exists("pr_kelas.txt"):
        os.remove("pr_kelas.txt")
        st.success("Semua PR sudah dihapus! Silakan refresh (muat ulang) halaman ini.")
