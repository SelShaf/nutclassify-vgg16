// script.js
// Logika upload gambar dan pemanggilan endpoint /predict
// hanya dipakai di halaman klasifikasi.html

document.addEventListener("DOMContentLoaded", function () {
    const uploadArea = document.getElementById("upload-area");
    const fileInput = document.getElementById("file-input");
    const previewContainer = document.getElementById("preview-container");
    const previewImg = document.getElementById("preview-img");
    const pesanValidasi = document.getElementById("pesan-validasi");
    const btnAnalisis = document.getElementById("btn-analisis");
    const statusLoading = document.getElementById("status-loading");
    const hasilCard = document.getElementById("hasil-card");
    const hasilGambar = document.getElementById("hasil-gambar-img");
    const hasilLabel = document.getElementById("hasil-label");
    const badgeStatus = document.getElementById("badge-status");
    const hasilConfidenceText = document.getElementById("hasil-confidence-text");
    const confidenceBarFill = document.getElementById("confidence-bar-fill");
    const opsiLainList = document.getElementById("opsi-lain-list");

    let fileTerpilih = null;
    let dataUrlGambar = null;

    if (!uploadArea) {
        return;
    }

    uploadArea.addEventListener("click", function () {
        fileInput.click();
    });

    fileInput.addEventListener("change", function (e) {
        if (e.target.files.length > 0) {
            tampilkanPreview(e.target.files[0]);
        }
    });

    uploadArea.addEventListener("dragover", function (e) {
        e.preventDefault();
        uploadArea.classList.add("drag-over");
    });

    uploadArea.addEventListener("dragleave", function () {
        uploadArea.classList.remove("drag-over");
    });

    uploadArea.addEventListener("drop", function (e) {
        e.preventDefault();
        uploadArea.classList.remove("drag-over");
        if (e.dataTransfer.files.length > 0) {
            tampilkanPreview(e.dataTransfer.files[0]);
        }
    });

    function tampilkanPreview(file) {
        if (!file.type.startsWith("image/")) {
            pesanValidasi.textContent = "File yang dipilih harus berupa gambar";
            pesanValidasi.style.display = "block";
            return;
        }

        fileTerpilih = file;
        pesanValidasi.style.display = "none";
        hasilCard.style.display = "none";

        const reader = new FileReader();
        reader.onload = function (e) {
            dataUrlGambar = e.target.result;
            previewImg.src = dataUrlGambar;
            previewContainer.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    btnAnalisis.addEventListener("click", function () {
        if (!fileTerpilih) {
            pesanValidasi.textContent = "Silakan pilih gambar terlebih dahulu";
            pesanValidasi.style.display = "block";
            return;
        }

        pesanValidasi.style.display = "none";
        hasilCard.style.display = "none";
        statusLoading.style.display = "block";

        const formData = new FormData();
        formData.append("file", fileTerpilih);

        fetch("/predict", {
            method: "POST",
            body: formData
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                statusLoading.style.display = "none";

                if (data.error) {
                    pesanValidasi.textContent = data.error;
                    pesanValidasi.style.display = "block";
                    return;
                }

                tampilkanHasil(data);
            })
            .catch(function () {
                statusLoading.style.display = "none";
                pesanValidasi.textContent = "Terjadi kesalahan saat menghubungi server";
                pesanValidasi.style.display = "block";
            });
    });

    function tampilkanHasil(data) {
        const prediksi = data.prediction;
        const lainnya = data.others;

        hasilGambar.src = dataUrlGambar;
        hasilLabel.textContent = prediksi.label;
        hasilConfidenceText.textContent = prediksi.confidence + "% yakin ini " + prediksi.label;
        confidenceBarFill.style.width = prediksi.confidence + "%";

        // badge tingkat keyakinan berdasarkan confidence score
        badgeStatus.classList.remove("badge-tinggi", "badge-sedang", "badge-rendah");
        if (prediksi.confidence >= 75) {
            badgeStatus.textContent = "Keyakinan Tinggi";
            badgeStatus.classList.add("badge-tinggi");
        } else if (prediksi.confidence >= 45) {
            badgeStatus.textContent = "Keyakinan Sedang";
            badgeStatus.classList.add("badge-sedang");
        } else {
            badgeStatus.textContent = "Keyakinan Rendah";
            badgeStatus.classList.add("badge-rendah");
        }

        opsiLainList.innerHTML = "";
        lainnya.forEach(function (item) {
            const div = document.createElement("div");
            div.className = "opsi-item";
            div.innerHTML = "<span>" + item.label + "</span><span>" + item.confidence + "%</span>";
            opsiLainList.appendChild(div);
        });

        hasilCard.style.display = "block";
    }
});