# NutClassify - Klasifikasi Jenis Kacang-kacangan dengan Transfer Learning VGG16

Aplikasi web berbasis Flask yang mengklasifikasikan jenis kacang-kacangan (tree nuts) dari foto menggunakan model deep learning hasil transfer learning dengan arsitektur VGG16.

Dibuat untuk memenuhi Tugas 11 mata kuliah Praktikum Kecerdasan Buatan - Universitas Bale Bandung.

## Studi Kasus

Klasifikasi Gambar (Image Classification) - mengenali 10 jenis kacang pohon dari satu foto yang diunggah pengguna.

## Dataset

- **Sumber:** [Tree Nuts Image Classification](https://www.kaggle.com/datasets/gpiosenka/tree-nuts-image-classification) (Kaggle)
- **Jumlah kelas:** 10 - almonds, brazil nuts, cashews, coconut, hazelnuts, macadamia, pecans, pine nuts, pistachios, walnuts
- **Jumlah gambar:** 1163 (training), 50 (validasi), 50 (testing)
- **Format:** JPG, 224x224 piksel, RGB

## Arsitektur Model

Base model VGG16 (pretrained ImageNet, `include_top=False`) ditambah classifier baru:

```
VGG16 (frozen) → Flatten → Dense(256, relu) → Dropout(0.5) → Dense(10, softmax)
```

**Strategi training dua tahap:**

1. **Feature extraction** (8 epoch) - seluruh layer VGG16 dibekukan, hanya classifier baru yang dilatih
2. **Fine-tuning** (12 epoch) - block5 VGG16 dibuka dan dilatih ulang dengan learning rate kecil (1e-5) agar model bisa menyesuaikan fitur visual spesifik terhadap tekstur dan bentuk kacang

**Hasil akhir:** akurasi 66% (feature extraction saja) meningkat menjadi **86%** setelah fine-tuning pada data test.

## Struktur Folder

```
PROJECT_VGG16_NUTS/
├── templates/
│   ├── index.html
│   ├── klasifikasi.html
│   ├── tentang_dataset.html
│   └── cara_penggunaan.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── script.js
│   │   └── theme.js
│   └── images/
│       └── (10 gambar contoh, satu per jenis kacang)
├── dokumentasi/          
│   ├── grafik_accuracy.png
│   ├── grafik_loss.png
├── data/
│   ├── train/
│   ├── valid/
│   └── test/
├── app.py
├── train_model.py
├── model_vgg16_nuts.h5
└── requirements.txt
```

## Fitur Aplikasi

- **Beranda** - pengenalan aplikasi, statistik model, dan galeri jenis kacang
- **Klasifikasi** - upload gambar (drag & drop atau klik), hasil prediksi dengan confidence score dan 2-3 kemungkinan lain
- **Tentang Dataset** - detail dataset, augmentasi data, dan keterbatasannya
- **Cara Penggunaan** - panduan langkah demi langkah dan penjelasan istilah teknis
- Mode gelap/terang (dapat diganti lewat toggle di navbar)
- Desain responsif, dapat diakses dari perangkat mobile

## Cara Menjalankan (Lokal)

1. Buat virtual environment dan aktifkan:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install tensorflow flask numpy pillow scipy
   ```

3. Siapkan dataset di folder `data/train`, `data/valid`, `data/test` (struktur per kelas)

4. Latih model:
   ```bash
   python train_model.py
   ```
   Proses ini menghasilkan `model_vgg16_nuts.h5`.

5. Jalankan aplikasi web:
   ```bash
   python app.py
   ```

6. Buka `http://127.0.0.1:5000/` di browser

## Teknologi yang Digunakan

- **Backend:** Flask
- **Model:** TensorFlow / Keras (VGG16 transfer learning)
- **Frontend:** HTML, CSS (custom, tanpa framework), JavaScript vanilla
- **Image processing:** Pillow, NumPy

## Keterbatasan

- Dataset training relatif kecil (±116 gambar per kelas), sehingga akurasi model dibatasi oleh ketersediaan data
- Model sensitif terhadap variasi warna di luar distribusi data training (contoh: pistachio dengan pewarnaan tidak alami cenderung salah diklasifikasikan)
- Belum ada deteksi objek/cropping otomatis, sehingga gambar dengan banyak objek atau background ramai dapat menurunkan akurasi prediksi

## Penulis

Selsa Shafana Alfiyani
NIM 301240041 - Kelas 4B, S1 Teknik Informatika
Universitas Bale Bandung
