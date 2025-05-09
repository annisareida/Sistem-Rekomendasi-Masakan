import streamlit as st

st.title("Sistem Rekomendasi Masakan 🍲")

# Input + CF
bawang = st.selectbox("Apakah menggunakan Bawang?", ["Ya", "Tidak"])
cf_bawang = st.slider("Seberapa yakin untuk pilihan Bawang?", 0.0, 1.0, 1.0)

santan = st.selectbox("Apakah menggunakan Santan?", ["Ya", "Tidak"])
cf_santan = st.slider("Seberapa yakin untuk pilihan Santan?", 0.0, 1.0, 1.0)

cabai_merah = st.selectbox("Apakah menggunakan Cabai Merah?", ["Ya", "Tidak"])
cf_cabai = st.slider("Seberapa yakin untuk pilihan Cabai Merah?", 0.0, 1.0, 1.0)

bahan_utama = st.selectbox("Pilih Bahan Utama:", ["Ayam", "Daging Sapi", "Telur", "Ikan"])

# Inferensi Tipe Masakan + CF
tipe_masakan = None
cf_tipe_masakan = 0.0

if bawang == "Tidak":
    tipe_masakan = "Tidak Lengkap"
    cf_tipe_masakan = cf_bawang * 1.0  # Rule 4
elif bawang == "Ya" and santan == "Ya":
    tipe_masakan = "Gulai"
    cf_tipe_masakan = min(cf_bawang, cf_santan) * 0.8  # Rule 1
elif bawang == "Ya" and cabai_merah == "Ya" and santan == "Tidak":
    tipe_masakan = "Sambal"
    cf_tipe_masakan = min(cf_bawang, cf_cabai, cf_santan) * 0.9  # Rule 2
elif bawang == "Ya" and cabai_merah == "Tidak" and santan == "Tidak":
    tipe_masakan = "Tidak Lengkap"
    cf_tipe_masakan = min(cf_bawang, cf_cabai, cf_santan) * 0.7  # Rule 3

# Inferensi Rekomendasi + CF
rekomendasi = None
cf_rekomendasi = 0.0

if tipe_masakan == "Gulai":
    if bahan_utama == "Ayam":
        rekomendasi = "Gulai Ayam"
        cf_rekomendasi = cf_tipe_masakan * 0.95
    elif bahan_utama == "Daging Sapi":
        rekomendasi = "Gulai Daging Sapi"
        cf_rekomendasi = cf_tipe_masakan * 0.95
    elif bahan_utama == "Telur":
        rekomendasi = "Gulai Telur"
        cf_rekomendasi = cf_tipe_masakan * 0.9
    elif bahan_utama == "Ikan":
        rekomendasi = "Gulai Ikan"
        cf_rekomendasi = cf_tipe_masakan * 0.9
elif tipe_masakan == "Sambal":
    if bahan_utama == "Ayam":
        rekomendasi = "Sambal Ayam"
        cf_rekomendasi = cf_tipe_masakan * 0.9
    elif bahan_utama == "Daging Sapi":
        rekomendasi = "Dendeng"
        cf_rekomendasi = cf_tipe_masakan * 0.85
    elif bahan_utama == "Telur":
        rekomendasi = "Telur Sambal"
        cf_rekomendasi = cf_tipe_masakan * 0.9
    elif bahan_utama == "Ikan":
        rekomendasi = "Ikan Sambal"
        cf_rekomendasi = cf_tipe_masakan * 0.85
elif tipe_masakan == "Tidak Lengkap":
    rekomendasi = "Tidak Lengkap"
    cf_rekomendasi = cf_tipe_masakan * 1.0

# Output
if st.button("Proses"):
    st.subheader("Hasil Inferensi")
    st.write(f"**Tipe Masakan**: {tipe_masakan}")
    st.write(f"**CF Tipe Masakan**: {cf_tipe_masakan:.2f}")
    st.write(f"**Rekomendasi**: {rekomendasi}")
    st.write(f"**CF Rekomendasi**: {cf_rekomendasi:.2f}")
