import os
import processing
from qgis.core import QgsProject

# FIELD kecamatan dan kelurahan (sesuaikan nama field di atribut)
field_kecamatan = "kd_kecamatan"
field_kelurahan = "kd_kelurahan"

# Folder output utama
output_folder = r"C:\Users\Asus\OneDrive\Documents\Jagung\kota batu\hasil_kelurahan_perkecamatan"
os.makedirs(output_folder, exist_ok=True)

# Loop layer 001 sampai 020
for i in range(1,4):
    layer_name = str(i).zfill(3)  # jadi 001, 002, dst

    layers_found = QgsProject.instance().mapLayersByName(layer_name)

    if len(layers_found) == 0:
        print(f"⚠️ Layer {layer_name} tidak ditemukan, skip.")
        continue

    layer = layers_found[0]
    print(f"\n📌 Memproses layer: {layer_name}")

    idx_kec = layer.fields().indexFromName(field_kecamatan)
    idx_kel = layer.fields().indexFromName(field_kelurahan)

    if idx_kec == -1:
        print(f"❌ Field '{field_kecamatan}' tidak ditemukan di layer {layer_name}")
        continue

    if idx_kel == -1:
        print(f"❌ Field '{field_kelurahan}' tidak ditemukan di layer {layer_name}")
        continue

    # Ambil kecamatan unik
    unique_kecamatan = layer.uniqueValues(idx_kec)

    for kec in unique_kecamatan:
        kec_str = str(kec).strip()
        safe_kec = kec_str.replace(" ", "_").replace("/", "_")

        # Buat folder kecamatan
        kec_folder = os.path.join(output_folder, safe_kec)
        os.makedirs(kec_folder, exist_ok=True)

        # Filter kecamatan
        layer_kec = processing.run("native:extractbyexpression", {
            'INPUT': layer,
            'EXPRESSION': f"trim(\"{field_kecamatan}\") = '{kec_str}'",
            'OUTPUT': 'memory:kec'
        })['OUTPUT']

        # Ambil kelurahan unik dalam kecamatan tsb
        unique_kelurahan = layer_kec.uniqueValues(idx_kel)

        for kel in unique_kelurahan:
            kel_str = str(kel).strip()
            safe_kel = kel_str.replace(" ", "_").replace("/", "_")

            # Filter kelurahan
            layer_kel = processing.run("native:extractbyexpression", {
                'INPUT': layer_kec,
                'EXPRESSION': f"trim(\"{field_kelurahan}\") = '{kel_str}'",
                'OUTPUT': 'memory:kel'
            })['OUTPUT']

            if layer_kel.featureCount() == 0:
                continue

            # Simpan output kelurahan
            out_path = os.path.join(kec_folder, f"{safe_kel}.geojson")

            processing.run("native:savefeatures", {
                'INPUT': layer_kel,
                'OUTPUT': out_path
            })

            print(f"✅ {layer_name} -> {safe_kec} -> {safe_kel}.geojson")

print("\n🔥 SELESAI! Semua layer 001-020 sudah diproses.")