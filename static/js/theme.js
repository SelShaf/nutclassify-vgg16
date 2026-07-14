// theme.js
// Mengatur mode gelap/terang dan menyimpan pilihan user selama sesi berjalan

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-tema");
    const htmlEl = document.documentElement;

    if (!toggleBtn) {
        return;
    }

    // tema disimpan di variabel biasa (bukan localStorage, supaya kompatibel dengan artifact/browser manapun)
    let temaSaatIni = "light";

    toggleBtn.addEventListener("click", function () {
        temaSaatIni = temaSaatIni === "light" ? "dark" : "light";

        if (temaSaatIni === "dark") {
            htmlEl.setAttribute("data-theme", "dark");
        } else {
            htmlEl.removeAttribute("data-theme");
        }
    });
});