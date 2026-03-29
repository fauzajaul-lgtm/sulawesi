import os
import processing

# Folder input (isi geojson per kelurahan)
input_folder = r"C:\Users\Asus\OneDrive\Documents\Jagung\jatim\35.22_bojonegoro"

# Folder output (hasil per kecamatan)
output_folder = os.path.join(input_folder, "hasil_perkecamatan")
os.makedirs(output_folder, exist_ok=True)

# Nama field kecamatan (GANTI sesuai data kamu)
field_kecamatan = "kd_kecamatan"

# Ambil semua file geojson
geojson_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".geojson")]

# List semua fitur dari semua geojson
all_layers = []
for file in geojson_files:
    all_layers.append(file)

# Gabungkan semua geojson jadi satu layer sementara
merged = processing.run("native:mergevectorlayers", {
    'LAYERS': all_layers,
    'CRS': None,
    'OUTPUT': 'memory:merged'
})['OUTPUT']

# Ambil nilai unik kecamatan
unique_kecamatan = merged.uniqueValues(merged.fields().indexFromName(field_kecamatan))

for kec in unique_kecamatan:
    kec_str = str(kec)
    safe_kec = kec_str.replace(" ", "_").replace("/", "_")

    # Filter kecamatan
    filtered = processing.run("native:extractbyexpression", {
        'INPUT': merged,
        'EXPRESSION': f"\"{field_kecamatan}\" = '{kec_str}'",
        'OUTPUT': 'memory:filtered'
    })['OUTPUT']

    # Simpan output per kecamatan
    out_path = os.path.join(output_folder, f"{safe_kec}.geojson")

    processing.run("native:savefeatures", {
        'INPUT': filtered,
        'OUTPUT': out_path
    })

    print(f"Berhasil dibuat: {safe_kec}.geojson")

print("🔥 SELESAI! Semua kecamatan sudah jadi file masing-masing.")import os
import processing

# Folder input (isi geojson per kelurahan)
input_folder = r"C:\Users\Asus\OneDrive\Documents\Jagung\jatim\35.22_bojonegoro"

# Folder output (hasil per kecamatan)
output_folder = os.path.join(input_folder, "hasil_perkecamatan")
os.makedirs(output_folder, exist_ok=True)

# Nama field kecamatan (GANTI sesuai data kamu)
field_kecamatan = "kd_kecamatan"

# Ambil semua file geojson
geojson_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".geojson")]

# List semua fitur dari semua geojson
all_layers = []
for file in geojson_files:
    all_layers.append(file)

# Gabungkan semua geojson jadi satu layer sementara
merged = processing.run("native:mergevectorlayers", {
    'LAYERS': all_layers,
    'CRS': None,
    'OUTPUT': 'memory:merged'
})['OUTPUT']

# Ambil nilai unik kecamatan
unique_kecamatan = merged.uniqueValues(merged.fields().indexFromName(field_kecamatan))

for kec in unique_kecamatan:
    kec_str = str(kec)
    safe_kec = kec_str.replace(" ", "_").replace("/", "_")

    # Filter kecamatan
    filtered = processing.run("native:extractbyexpression", {
        'INPUT': merged,
        'EXPRESSION': f"\"{field_kecamatan}\" = '{kec_str}'",
        'OUTPUT': 'memory:filtered'
    })['OUTPUT']

    # Simpan output per kecamatan
    out_path = os.path.join(output_folder, f"{safe_kec}.geojson")

    processing.run("native:savefeatures", {
        'INPUT': filtered,
        'OUTPUT': out_path
    })

    print(f"Berhasil dibuat: {safe_kec}.geojson")

print("🔥 SELESAI! Semua kecamatan sudah jadi file masing-masing.")