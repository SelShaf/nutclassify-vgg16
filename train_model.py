# train_model.py
# Transfer Learning VGG16 untuk klasifikasi jenis kacang-kacangan (tree nuts)
# Dua tahap: feature extraction (base dibekukan) lalu fine-tuning (block5 dibuka)

import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import os

print(tf.__version__)

train_dir = 'data/train'
valid_dir = 'data/valid'
test_dir = 'data/test'

# folder untuk menyimpan grafik dan dokumentasi laporan
dokumentasi_dir = 'dokumentasi'
os.makedirs(dokumentasi_dir, exist_ok=True)

classes = sorted(os.listdir(train_dir))
jumlah_kelas = len(classes)

print(f"Jumlah kelas: {jumlah_kelas}")
print(f"Nama kelas: {classes}")

# load VGG16 tanpa fully connected layer, pakai bobot ImageNet
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# tahap 1: bekukan seluruh layer VGG16, hanya classifier baru yang dilatih
for layer in base_model.layers:
    layer.trainable = False

model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(jumlah_kelas, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

valid_data = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

print("Class indices:", train_data.class_indices)

print("=== Tahap 1: melatih classifier baru, base VGG16 dibekukan ===")
history_tahap1 = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=8
)

# tahap 2: buka block terakhir VGG16 (block5) untuk fine-tuning
# block1-block4 tetap dibekukan supaya fitur dasar (garis, tekstur umum) tidak rusak
for layer in base_model.layers:
    if layer.name.startswith('block5'):
        layer.trainable = True
    else:
        layer.trainable = False

# learning rate kecil supaya bobot pretrained tidak berubah drastis
model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

print("=== Tahap 2: fine-tuning block5 VGG16 ===")
history_tahap2 = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=12
)

test_loss, test_acc = model.evaluate(test_data)
print(f'Akurasi Model: {test_acc:.2f}')

model.save('model_vgg16_nuts.h5')
print("Model berhasil disimpan sebagai model_vgg16_nuts.h5")

# ==========================================
# Menggabungkan history dua tahap jadi satu grafik berkesinambungan
# ==========================================
acc = history_tahap1.history['accuracy'] + history_tahap2.history['accuracy']
val_acc = history_tahap1.history['val_accuracy'] + history_tahap2.history['val_accuracy']
loss = history_tahap1.history['loss'] + history_tahap2.history['loss']
val_loss = history_tahap1.history['val_loss'] + history_tahap2.history['val_loss']

epoch_range = range(1, len(acc) + 1)
batas_fine_tuning = len(history_tahap1.history['accuracy'])

# grafik accuracy
plt.figure(figsize=(8, 5))
plt.plot(epoch_range, acc, label='Training Accuracy')
plt.plot(epoch_range, val_acc, label='Validation Accuracy')
plt.axvline(x=batas_fine_tuning, color='gray', linestyle='--', label='Mulai Fine-Tuning')
plt.title('Training vs Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(dokumentasi_dir, 'grafik_accuracy.png'), dpi=150)
plt.close()

# grafik loss
plt.figure(figsize=(8, 5))
plt.plot(epoch_range, loss, label='Training Loss')
plt.plot(epoch_range, val_loss, label='Validation Loss')
plt.axvline(x=batas_fine_tuning, color='gray', linestyle='--', label='Mulai Fine-Tuning')
plt.title('Training vs Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(dokumentasi_dir, 'grafik_loss.png'), dpi=150)
plt.close()

print(f"Grafik berhasil disimpan di folder '{dokumentasi_dir}': grafik_accuracy.png dan grafik_loss.png")