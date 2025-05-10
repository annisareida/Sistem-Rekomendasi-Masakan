import streamlit as st

st.title("Sistem Rekomendasi Masakan 🍲")

cf_map = {
    "Sangat Tidak Yakin": 0.1,
    "Tidak Yakin": 0.3,
    "Mungkin": 0.5,
    "Yakin": 0.7,
    "Sangat Yakin": 0.9
}

# Konversi nilai CF ke tingkat verbal
def verbal_cf(cf):
    if cf < 0.2:
        return "Sangat Tidak Yakin"
    elif cf < 0.4:
        return "Tidak Yakin"
    elif cf < 0.6:
        return "Mungkin"
    elif cf < 0.8:
        return "Yakin"
    else:
        return "Sangat Yakin"

# Input pengguna
bawang = st.selectbox("Apakah menggunakan Bawang?", ["Ya", "Tidak"])
cf_bawang_verbal = st.selectbox("Seberapa yakin untuk pilihan Bawang?", list(cf_map.keys()))
cf_bawang = cf_map[cf_bawang_verbal]

santan = st.selectbox("Apakah menggunakan Santan?", ["Ya", "Tidak"])
cf_santan_verbal = st.selectbox("Seberapa yakin untuk pilihan Santan?", list(cf_map.keys()))
cf_santan = cf_map[cf_santan_verbal]

cabai_merah = st.selectbox("Apakah menggunakan Cabai Merah?", ["Ya", "Tidak"])
cf_cabai_verbal = st.selectbox("Seberapa yakin untuk pilihan Cabai Merah?", list(cf_map.keys()))
cf_cabai = cf_map[cf_cabai_verbal]

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

# Tampilkan hasil
if st.button("Proses"):
    st.subheader("Hasil Inferensi")
    st.write(f"**Tipe Masakan:** {tipe_masakan}")
    st.write(f"**Tingkat Keyakinan Tipe Masakan:** {verbal_cf(cf_tipe_masakan)}")
    st.write(f"**Rekomendasi:** {rekomendasi}")
    st.write(f"**Tingkat Keyakinan Rekomendasi:** {verbal_cf(cf_rekomendasi)}")
